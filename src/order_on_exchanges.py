import sys
import configparser
import twitter
import orders

# load config
inifile = configparser.ConfigParser()
inifile.read('../config/config.ini', 'UTF-8')
 
kucoint_api_key = inifile.get('settings', 'KUCOIN_API_KEY')
kucoint_api_secret = inifile.get('settings', 'KUCOIN_API_SECRET')
binance_api_key = inifile.get('settings', 'BINANCE_API_KEY')
binance_api_secret = inifile.get('settings', 'BINANCE_API_SECRET')

EXCHANGE_TYPE = ["Binance", "KuCoin"]


has_listing_info, listed_array = twitter.detect_listing_tweet.get_listing_information()
if not has_listing_info: 
    orders.order_logging.logger.info("上場のtweetはありませんでした...")
    sys.exit()

# Kucoin
#kucoin_trade = orders.order_on_kucoin.apply_on_kucoin(has_listing_info, listed_array)
kucoin_trade = orders.order_on_binance.apply_on_kucoin(has_listing_info, listed_array)

