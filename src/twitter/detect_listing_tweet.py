#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import sys
import json
import oauth2 as oauth
import datetime

# Load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
# Get Twitter API_KEYS
CK = inifile.get('settings', 'CK')  # Consumer Key
CS = inifile.get('settings', 'CS')  # Consumer Secret
AT = inifile.get('settings', 'AT')  # Access Token
AS = inifile.get('settings', 'AS')  # Accesss Token Secert

### twitter ID (優先度順に書いておく)
#BINANCE = "877807935493033984"
BITHUMB = "908496633196814337"
BITFINEX = "886832413"
OKEX = "867617849208037377"
#yoheitaonishi = "3012996895"
BINANCE =      "3012996895"
#BITHUMB = "3012996895"
#BITFINEX = "3012996895"
#OKEX = "3012996895"
#USER_IDS = [BINANCE, BITHUMB, BITFINEX, OKEX, yoheitaonishi]
USER_IDS = [BINANCE, BITHUMB, BITFINEX, OKEX]

# Listing sentence twitter
BINANCE_TW = "#Binance Lists"
BITHUMB_TW = "We're listing"
BITFINEX_TW = "We are pleased to introduce trading for"
#OKEX_TW = [] There is no format about listing 
 


def get_listing_information():
    client = define_client_proc()
    tw_array = get_tweets_proc(client, USER_IDS)
    one_minute_tw = []
    listed_array= []
    has_listing_info = False
    if tw_array:
        one_minute_tw = get_one_minute_tweet(tw_array)
    if one_minute_tw:
        has_listing_info, listed_array = get_listing_tweet(one_minute_tw)
    return has_listing_info, listed_array
 
def define_client_proc():
    consumer = oauth.Consumer(key=CK, secret=CS)
    access_token = oauth.Token(key=AT, secret=AS)
    client = oauth.Client(consumer, access_token)
    return client

def get_tweets_proc(client, user_ids):
    # Hypothesis is twitter account wouldn't tweet more than three times per a minute
    nnx = 2
    tw_array = []
    for user_id in USER_IDS:
        url_base = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id="
        url = url_base + user_id + "&count=" + str(nnx)
        response, data = client.request(url)
        if response.status == 200:
            json_str = data.decode('utf-8')
            tw_array.extend(json.loads(json_str))
        else:
            sys.stderr.write("*** error *** get_ids_proc ***\n")
            sys.stderr.write("Error: %d\n" % response.status)
    return  tw_array

def get_one_minute_tweet(tw_array):
    one_minute_tw = []
    end_tweet_term = datetime.datetime.now(datetime.timezone.utc)
    start_tweet_term = (end_tweet_term - datetime.timedelta(minutes=1))
    for tw in tw_array:
        tw_datetime = datetime.datetime.strptime(tw["created_at"], '%a %b %d  %H:%M:%S %z %Y')
        if start_tweet_term <= tw_datetime and tw_datetime < end_tweet_term:
            user_id = tw['user']['id']
            one_minute_tw.append({user_id: tw["text"]})
    return one_minute_tw
    
def get_listing_tweet(one_minute_tw):
    listed_array = []
    for tw in one_minute_tw:
        for key in tw.keys():
            if key == int(BINANCE):
                if BINANCE_TW in tw.get(key): listed_array.append(tw.get(key))
            elif key == int(BITHUMB):
                if BITHUMB_TW in tw.get(key): listed_array.append(tw.get(key))
            elif key == int(BITFINEX):
                if BITFINEX_TW in tw.get(key): listed_array.append(tw.get(key))
            #elif key == OKEX:
                #if OKEX_TW in tw.get(key): listed_array.append({key: tw.get(key)})
    
    has_listing_info = False
    if listed_array:
        has_listing_info = True
    
    return has_listing_info, listed_array
