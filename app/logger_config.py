import logging


class LoggerConfig:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


setting = LoggerConfig()
