from logab import log_init


def critical_function():
    logger = log_init()
    logger.critical(f"Some critical message")