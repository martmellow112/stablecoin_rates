from web3 import Web3
import requests
import json
import keys

rpc = dict(ethereum="https://rpc.ankr.com/eth", bnb="https://rpc.ankr.com/bsc",
           avalanche="https://rpc.ankr.com/avalanche", fantom="https://rpc.ankr.com/fantom",
           arbitrum="https://rpc.ankr.com/arbitrum", optimism="https://rpc.ankr.com/optimism",
           polygon="https://rpc.ankr.com/polygon")

w3 = Web3(Web3.HTTPProvider(rpc["ethereum"]))

ETHERSCAN_API_KEY = keys.etherscan_api_key

# This will fetch abi from an explorer given an address
def fetch_abi(address):
    address = Web3.toChecksumAddress(address)
    payload = {"module": "contract",
               "action": "getabi",
               "address": address,
               "apikey": ETHERSCAN_API_KEY
               }
    r = requests.get("https://api.etherscan.io/api", params=payload).json()
    abi = json.loads(r["result"])
    return abi


def get_token_decimals(token_address):
    """
    This function assumes that the token is ERC20 standard.
    """
    # Load ERC20 ABI
    erc20_abi = json.load(open("erc20.abi.json"))
    decimals = w3.eth.contract(address=token_address,abi=erc20_abi).functions.decimals().call()
    return decimals


def curve_connector(pool, token_in, token_out, amount_in) -> int:
    """
    :param pool: Address of the pool where the swap should happen
    :param token_in: Address of the token to be swapped (outgoing) -->
    :param token_out: Address of the token to be received (incoming) <--
    :param amount_in: Size of the swap in standard units (this will be converted into the required decimal amount)
    :return: int() output of exchange rate
    """

    # Transform to checksum values, for reasons i do not understand right now
    pool = Web3.toChecksumAddress(pool)
    token_in = Web3.toChecksumAddress(token_in)
    token_out = Web3.toChecksumAddress(token_out)

    # Get ABI of the pool contract in order to interact with it.
    pool = w3.eth.contract(address=pool, abi=fetch_abi(pool)).functions

    # Transform human-readable swap amount into correct decimal representation
    amount_in_dec = amount_in * 10 ** (get_token_decimals(token_in))

    # Make a list of tokens, which could be exchanged in the pool. Length of list is an arbitrary number.
    # Typically, curve pools do not have more than 4 tokens to be exchanged, hence the value in the list.

    coins = []
    for i in range(0, 4):
        try:
            coins.append(pool.coins(i).call())
        except Exception:
            pass

    # This function will be used to calculate the given exchange rate.
    if token_in and token_out in coins:
        print(f"Exchange rate can be calculated.\n")
        amount_out_dec = pool.get_dy(coins.index(token_in),
                                     coins.index(token_out),
                                     amount_in_dec).call()
        amount_out = amount_out_dec / 10 ** get_token_decimals(token_out)
        exchange_rate  = amount_out/amount_in
        print(f"Swap of {amount_in:,.2f} of token {coins.index(token_in)} will yield "
              f"{amount_out:,.2f} of token {coins.index(token_out)}.\n"
              f"Exchange rate is {exchange_rate:,.5f}")
        return exchange_rate
    else:
        print('Exchange rate cannot be calculated. Check if both tokens are contained in the pool.')


def uniswap_v3_connector(quoter, token_in, token_out, amount_in) -> int:
    """
    :param router: Address of the router, which is a periphery contract used to output price for swaps
    :param token_in: Address of the token to be swapped (outgoing) -->
    :param token_out: Address of the token to be received (incoming) <--
    :param amount_in: Size of the swap in standard units (this will be converted into the required decimal amount)
    :return: int() output of exchange rate
    """

    # Transform to checksum values, for reasons i do not understand right now
    pool = Web3.toChecksumAddress(router)
    token_in = Web3.toChecksumAddress(token_in)
    token_out = Web3.toChecksumAddress(token_out)





def main():
    # curve_connector(pool='0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7',
    #                 token_in='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    #                 token_out='0xdAC17F958D2ee523a2206206994597C13D831ec7',
    #                 amount_in=100_000_000)

    uniswap_v3_connector(quoter="0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7",
                         token_in='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                         token_out='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                         amount_in=100_000_000)


if __name__ == "__main__":
    main()
