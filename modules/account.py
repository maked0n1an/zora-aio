import random
from web3 import Web3
from web3.eth import AsyncEth
from eth_account import Account as EthereumAccount

from utils.config import CHAIN_DATA
from utils.chain import Chain

class Account:
    def __init__(self, wallet_name: str, private_key: str, chain: Chain) -> None:
        self.wallet_name = wallet_name
        self.private_key = private_key
        self.chain = chain
        
        self.rpc = CHAIN_DATA[chain]["rpc"]
        self.explorer = CHAIN_DATA[chain]["explorer"]
        self.token = CHAIN_DATA[chain]["token"]
        
        self.w3 = Web3(Web3.AsyncHTTPProvider(self.rpc),
                       modules={'eth', (AsyncEth,)}, middlewares=[])
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    def get_contract(self, contract_address: str, contract_abi=None):
        contract_address = Web3.to_checksum_address(contract_address)
        
        if contract_abi is None:
            contract_abi = ""
        
        contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
        
        return contract
    
    def get_balance(self, contract_address: str) -> dict:
        contract_address = Web3.to_checksum_address(contract_address)
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
    
    def approve(self, amount: float, token_address: str, contract_address: str):
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)
        
        
    
    # def get_amount(
    #     self,
    #     from_token: str, 
    #     min_amount: float, 
    #     max_amount: float, 
    #     decimal: int, 
    #     all_amount: bool, 
    #     min_percent: int, 
    #     max_percent: int, 
    # ):
    #     random_amount = round(random.uniform(min_amount, max_amount), decimal)
    #     random_percent = random.randint(min_percent, max_percent)
    
    # def check_allowance(self, amount: float, token_address: str, contract_address: str):
    #     token_address = Web3.to_checksum_address(token_address)
    #     contract_address = Web3.to_checksum_address(contract_address)
        
    #     contract = self.w3.eth.contract(address=token_address, abi=)
        