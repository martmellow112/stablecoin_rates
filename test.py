from web3 import Web3
import requests
import json


rpcs = {'ethereum': 'https://rpc.ankr.com/eth',
             'bnb': 'https://rpc.ankr.com/bsc',
             'avalanche': 'https://rpc.ankr.com/avalanche',
             'fantom': 'https://rpc.ankr.com/fantom',
             'arbitrum': 'https://rpc.ankr.com/arbitrum',
             'optimism': 'https://rpc.ankr.com/optimism',
             'polygon': 'https://rpc.ankr.com/polygon'
             }

w3 = Web3(Web3.HTTPProvider(rpcs['ethereum']))

ETHERSCAN_API_KEY = "M89HK8KFR9I27UNGX4ANE2BBZ7QN13GUY7"

def fetch_abi(address):
    address = Web3.toChecksumAddress(address)
    payload = {'module': 'contract',
               'action': 'getabi',
               'address': address,
               'apikey': ETHERSCAN_API_KEY
               }
    r = requests.get("https://api.etherscan.io/api", params=payload).json()
    abi = json.loads(r['result'])
    return abi

def curve_connector(pool):
    pool = w3.eth.contract(address=pool,abi=fetch_abi(pool)).functions
    print(pool.get_dy(1,2,1_000_000_000).call())

if __name__ == '__main__':
    curve_connector('0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7')