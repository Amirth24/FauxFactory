"""
Config Logging

"""

import logging
from .config import LoggingConfig

LOG_LEVELS: list[tuple[str, int]] = [
    ("CRITICAL", logging.CRITICAL),
    ("ERROR", logging.ERROR),
    ("WARNING", logging.WARNING),
    ("INFO", logging.INFO),
    ("DEBUG", logging.DEBUG),
    ("NOTSET", logging.NOTSET),
    ("APPFLOW", 25),  # Custom log level between INFO and WARNING
]


def get_system_logger() -> logging.Logger:
    """
    Get a logger for system-level logs.
    """

    logger = logging.getLogger("system")
    logger.setLevel(logging.INFO)
    return logger


def setup_logging(config: LoggingConfig):
    """
    Set up logging configuration to only show logs from flows.flow
    """

    # setup global logger
    logging.basicConfig(
        level=config.level,
        format=config.line_format,
        handlers=[logging.StreamHandler()],
    )

    for level_name, level_value in LOG_LEVELS:
        logging.addLevelName(level_value, level_name)

    for logger_cfg in config.loggers:
        logger = logging.getLogger(logger_cfg.name)
        logger.setLevel(getattr(logging, logger_cfg.level.upper(), logging.INFO))
