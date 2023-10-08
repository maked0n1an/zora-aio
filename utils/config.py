import json

input_data_folder   = 'input_data'
data_folder         = 'data'
abi_folder          = 'abi'

bridge_folder       = 'bridge'
mint_folder         = 'mint'
create_nft_folder   = 'create_nft'

with open(f'{data_folder}/chains/chains.json') as file:
    CHAINS_DATA = json.load(file)

with open(f"{input_data_folder}/wallet_names.txt", "r") as file:
    WALLET_NAMES = [row.strip() for row in file]

with open(f"{input_data_folder}/accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open(f'{data_folder}/{abi_folder}/{bridge_folder}/abi.json') as file:
    ZORA_BRIDGE_ABI = json.load(file)

with open(f'{data_folder}/{abi_folder}/{mint_folder}/abi.json') as file:
    ZORA_MINT_ABI = json.load(file)

with open(f'{data_folder}/{abi_folder}/{create_nft_folder}/erc721_abi.json') as file:
    ZORA_ERC_721_ABI = json.load(file)
    
with open(f'{data_folder}/{abi_folder}/{create_nft_folder}/erc1155_abi.json') as file:
    ZORA_ERC_1155_ABI = json.load(file)
    
with open(f'{data_folder}/{abi_folder}/{create_nft_folder}/custom_erc721_abi.json') as file:
    CUSTOM_ERC_721_ABI = json.load(file)
    
with open(f'{data_folder}/{abi_folder}/mintfun/abi.json') as file:
    MINTFUN_ABI = json.load(file)

with open(f'{data_folder}/{abi_folder}/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

ZORA_BRIDGE_ADDRESS = '0x1a0ad011913A150f69f6A19DF447A0CfD9551054'