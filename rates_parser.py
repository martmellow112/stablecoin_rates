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
w3 = Web3(Web3.HTTPProvider(providers['ethereum']))

ETHERSCAN_API_KEY = "M89HK8KFR9I27UNGX4ANE2BBZ7QN13GUY7"

address = web3.Web3.toChecksumAddress('0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7')


# this will fetch abi from an explorer given an address
def fetch_abi(address):
    payload = {'module': 'contract',
               'action': 'getabi',
               'address': address,
               'apikey': ETHERSCAN_API_KEY
               }
    r = requests.get("https://api.etherscan.io/api", params=payload).json()
    abi = json.loads(r['result'])
    return abi


def get_decimals(token_address):
    token_abi = fetch_abi(address=token_address)
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)
    decimals = token_contract.functions.decimals().call()
    print(decimals)
    return decimals

def curve_connector(pool):
    # Get ABI of the pool contract in order to interact with it
    contract_abi = fetch_abi(address=pool)
    contract = w3.eth.contract(address=address, abi=contract_abi)
    coins_and_addresses = []

    for i in range(0, 4):
        try:
            coins_and_addresses.append(contract.functions.coins(i).call())
        except Exception:
            pass

    print(coins_and_addresses)


# This function will be used to govern the logic of choosing an exchange rate
def main():
    curve_connector(address)
    get_decimals('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')

if __name__ == "__main__":
    main()
