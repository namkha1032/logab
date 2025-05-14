import logging
import os
import sys
import time

from logab import log_init, log_wrap
from tests.temp import a_very_long_function, cause_error, supermegaprint
from tests.utils.newutils import newfunc


def print_main():
    logger = log_init()
    logger.warning("In log main")
if __name__ == "__main__":
    with log_wrap(log_level="notset"):
        logger = log_init()
        for idx, char in enumerate(range(100)):
            # supermegaprint(idx)
            time.sleep(1)
            logger.info(idx)
            if idx == 1:
                print_main()
            if idx == 2:
                supermegaprint()
                logger.warning(f"Loss: {idx} 游客")
                logger.critical(f"Loss: {idx} au cuộc đàm phán cuối tuần trước, Mỹ và Trung Quốc thống nhất tạm hoãn một phần thuế đối ứng trong 90 ngày, đồng thời giảm đáng kể tổng thuế nhập khẩu.")
            if idx == 5:
                a_very_long_function()
            if idx == 6:
                newfunc()
            if idx == 7:
                cause_error()

# if __name__ == "__main__":
#     logger = log_init()
#     with log_wrap(logger):
#         logger2 = log_init()
#         with log_wrap(logger2, log_file='app2.log'):
#             for idx, char in enumerate(range(100)):
#                     time.sleep(1)
#                     myprint(idx)
#                     if idx % 2 == 0:
#                         logger2.debug(f"Loss: {idx}")
#                     if idx % 3 == 0:
#                         myfunc()
#                     if idx % 5 == 0 and idx > 0:
#                         with open('abc.txt', 'r') as file:
#                             pass