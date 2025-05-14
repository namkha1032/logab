import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logab')))
from logab import log_init
from tests.utils.error2 import error2_func

# import logging


def supermegaprint():
    logger = log_init()
    logger.debug("nam kha")

def a_very_long_function():
    logger = log_init()
    logger.debug("nam kha")

def cause_error():
    error2_func()
