import json
import os

import pandas as pd
import requests

r = requests.get("https://api.curve.fi/api/getPools/ethereum/main").json()
data = r['data']['poolData']

df = pd.DataFrame(data)
df = df[['name', 'symbol', 'id', 'address', 'coinsAddresses', 'decimals',
          'lpTokenAddress', 'priceOracle', 'implementation',
          'assetTypeName', 'coins', 'usdTotal', 'isMetaPool',
          'usdTotalExcludingBasePool', 'underlyingDecimals',
          'underlyingCoins']]
# df1['coinsAddresses'].str.split(',', expand=True)
print(df['coinsAddresses'].str.)

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
print(df.head(10))

df.to_json(indent=4, orient='split')