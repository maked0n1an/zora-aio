import random

from web3 import Web3

from utils.chain import Chain
from utils.gas_checker import check_gas
from utils.status import Status
from utils.config import (    
    CHAINS_DATA,
    ZORA_BRIDGE_ABI,
    ZORA_BRIDGE_CONTRACT
)
from utils.logger import logger
from .account import Account


class Bridge(Account):
    def __init__(self, wallet_name: str, private_key: str) -> None:
        super().__init__(wallet_name=wallet_name, private_key=private_key)
        
        self.zora_w3 = Web3(Web3.HTTPProvider(random.choice(CHAINS_DATA[Chain.ZORA]['rpc'])))
        
    def _get_tx_data(self, value: int):
        tx = {
            'chainId': self.zora_w3.chain_id,
            'nonce': self.zora_w3.eth.get_transaction_count(self.address),
            'from': self.address,
            'value': value
        }
        
        return tx
    
    @check_gas
    async def deposit(
        self,
        min_amount: float,
        max_amount: float, 
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int
    ):
        balance, amount_wei, amount = self.get_amount(
            'ETH',
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )
        
        logger.info(f'{self.wallet_name} | {self.address} | Bridge to Starknet | {amount} ETH')
        
        contract = self.get_contract(ZORA_BRIDGE_CONTRACT, ZORA_BRIDGE_ABI) 

        tx_data = self._get_tx_data(amount_wei)
        
        try:
            tx = contract.functions.depositTransaction(
                self.address,
                amount_wei,
                100000,
                False,
                "0x01"
            ).build_transaction(tx_data)
            
            signed_tx = await self.sign(tx)
            
            tx_hash = await self.send_raw_transaction(signed_tx)
            
            self.wait_until_tx_finished(tx_hash.hex(), status_if_success=Status.BRIDGED)
        except Exception as e:
            logger.error(f'{self.wallet_name} | {self.address} | Deposit transaction on L2 network failed | error: {e}')