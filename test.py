import logging
import time

from inside import myfunc
from logab import log_context, log_init
from temp import supermegaprint
from utils.newfunc import print_somethingggggggggg

if __name__ == "__main__":
    with log_context():
        logger = log_init()
        for idx, char in enumerate(range(100)):
            time.sleep(1)
            supermegaprint(idx)
            myfunc()
            if idx % 2 == 0 and idx > 0:
                supermegaprint(idx)
                logger.warning(f"Loss: {idx} 游客")
                logger.critical(f"Loss: {idx} au cuộc đàm phán cuối tuần trước, Mỹ và Trung Quốc thống nhất tạm hoãn một phần thuế đối ứng trong 90 ngày, đồng thời giảm đáng kể tổng thuế nhập khẩu.")
                print_somethingggggggggg()
            # if idx % 3 == 0:
            #     myfunc()
            if idx % 5 == 0 and idx > 0:
                with open('abc.txt', 'r') as file:
                    pass

# if __name__ == "__main__":
#     logger = log_init()
#     with log_context(logger):
#         logger2 = log_init()
#         with log_context(logger2, log_file='app2.log'):
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