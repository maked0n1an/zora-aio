import random
import time
import requests

from web3 import Web3

from .account import Account
from settings.settings import (
    EDITION_SIZE,
    MINT_PRICE
)
from utils.constants import Chain
from utils.helpers import check_gas
from utils.config import (
    ENGLISH_WORDS,
    ZORA_NFT_CREATOR_ABI, 
    ZORA_NFT_CREATOR_ADDRESS
)

class Nft(Account):
    def __init__(self, wallet_name: str, private_key: str, chain = Chain.ZORA) -> None:
        super().__init__(wallet_name=wallet_name, private_key=private_key, chain=chain)
    
    def _get_random_words(n: int):
        return [random.choice(ENGLISH_WORDS) for _ in range(n)]    
    
    def _decimal_to_int(d, n):
        return int(d * (10 ** n))
    
    def _generate_collection_name_and_symbol(self):
        while True:
            name = ' '.join(self._get_random_words(random.randint(1, 3))).title()
            consonants = [char for char in name if char not in 'aeiou ']
            symbol = ''.join(consonants)[:3].upper()
            
            if len(name) >= 4 and len(symbol) >= 3:
                return name, symbol
            else:
                self._generate_collection_name_and_symbol()
                
    def _generate_description(self):
        description_words = self._get_random_words(random.randint(3, 10))
        description_words[0] = description_words[0].capitalize()
        description = ' '.join(description_words)
        return description

    def upload_image_ipfs(self, name):
        img_szs = [i for i in range(500, 1001, 50)]
        url = f'https://picsum.photos/{random.choice(img_szs)}/{random.choice(img_szs)}'
        resp = requests.get(url, proxies=self.http_proxies, timeout=60)
        if resp.status_code != 200:
            raise Exception(f'Get random image failed, status_code = {resp.status_code}, response = {resp.text}')
        filename = name.replace(' ', '_').lower() + '.jpg'
        return self.upload_ipfs(filename, resp.content, 'image/jpg')
    
    def get_image_uri(self, name):
        return 'ipfs://' + self.upload_image_ipfs(name)
    
        
    
    @check_gas
    async def create_collection(self):
        contract = self.w3.eth.contract(ZORA_NFT_CREATOR_ADDRESS, ZORA_NFT_CREATOR_ABI)
        
        name, symbol = self._generate_collection_name_and_symbol()
        description = self._generate_description()
        price = self._decimal_to_int(round(random.uniform(MINT_PRICE[0], MINT_PRICE[1]), 6), 18)
        edition_size = random.randint(EDITION_SIZE[0], EDITION_SIZE[1])
        royalty = random.randint(0, 10) * 100
        merkle_root = '0x0000000000000000000000000000000000000000000000000000000000000000'
        sale_config = (price, 2 ** 32 - 1, int(time.time()), edition_size, 0, 0, self.zora_w3.to_bytes(merkle_root))        
        image_uri = self.get_image_uri(name)
        
        args = {
            name, symbol,
            edition_size, royalty,
            self.address, self.address,
            sale_config, description, '', image_uri
        }
        
        check_gas()
        
        tx_data = {
            'from': self.address,
            'nonce': await self.w3.eth.get_transaction_count(self.address) 
        }
        
        tx = await contract.functions.createEdition(*args).build_transaction(tx_data)
        
        
        
        
        
        
        