from web3 import Web3
import requests
import json
import keys
import pandas as pd


rpc = dict(ethereum="https://rpc.ankr.com/eth", bnb="https://rpc.ankr.com/bsc",
           avalanche="https://rpc.ankr.com/avalanche", fantom="https://rpc.ankr.com/fantom",
           arbitrum="https://rpc.ankr.com/arbitrum", optimism="https://rpc.ankr.com/optimism",
           polygon="https://rpc.ankr.com/polygon")

w3 = Web3(Web3.HTTPProvider(rpc["ethereum"]))
ETHERSCAN_API_KEY = keys.ETHERSCAN_API_KEY


def fetch_abi(address: str):
    """
    This will fetch abi from an explorer given an address.
    """
    address = Web3.toChecksumAddress(address)
    payload = {"module": "contract",
               "action": "getabi",
               "address": address,
               "apikey": ETHERSCAN_API_KEY
               }
    r = requests.get("https://api.etherscan.io/api", params=payload).json()
    abi = json.loads(r["result"])
    
    return abi

def fetch_symbol(address: str) -> str:
    '''
    This will fetch the symbol of an ERC20 token.
    '''
    erc20_abi = json.load(open("erc20.abi.json"))
    address = Web3.toChecksumAddress(address)
    symbol = w3.eth.contract(address=address,abi=erc20_abi).functions.symbol().call()
    
    return symbol


def get_decimals(token_address: str) -> int:
    """
    This function assumes that the token is ERC20 standard.
    """
    # Load ERC20 ABI
    erc20_abi = json.load(open("erc20.abi.json"))
    token_address = Web3.toChecksumAddress(token_address)
    decimals = w3.eth.contract(address=token_address,abi=erc20_abi).functions.decimals().call()
    
    return decimals


def curve_connector(token_in: str, token_out: str, amount_in: int) -> int:
    '''
    :param token_in: address of the token to be swapped (outgoing) -->
    :param token_out: Address of the token to be received (incoming) <--
    :param amount_in: Size of the swap in standard units (this will be converted into the required decimal amount)
    '''
    # Swap router address, found randomly via google search.
    # Current contract from https://curve.readthedocs.io/registry-exchanges.html#swapping-tokens is apparently old
    swap_router = Web3.toChecksumAddress("0x99a58482bd75cbab83b27ec03ca68ff489b5788f")
    token_in = Web3.toChecksumAddress(token_in)
    token_out = Web3.toChecksumAddress(token_out)

    swap_router = w3.eth.contract(address=swap_router, abi=fetch_abi(swap_router)).functions
    decimals = get_decimals(token_in)
    exchange_rate = swap_router.get_best_rate(token_in, token_out, amount_in * 10 ** decimals).call()[1] \
        / (amount_in * 10 ** get_decimals(token_out))

    print(f"Exchange rate for {amount_in:,.0f} {fetch_symbol(token_in)} "
          f"-> {fetch_symbol(token_out)} on Curve: {exchange_rate}.")
    return exchange_rate


def uniswap_v3_connector(token_in: str, token_out: str, amount_in: int, fee: int) -> int:
    """
    :param token_in: Address of the token to be swapped (outgoing) -->
    :param token_out: Address of the token to be received (incoming) <--
    :param amount_in: Size of the swap in standard units (this will be converted into the required decimal amount)
    :param fee: fee
    :return: output of exchange rate
    """

    # Transform to checksum value
    quoter = Web3.toChecksumAddress("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")
    token_in = Web3.toChecksumAddress(token_in)
    token_out = Web3.toChecksumAddress(token_out)

    # We need to access Quoter smart contract in order to obtain the current price of the tokens
    quoter = w3.eth.contract(address=quoter, abi=fetch_abi(quoter)).functions

    amount_in_dec = amount_in * 10 ** get_decimals(token_in)
    amount_out_dec = quoter.quoteExactInputSingle(token_in, token_out, fee, amount_in_dec, 0).call()
    amount_out = amount_out_dec / 10 ** get_decimals(token_out)
    exchange_rate = amount_out / amount_in

    print(f"Exchange rate for {amount_in:,.0f} {fetch_symbol(token_in)} -> "
          f"{fetch_symbol(token_out)} on Uniswap V3 {fee / 1e5:.2%}: {exchange_rate}.")
    return exchange_rate


def main():
    def to_table():
        token_in = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        token_out = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
        amounts = [10_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]

        rates_array = []
        for amount in amounts:
            print(f"Printing exchange rates for amount: ${amount:,.0f}")
            rates_array.append(list([amount, curve_connector(token_in, token_out, amount),
                                    uniswap_v3_connector(token_in, token_out, amount, 100),
                                    uniswap_v3_connector(token_in, token_out, amount, 500)]))
            print(f"")
        
        # Creating an array
        df = pd.DataFrame(rates_array, columns=["amount", "curve", "uniswap_v3 0.1%", "uniswap_v3 0.5%"])
        print(df)

    to_table()

if __name__ == "__main__":
    main()
