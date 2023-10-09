from modules import *
from utils.helpers import retry

@retry
async def deposit_zora(wallet_name, key):  
    """
    Deposit to Zora Network
    _____________________________________
    all_amount = swap from min_percent to max_percent
    """
    
    min_amount = 0.001
    max_amount = 0.009
    decimal = 9
    
    all_amount = False
    
    min_percent = 2
    max_percent = 5
    
    bridge = Bridge(wallet_name, key)
    await bridge.deposit(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)

@retry
async def create_edition(wallet_name, key):
    