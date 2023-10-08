import random

from web3 import Web3
from utils.config import CHAINS_DATA
from settings.settings import (
    CHECK_GWEI, MAX_GWEI,MIN_ETH_BALANCE
)
from utils.logger import logger
from utils.sleeping import sleep


def _get_gas():
    try:
        w3 = Web3(Web3.HTTPProvider(random.choice(CHAINS_DATA["ethereum"]["rpc"])))
        gas_price = w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')
        return gwei
    except Exception as error:
        logger.error(error)


def _wait_gas():
    while True:
        gas = _get_gas()

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            sleep(60, 70)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {MAX_GWEI}")
            break

# decorator
def check_gas(func):
    def _wrapper(*args, **kwargs):
        if CHECK_GWEI:
            _wait_gas()
        return func(*args, **kwargs)

    return _wrapper

# decorator
def check_eth_balance(func):
    async def _wrapper(self, *args, **kwargs):
        eth_balance = await self.get_eth_balance()
        
        if eth_balance < MIN_ETH_BALANCE:
            from_token = kwargs['from_token']
            to_token = kwargs['to_token']
            
            if kwargs['from_token'] == "ETH":           
                kwargs['from_token'] = kwargs['to_token']
                             
            kwargs['to_token'] = "ETH"
                
            kwargs['all_amount'] = True
            kwargs['min_percent'] = 50
            kwargs['max_percent'] = 100
            
            self.logger.info(f"Changed from <{from_token} -> {to_token}> to <{kwargs['from_token']} -> ETH>")

        return await func(self, *args, **kwargs)

    return _wrapper