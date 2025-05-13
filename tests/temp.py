from logab import log_init

# import logging


def supermegaprint(idx):
    logger = log_init()
    # logger = log_init()
    logger.debug("nam kha")
    if idx == 3:
        with open('temp.txt', 'r') as file:
            pass