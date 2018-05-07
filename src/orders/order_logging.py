import logging



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
