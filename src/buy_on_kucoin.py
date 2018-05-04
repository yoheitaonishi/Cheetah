import configparser
import json
from kucoin.client import Client
import time
import re
from datetime import datetime
import urllib.request, urllib.error
from detect_tweet import get_listing_information

RATIO_OF_ORDER_TO_REMIANING = 1

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
# set KuCoin client APIKEY
kucoin_api_key = inifile.get('settings', 'KUCOIN_API_KEY')
kucoin_api_secret = inifile.get('settings', 'KUCOIN_API_SECRET')
kucoin_client = Client(kucoin_api_key, kucoin_api_secret)



#################### KuCoin ####################

def apply_kucoin_bot():
    has_listing_info, listed_array = get_listing_information()
    if not has_listing_info: return False
    order_symbol = get_symbol_from_list(listed_array)
    if not order_symbol: return False
    order_currency_symbol = order_symbol + "-BTC"
    #print(order_currency_symbol)
    unit_price = get_unit_price_of_tx_on_kucoin(order_currency_symbol)
    order_on_kucoin(kucoin_client, unit_price)

# kucoinの取引可能銘柄のsymbolを取得する
def get_enable_symboles_on_kucoin():
    request = urllib.request.urlopen('https://api.kucoin.com/v1/market/open/symbols').read()
    decoded_request = request.decode('utf8').replace("'", '"')
    json_request = json.loads(decoded_request) 
    kucoin_symbols = []
    for data in json_request["data"]:
        kucoin_symbols.append(data['coinType'])
    return kucoin_symbols

# 上場tweetからsymbolを取得
def get_symbol_from_list(listed_array):
    kucoin_symbols = get_enable_symboles_on_kucoin()
    if not listed_array: 
        print("上場に関するTweetはありませんでした。")
    # 優先順に格納されているので1番目の情報を優先
    listed_word = listed_array[0].split()
    # 特定文字の削除
    order_symbol = ""
    for word in listed_word:
        word = word.replace('(', '')
        word = word.replace(')', '')
        word = word.replace('$', '')
        word = word.replace('#', '')
        if word in kucoin_symbols:
            order_symbol = word
    if not order_symbol: 
        print("KuCoinで$" + order_symbol + "は取引できません...")
    return order_symbol

# 発注する銘柄の相場を取得（直近10オーダーの最安値を発注金額とする）
def get_unit_price_of_tx_on_kucoin(order_currency_symbol):
    buy_orders = kucoin_client.get_buy_orders(order_currency_symbol, limit=10)
    unit_price = 0
    for order in buy_orders:
        if unit_price == 0 or unit_price > order[0]: unit_price = order[0]
    if unit_price == 0: print("相場情報を取得できませんでした...")
    return unit_price


def order_on_kucoin(kucoin_client, unit_price):
    # アカウント残高を取得
    user = kucoin_client.get_user()
    # TODO: BTC以外での発注も可能にする
    balances = kucoin_client.get_coin_balance('BTC')['balance']
    # アカウント残高から発注金額を計算
    order_amount = balances * RATIO_OF_ORDER_TO_REMIANING
    # 買い注文をする
    transaction = kucoin_client.create_order( order_currency_symbol, Client.SIDE_BUY, unit_price, order_amount)
    if "orderOid" in transaction: print("発注が完了しました！")

#################### KuCoin ####################
