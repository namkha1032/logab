from logab import log_context, log_init


def myfunc():
    # with log_context(log_file='app2.log'):
        logger = log_init()
        logger.debug(123)