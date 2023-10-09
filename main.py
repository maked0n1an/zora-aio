import asyncio
import random
import sys
import time

from art import text2art
from termcolor import colored
from questionary import questionary, Choice

from settings.modules_settings import *
from settings.settings import (
    IS_DELAYED_EXECUTION, IS_RANDOM_WALLETS, IS_SLEEP, SLEEP_FROM, SLEEP_TO
)
from utils.config import WALLET_NAMES, ACCOUNTS
from utils.logger import logger, setup_logger_for_output
from utils.sleeping import initial_delay

def check_for_start_bot():
    end_bot = False
    
    if len(ACCOUNTS) == 0:
        logger.error("Please insert account mnemonics in 'accounts.txt'!")
        end_bot = True 
    if len(WALLET_NAMES) == 0:
        logger.error("Please insert names in 'wallet_names.txt'!")
        end_bot = True 
    if len(ACCOUNTS) != len(WALLET_NAMES):
        logger.error("The wallet names' amount must be equal to private keys' amount!")
        end_bot = True 
    
    if end_bot:
        logger.error("-- The bot has ended it's work --")
        sys.exit
        
def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices = [
            Choice('1) Make deposit to Zora', deposit_zora),
            Choice('2) Make withdraw from Zora (!not implemented!)', 'not_implemented'),
            Choice('3) Mint random NFT on Zora Marketplace', mint_random_zora_nft),
            Choice('4) Mint random NFT on MintFun Marketplace', mint_randrom_mintfun_nft),
            Choice('5) Create a random ERC771 NFT collection', create_random_nft_collection),
            Choice('6) Update created collection', update_nft_collection),
            Choice('7) Use custom routes', use_custom_routes)
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        sys.exit()
    return result

def get_wallets():
    data_table = [(wallet_name, account) for wallet_name, account in zip(WALLET_NAMES, ACCOUNTS)]
                                                                                                   
    wallets = [
        {
            "wallet_name": wallet_name,
            "key": key,
        } for wallet_name, key in data_table
    ]
    
    return wallets

def run_module(module, wallet_name, key):
    asyncio.run(module(wallet_name, key))
    
def delay_launch():
    hours = int(input("Please enter the number of hours for the delay: "))
    minutes = int(input("Please enter the number of minutes for the delay: "))
    
    delay_time = hours * 3600 + minutes * 60
    
    logger.info(f'Waiting for {hours} hours {minutes} minutes to start bot')
    time.sleep(delay_time)

def main():
    setup_logger_for_output()
    
    wallets = get_wallets()
    
    if IS_RANDOM_WALLETS:
        random.shuffle(wallets)
    
    if IS_DELAYED_EXECUTION:
        delay_launch()    
    
    for wallet in wallets:
        run_module(module, wallet.get('wallet_name'), wallet.get('key'))
        
        if wallet != wallets[-1] and IS_SLEEP:
            initial_delay(SLEEP_FROM, SLEEP_TO)
        

if __name__ == '__main__':
    art = text2art(text='Zora AIO', font='standart')
    print(colored(art, 'cyan'))
    
    check_for_start_bot()
    
    module = get_module()
    
    if get_module == 'not_implemented':
        sys.exit()
    else: 
        main(module)