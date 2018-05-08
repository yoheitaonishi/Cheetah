import sys
import configparser
import twitter
import orders

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
binance_api_key = inifile.get('settings', 'BINANCE_API_KEY')
binance_api_secret = inifile.get('settings', 'BINANCE_API_SECRET')
kucoin_api_key = inifile.get('settings', 'KUCOIN_API_KEY')
kucoin_api_secret = inifile.get('settings', 'KUCOIN_API_SECRET')

EXCHANGE_TYPE = ["Binance", "KuCoin"]
EXCHANGE_API_KEYS = [
    {"Binance": {"api_key": binance_api_key, "api_secret": binance_api_secret},
    {"KuCoin":  {"api_key": kucoin_api_key,  "api_secret": kucoin_api_secret}
    ]


has_listing_info, listed_array = twitter.detect_listing_tweet.get_listing_information()
if not has_listing_info: 
    orders.order_logging.logger.info("There is no tweet about listing")
    sys.exit()

for exchange in EXCHANGE_TYPE:
    trade = orders.order.apply(EXCHANGE_API_KEYS[exchange]["api_key"], EXCHANGE_API_KEYS[exchange]["api_secret"], has_listing_info, listed_array)
