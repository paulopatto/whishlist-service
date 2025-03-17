import logging
import sys

class AppLogger:
    _instance = None

    def __new__(clazz):
        if clazz._instance is None:
            clazz._instance = super(AppLogger, clazz).__new__(clazz)
            clazz._instance.logger = clazz._config_logger()

        return clazz._instance.logger

    @staticmethod
    def  _config_logger():
        logger = logging.getLogger("whishlist-service")
        logger.setLevel(logging.INFO) #TODO: Mudar isso para uma variável de ambiente

        #READ:
        # - https://docs.python.org/3/howto/logging.html
        # - https://www.datadoghq.com/blog/python-logging-best-practices/
        fmt = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        return logger

# Sigleton LOg
AppLog = AppLogger()
