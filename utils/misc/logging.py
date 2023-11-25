import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname:<8} {message}",
    style="{",
)


INFO = logging.INFO
logger = logging.Logger("logger")
