import asyncio
import random
import time

from web3 import Web3
from web3.eth import AsyncEth
from web3.exceptions import TransactionNotFound
from eth_account import Account as EthereumAccount

from settings.settings import (
    IS_LOW_GAS, MAX_FEE, MAX_PRIORITY
)
from utils.config import (
    CHAINS_DATA, 
    ERC20_ABI
)
from utils.constants import Status, Chain
from utils.logger import logger

class Account:
    def __init__(self, wallet_name: str, private_key: str, chain: Chain) -> None:
        self.wallet_name = wallet_name
        self.private_key = private_key
        self.chain = chain
        
        self.explorer = CHAINS_DATA[chain]["explorer"]
        self.token = CHAINS_DATA[chain]["token"]
        
        self.w3 = Web3(
            Web3.AsyncHTTPProvider(random.choice(CHAINS_DATA[chain]["rpc"])),
            modules={"eth": (AsyncEth,)},
        )
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    def get_contract(self, contract_address: str, contract_abi=None):
        contract_address = Web3.to_checksum_address(contract_address)
        
        if contract_abi is None:
            contract_abi = ERC20_ABI
        
        contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
        
        return contract
    
    def get_balance(self, contract_address: str) -> dict:
        contract = self.get_contract(contract_address)
        
        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimal().call()
        balance_wei = contract.functions.balance_wei().call()
        
        balance = balance_wei / 10 ** decimal
        
        return {
            "balance_wei": balance_wei, 
            "balance": balance, 
            "symbol": symbol,
            "decimal" : decimal
        }
    
    async def check_allowance(self, token_address: str, contract_address: str) -> float:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = await self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = contract.functions.allowance(self.address, contract_address).call()

        return amount_approved
    
    async def get_amount(
        self,
        min_amount: float, 
        max_amount: float, 
        decimal: int, 
        all_amount: bool, 
        min_percent: int, 
        max_percent: int, 
    ):
        random_amount = round(random.uniform(min_amount, max_amount), decimal)
        random_percent = random.randint(min_percent, max_percent)
    
        balance = await self.w3.eth.get_balance(self.address)
        random_balance = int(balance / 100 * random_percent)
        amount_wei =  random_balance if all_amount else Web3.to_wei(random_amount, 'ether')
        amount = Web3.from_wei(random_balance, 'ether') if all_amount else random_amount
        
        return balance, amount_wei, amount
    
    async def wait_until_tx_finished(self, tx_hash: str, max_wait_time=180, status_if_success: Status = Status.SUCCESS):
        start_time = time.time()
        while True:
            try: 
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get('status')
                
                if status == 1:
                    logger.log(status_if_success, f'{self.wallet_name} | {self.address} | {self.explorer}{tx_hash} - successfully!')
                    return True
                elif status is None:
                    await asyncio.sleep(1)
                else:
                    logger.error(f'{self.wallet_name} | {self.address} | {self.explorer}{tx_hash} - transaction failed')
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    logger.log(Status.FAILED, f'{tx_hash} - failed')
                    return False
                await asyncio.sleep(1)
    
    async def sign(self, transaction):
        gas = await self.w3.eth.estimate_gas()        
        gas = int(gas + gas * 0.3)

        transaction.update({'gas': gas})
        
        if IS_LOW_GAS:
            transaction.update({
                'gas': 100000,
                'maxPriorityFeePerGas': int(MAX_PRIORITY * 10 ** 9),
                'maxFeePerGas': int(MAX_FEE * 10 ** 9)
            })
            
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        
        return signed_tx
            
    async def send_raw_transaction(self, signed_tx):
        tx_hash = await self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash   