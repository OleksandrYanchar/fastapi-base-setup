import logging
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = os.getenv("ROOT")

def setup_logger(ROOT):
    LOG_FILENAME = os.getenv("LOG_FILENAME", "app.log")
    LOG_FILE = f"{ROOT}/{LOG_FILENAME}"

    log_format = "%(asctime)s %(levelname)-8s %(message)s  file: %(pathname)s  %(funcName)s line %(lineno)d"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        filename=LOG_FILE, level=logging.ERROR, format=log_format, datefmt=date_format
    )

    # Example logging messages
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")
