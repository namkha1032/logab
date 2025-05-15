import os
import sys

from logab import log_init
from tests.utils.error import error_func

# import logging


def supermegaprint():
    logger = log_init()
    logger.debug("nam kha")

def a_very_long_function():
    logger = log_init()
    logger.debug("nam kha")

def cause_error():
    error_func()
