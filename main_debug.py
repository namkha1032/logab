import logging
import os
import sys
import time

from critical import critical_function
from logab import log_init, log_wrap
from new_print import override_print
from tests.temp import a_very_long_function, supermegaprint
from tests.utils.error import error_func
from tests.utils.use import newfunc


def print_main():
    logger = log_init()
    logger.warning("In function of main.py")
def exec_program():
    logger = log_init()
    for idx, char in enumerate(range(100)):
        # supermegaprint(idx)
        time.sleep(1)
        logger.info(f"idx: {idx}")
        if idx == 1:
            print_main()
        if idx == 2:
            supermegaprint()
            logger.warning(f"Some warn | ing message")
        if idx == 3:
            critical_function()
        if idx == 4:
            override_print()
        if idx == 5:
            a_very_long_function()
        if idx == 6:
            newfunc()
        if idx == 7:
            error_func()
        if (idx + 1) % 3 == 0:
            print("this is a multiline message\n this is line number 2")
            # print("this is a multiline message\n this is line number 3")
            # print("this is a multiline message\n this is line number 4")



if __name__ == "__main__":
    with log_wrap(
        log_file="/hpcfs/users/a1956473/projects/logab/app.log",
        log_level="debug", print_level="debug"):
        exec_program()