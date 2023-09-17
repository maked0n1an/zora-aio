import json

out_file            = ''
data_folder         = 'data'
abi_folder          = 'abi'

bridge_folder       = 'bridge'
mint_folder         = 'mint'
create_nft_folder   = 'create_nft'

with open(f'{out_file}/{data_folder}/{abi_folder}/{bridge_folder}/abi.json') as file:
    ZORA_BRIDGE_ABI = json.load(file)

with open(f'{out_file}/{data_folder}/{abi_folder}/{mint_folder}/abi.json') as file:
    ZORA_MINT_ABI = json.load(file)

with open(f'{out_file}/{data_folder}/{abi_folder}/{create_nft_folder}/erc_721_abi.json') as file:
    ZORA_ERC_721_ABI = json.load(file)
    
with open(f'{out_file}/{data_folder}/{abi_folder}/{create_nft_folder}/erc_1155_abi.json') as file:
    ZORA_ERC_1155_ABI = json.load(file)
    
with open(f'{out_file}/{data_folder}/{abi_folder}/{create_nft_folder}/custom_erc_721_abi.json') as file:
    CUSTOM_ERC_721_ABI = json.load(file)
    
with open(f'{out_file}/{data_folder}/{abi_folder}/mintfun/abi.json') as file:
    MINTFUN_ABI = json.load(file)
    
with open(f'{out_file}/{data_folder}/chains/chains.json') as file:
    CHAIN_DATA = json.load(file)