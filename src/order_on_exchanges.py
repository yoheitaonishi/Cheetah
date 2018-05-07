import sys
import twitter
import orders



has_listing_info, listed_array = twitter.detect_listing_tweet.get_listing_information()
if not has_listing_info: 
    orders.order_logging.logger.info("上場のtweetはありませんでした...")
    sys.exit()

# Kucoin
kucoin_trade = orders.order_on_kucoin.apply_on_kucoin(has_listing_info, listed_array)
kucoin_trade = orders.order_on_binance.apply_on_binance(has_listing_info, listed_array)

