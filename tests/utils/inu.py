from logab import log_context, log_init

with log_context():
    for i in range(100):
        logger = log_init()
        logger.debug(i)