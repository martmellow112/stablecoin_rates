import web3

from rates_parser import fetch_abi
from web3 import Web3

w3 = Web3(web3.HTTPProvider('https://rpc.ankr.com/eth'))

def get_decimals(token):
    contract_abi = fetch_abi(address=token)
    token_contract = w3.eth.contract(address=token, abi=contract_abi)
    decimals = token_contract.functions()