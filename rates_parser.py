import web3
from web3 import Web3
import requests
import json

providers = {'ethereum': 'https://rpc.ankr.com/eth',
             'bnb': 'https://rpc.ankr.com/bsc',
             'avalanche': 'https://rpc.ankr.com/avalanche',
             'fantom': 'https://rpc.ankr.com/fantom',
             'arbitrum': 'https://rpc.ankr.com/arbitrum',
             'optimism': 'https://rpc.ankr.com/optimism',
             'polygon': 'https://rpc.ankr.com/polygon'
             }

ETHERSCAN_API_KEY = "M89HK8KFR9I27UNGX4ANE2BBZ7QN13GUY7"

address = web3.Web3.toChecksumAddress('0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7')


# this will fetch abi from an explorer given and address
def fetch_abi(address):
    payload = {'module': 'contract',
               'action': 'getabi',
               'address': address,
               'apikey': ETHERSCAN_API_KEY}
    r = requests.get("https://api.etherscan.io/api", params=payload).json()
    abi = json.loads(r['result'])
    return abi


# the amount
def curve_connector(contract):
    contract_abi = fetch_abi(address=contract)
    w3 = Web3(Web3.HTTPProvider(providers['ethereum']))
    contract = w3.eth.contract(address=address, abi=contract_abi)
    coins_and_addresses = []
    for i in range(0, 4):
        try:
            coins_and_addresses.append(contract.functions.coins(i).call())
        except Exception:
            pass
        print(coins_and_addresses)
    # We need to outline exchange rate calculator:


# This function will be used to govern the logic of choosing an exchange rate
def main(address):
    curve_connector(address)


if __name__ == "__main__":
    main(address)
