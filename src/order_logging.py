import logging

logger = logging.getLogger('OrderLogging')
logger.setLevel(10)
fh = logging.FileHandler('../log/order.log')
logger.addHandler(fh)
sh = logging.StreamHandler()
logger.addHandler(sh)
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
