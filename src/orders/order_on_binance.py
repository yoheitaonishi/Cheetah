# coding:utf-8

import configparser
import json
from binance.client import Client
from binance.enums import *
import urllib.request, urllib.error
import math

RATIO_OF_ORDER_TO_REMIANING = 1
CURRENCY_PAIR = "BTC"

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
kucoin_client = Client(api_key, api_secret)



def apply_on_kucoin(has_listing_info, listed_array):
    order_symbol = get_symbol_from_list(listed_array)
    if not order_symbol: 
        return False
    order_currency_symbol = order_symbol
    #print(order_currency_symbol)
    unit_price = get_unit_price_of_tx_on_kucoin(order_currency_symbol)
    order_on_kucoin(kucoin_client, order_currency_symbol, unit_price)

# kucoinの取引可能銘柄のsymbolを取得する
def get_enable_symboles_on_kucoin():
    symbols_data = kucoin_client.get_products()["data"]
    kucoin_symbols = []
    for data in symbols_data:
        kucoin_symbols.append(data['symbol'])
    return kucoin_symbols

# 上場tweetからsymbolを取得
def get_symbol_from_list(listed_array):
    kucoin_symbols = get_enable_symboles_on_kucoin()
    # 優先順に格納されているので1番目の情報を優先
    first_listed_sentence = listed_array[0]
    # 括弧()が付いている単語のみ切り出して文末に追加しておく
    fixed_listed_sentence = first_listed_sentence.replace('(', ' ').replace(')', ' ')
    listed_word = fixed_listed_sentence.split()
    # 特定文字の削除
    order_symbol = ""
    for word in listed_word:
        word = word.replace('$', '')
        word = word.replace('#', '')
        word = word + CURRENCY_PAIR
        if word in kucoin_symbols:
            order_symbol = word
    if not order_symbol: 
        logger.info("Binanceで取引できる通貨はありません...")
    return order_symbol

# 発注する銘柄の決済情報を取得（直近10の決済済買い注文の最高値+2%を発注金額とする）
def get_unit_price_of_tx_on_kucoin(order_currency_symbol):
    print(order_currency_symbol)
    buy_orders = kucoin_client.get_order_book(symbol = order_currency_symbol)
    unit_prices = []
    unit_price = 0
    for order in buy_orders["bids"]:
        unit_prices.append(order[0])
    unit_price = max(unit_prices)
    if unit_price == 0: logger.info("相場情報を取得できませんでした...")
    unit_price = float(unit_price) * 1.02
    return unit_price

def order_on_kucoin(kucoin_client, order_currency_symbol, unit_price):
    # TODO: BTC以外での発注も可能にする
    balances = kucoin_client.get_asset_balance(asset = CURRENCY_PAIR)['free']
    # アカウント残高から発注金額を計算
    order_amount = float(balances) * RATIO_OF_ORDER_TO_REMIANING
    # 買い注文をする
    buy_order_amount = math.floor(order_amount / unit_price)
    i = 0
    while i < 4: 
        transaction = kucoin_client.order_market_buy(symbol = order_currency_symbol, quantity = buy_order_amount/4)
        i += 1
        if "orderId" in transaction: 
            logger.info(order_currency_symbol + "を" + "単価" + str(unit_price) + "で" + str(buy_order_amount) + "のBUY注文が完了しました！")
        else
            logger.error([]order_currency_symbol + "を" + "単価" + str(unit_price) + "で" + str(buy_order_amount) + "のBUY注文完了しませんでした...")

