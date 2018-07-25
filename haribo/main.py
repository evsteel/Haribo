import sys
sys.path.append('./luffy')

import logging
import logging.handlers
import datetime

LOG_FORMAT = "[%(levelname)s][%(name)s]%(asctime)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger(__name__)

file_handler = logging.handlers.TimedRotatingFileHandler('logs/haribo_main.log',
                                                         when='midnight',
                                                         interval=1,
                                                         atTime=datetime.time(0, 0, 0, 0,))
file_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))
logger.addHandler(file_handler)

if __name__ == "__main__":
    import luffy.main as luffy_main
    luffy_main.main_loop()
    pass