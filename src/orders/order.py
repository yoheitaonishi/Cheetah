# coding:utf-8

import configparser
import json
from kucoin.client import Client
from binance.client import Client
import urllib.request, urllib.error
import math

RATIO_OF_ORDER_TO_REMIANING = 1
CURRENCY_PAIR = "BTC"
BUY_ORDER_PRICE_RETIO = 1.02
ORDER_RESPONSE = {
    "Binance": "orderId",
    "KuCoin":  "orderOid"
}
DEVIDED_MARKET_ORDER = 4



def apply_on_kucoin(api_key, api_secret, has_listing_info, listed_array, exchange_type):
    client = Client(api_key, api_secret)
    order_symbol = get_symbol_from_list(listed_array)
    if not order_symbol: 
        return False
    order_currency_symbol = order_symbol + "-" + CURRENCY_PAIR
    unit_price = get_unit_price_of_tx(client, order_currency_symbol)
    order(client, order_currency_symbol, unit_price)

# Get enable exchange pairs
def get_enable_symboles_on_market(exchange_type):
    symbols = []
    if exchange_type == "Binance":
        symbols_data = client.get_products()["data"]
        for data in symbols_data:
            symbols.append(data['symbol'])
    elif exchange_type == "KuCoin":
        request = urllib.request.urlopen('https://api.kucoin.com/v1/market/open/symbols').read()
        decoded_request = request.decode('utf8').replace("'", '"')
        json_request = json.loads(decoded_request) 
        for data in json_request["data"]:
            symbols.append(data['coinType'])
    return symbols

# Get listing currency symbol from tweet
def get_symbol_from_list(listed_array, exchange_type):
    symbols = get_enable_symboles_on_market(exchage_type)
    # Get first currency symbol from tweet
    # because symbol list is sorted by priority
    first_listed_sentence = listed_array[0]
    # Append inner word of ()
    # because currency symbol is often in it
    fixed_listed_sentence = first_listed_sentence.replace('(', ' ').replace(')', ' ')
    listed_word = fixed_listed_sentence.split()
    # Delete supecified words
    order_symbol = ""
    for word in listed_word:
        word = word.replace('$', '')
        word = word.replace('#', '')
        if exchange_type == "Binance": word = word + CURRENCY_PAIR
        if word in symbols:
            order_symbol = word
            if exchange_type == "KuCoin": word + '-' + CURRENCY_PAIR
    if not order_symbol: 
        logger.info("Tweet doesn't have information of currency listing on " exchange_type)
    return order_symbol

# 発注する銘柄の決済情報を取得（直近10の決済済買い注文の最高値+2%を発注金額とする）
def get_unit_price_of_tx(client, order_currency_symbol, exchange_type):
    if exchange_type == "Binance":
        buy_orders_from_api = client.get_order_book(symbol = order_currency_symbol)
        buy_orders = buy_orders_from_api["bids"]
    elif exchange_type == "KuCoin":
        buy_orders = client.get_buy_orders(order_currency_symbol, limit=10)
    unit_prices = []
    unit_price = 0
    for order in buy_orders:
        # API response has unit price at first value of list
        unit_prices.append(order[0])
    unit_price = max(unit_prices)
    if unit_price == 0: logger.info("There is no information about unit price on market")
    if exchange_type == "Binance": unit_price = float(unit_price)
    unit_price = unit_price * BUY_ORDER_PRICE_RETIO
    #print(unit_price)
    return unit_price

def get_balance_information(client, exchange_type):
    if exchange_type == "Binance":
        balances_from_api = client.get_asset_balance(asset = CURRENCY_PAIR)['free']
        balances = float(balances_from_api)
    elif exchange_type == "KuCoin":
        balances = client.get_coin_balance(CURRENCY_PAIR)['balance']
    return balances

def order(client, order_currency_symbol, unit_price, exchange_type):
    balance = get_balance_information(client, exchange_type)
    # Calculate order price
    order_amount = balances * RATIO_OF_ORDER_TO_REMIANING
    # Order BUY currency
    buy_order_amount = math.floor(order_amount / unit_price)
    if exchange_type == "Binance":
        """
        You can use market order on Binance
        but you have to calculate quantity of order
        so order is just devided by DEVIDED_MARKET_ORDER
        because you can't order if calculated quantity is not enough
        """
        i = 0
        while i < DEVIDED_MARKET_ORDER: 
            transaction = client.order_market_buy(symbol = order_currency_symbol, quantity = buy_order_amount / DEVIDED_MARKET_ORDER)
            i += 1
        order_response = ORDER_RESPONSE["Binance"]
    elif exchange_type == "KuCoin":
        transaction = client.create_buy_order( order_currency_symbol, unit_price, buy_order_amount)
        order_response = ORDER_RESPONSE["KuCoin"]
    if order_response in transaction: 
        logger.info("Cheetah ordered BUY "order_currency_symbol + str(buy_order_amount) + "@" + str(unit_price))
    else
        logger.error("[ERROR!!] Cheetah couldn't order BUY "order_currency_symbol + str(buy_order_amount) + "@" + str(unit_price))
