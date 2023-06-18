import logging

logger = logging.getLogger("to_chatgpt")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
# fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
# fh.setFormatter(formatter)
logger.addHandler(ch)  # screen
# logger.addHandler(fh) # file
