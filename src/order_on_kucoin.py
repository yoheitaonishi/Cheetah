# OSXでは2行目を削除しないとencodeエラーが発生する
# coding:utf-8

import configparser
import json
from kucoin.client import Client
import time
import re
from datetime import datetime
import urllib.request, urllib.error
from detect_tweet import get_listing_information
import sys
import logging
import math
from statistics import mean, median,variance,stdev
import regex

RATIO_OF_ORDER_TO_REMIANING = 1

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
# set KuCoin client APIKEY
kucoin_api_key = inifile.get('settings', 'KUCOIN_API_KEY')
kucoin_api_secret = inifile.get('settings', 'KUCOIN_API_SECRET')
kucoin_client = Client(kucoin_api_key, kucoin_api_secret)

# ログの出力名を設定
logger = logging.getLogger('LoggingTest')
# ログレベルの設定
logger.setLevel(10)
# ログのファイル出力先を設定
fh = logging.FileHandler('../log/order.log')
logger.addHandler(fh)
# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)
# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)



def apply_on_kucoin():
    has_listing_info, listed_array = get_listing_information()
    if not has_listing_info: 
        logger.info("上場のtweetはありませんでした...")
        sys.exit()
    order_symbol = get_symbol_from_list(listed_array)
    if not order_symbol: 
        sys.exit()
    order_currency_symbol = order_symbol + "-BTC"
    #print(order_currency_symbol)
    unit_price = get_unit_price_of_tx_on_kucoin(order_currency_symbol)
    order_on_kucoin(kucoin_client, order_currency_symbol, unit_price)

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
    # 優先順に格納されているので1番目の情報を優先
    first_listed_sentence = listed_array[0]
    # 括弧()が付いている単語のみ切り出して文末に追加しておく
    #fixed_listed_sentence = regex.search(r"\(.+?\)", first_listed_sentence).replace('(', ' ').replace(')', ' ')
    fixed_listed_sentence = first_listed_sentence.replace('(', ' ').replace(')', ' ')
    listed_word = fixed_listed_sentence.split()
    # 特定文字の削除
    order_symbol = ""
    print(listed_word)
    for word in listed_word:
        word = word.replace('$', '')
        word = word.replace('#', '')
        print(word)
        if word in kucoin_symbols:
            order_symbol = word
    if not order_symbol: 
        logger.info("KuCoinで$" + order_symbol + "は取引できません...")
    return order_symbol

# 発注する銘柄の決済情報を取得（直近10の決済済買い注文の最高値+2%を発注金額とする）
def get_unit_price_of_tx_on_kucoin(order_currency_symbol):
    buy_orders = kucoin_client.get_buy_orders(order_currency_symbol, limit=10)
    unit_prices = []
    unit_price = 0
    for order in buy_orders:
        unit_prices.append(order[0])
    unit_price = max(unit_prices)
    if unit_price == 0: logger.info("相場情報を取得できませんでした...")
    unit_price = unit_price * 1.02
    #print(unit_price)
    return unit_price

def order_on_kucoin(kucoin_client, order_currency_symbol, unit_price):
    # アカウント残高を取得
    user = kucoin_client.get_user()
    # TODO: BTC以外での発注も可能にする
    balances = kucoin_client.get_coin_balance('BTC')['balance']
    # アカウント残高から発注金額を計算
    order_amount = balances * RATIO_OF_ORDER_TO_REMIANING
    # 買い注文をする
    buy_order_amount =  math.floor(order_amount / unit_price)
    transaction = kucoin_client.create_buy_order( order_currency_symbol, unit_price, buy_order_amount)
    if "orderOid" in transaction: 
        logger.info(order_currency_symbol + "を" + "単価" + str(unit_price) + "で" + str(buy_order_amount) + "のBUY注文が完了しました！")


