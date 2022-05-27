"""Module for storing loggers"""

import logging.config
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

file_logger = logging.getLogger("fileLog")
