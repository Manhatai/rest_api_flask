import logging

logging.basicConfig(filename="logs/logs.log",
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)
