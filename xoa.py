import logging
import os
import time
import traceback

from temp import myprint

# Configure logging
logging.basicConfig(
    filename='app.log',           # Log file name
    filemode='w',                 # Append mode ('w' to overwrite)
    level=logging.NOTSET,          # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format=f'{os.getpid()} | %(asctime)s | %(levelname)s | %(name)s : %(message)s',  # Log format
    encoding='utf-8'
)
logger = logging.getLogger(__name__)
if __name__=="__main__":
    try:
        start_time = time.time()
        for idx, char in enumerate(range(100)):
            time.sleep(1)
            if idx % 2 == 0:
                logger.info(f"Loss: {idx}")
                myprint()
            if idx % 4 == 0 and idx > 0:
                with open('abc.txt', 'r') as file:
                    pass
        
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
    finally:
        end_time = time.time()
        logger.info(f"Execution time {end_time - start_time}")

# I'm creating a python script that log into a file, as well as calculating execution time. Above's the script. Is there any way to turn this script into something that I can easily use for my future programs?



# nohup python main.py > /dev/null 2>&1 &