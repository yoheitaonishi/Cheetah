import configparser
import json
from kucoin.client import Client
import time
import re
from datetime import datetime

from detect_tweet import get_listing_information

RATIO_OF_ORDER_TO_REMIANING = 1

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
# get APIKEY
api_key = inifile.get('settings', 'API_KEY')
api_secret = inifile.get('settings', 'API_SECRET')

# set CuKoin client APIKEY
client = Client(api_key, api_secret)


# tweetから銘柄を抽出する
# TODO: KuCoinの銘柄リストを取得して、tweetの銘柄の取得する
has_listing_info, listed_array = get_listing_information()
cryptocurrencies = open("cryptocurrencies.json")
data = json.load(cryptocurrencies)
crypto_symbols = data.keys()
# 単語毎に配列
listed_word = listed_array.split()
# $マークの削除
for word in listed_word:
    word = word.replace('(', '')
    word = word.replace(')', '')
    word = word.replace('$', '')
    word = word.replace('#', '')
    if word in crypto_symbols:
        order_symbol = word

#order_symbol
order_currency_symbol = order_symbol + "-BTC"

# 発注する銘柄の相場を取得（直近10オーダーの最安値を発注金額とする）
buy_orders = client.get_buy_orders('ETH-BTC', limit=10)
unit_price = 0
for order in buy_orders:
    if unit_price == 0 or unit_price > order[0]: unit_price = order[0]

# アカウント残高を取得
user = client.get_user()

# TODO: BTC以外での発注も可能にする
balances = client.get_coin_balance('BTC')['balance']

# アカウント残高から発注金額を計算
order_amount = balances * RATIO_OF_ORDER_TO_REMIANING

# 買い注文をする
transaction = client.create_order( order_currency_symbol, Client.SIDE_BUY, unit_price, order_amount)

