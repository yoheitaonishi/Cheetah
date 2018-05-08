## Setup

### Config Files
* Make files
```
cd Cheetah
mkdir config && cd config && touch config.ini
```
* Copy & Paste (order.sh)
```
[settings]
BINANCE_API_KEY = YOUR_BINANCE_API_KEY
BINANCE_API_SECRET = YOUR_BINANCE_API_SECRET
KUCOIN_API_KEY = YOUR_KUCOIN_API_KEY
KUCOIN_API_SECRET = YOUR_KUCOIN_API_SECRET
TWITTER_CK = YOUR_TWITTER_CK
TWITTER_CS = YOUR_TWITTER_CS
TWITTER_AT = YOUR_TWITTER_AT
TWITTER_AS = YOUR_TWITTER_AS
```

### Script Files
* Make files
```
cd Cheetah
mkdir script && cd script && touch order.sh
```
* Copy & Paste (order.sh)
```
#!/bin/sh

cd /var/www/Cheetah/src && python order_on_exchanges.py
```
if python returns errors, you should 'which python' and then replace `pyhon` above file.

