#!/bin/sh

# KuCoin production
cd /var/www/Cheetah/src && /home/ec2-user/.pyenv/versions/anaconda3-5.1.0/bin/python apply_exchanges.py
# KuCoin dev
#cd /Users/yoheitaonishi/block_chain/bot/Cheetah/src && python apply_exchanges.py

