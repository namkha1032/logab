# logab
A lightweight Python package for better log formatting.
## Install
```sh
pip install logab
```
## Usage
```python
from logab import log_init, log_wrap

def main_func():
    # log_init can be called from anywhere to get a logger instance
    logger = log_init()
    logger.debug("Inside main_func")

if __name__=="__main__":
    # log_wrap should be used only once at the program's entry point to configure logging globally
    with log_wrap(log_file="./app.log", log_level="notset"):
        logger = log_init()
        logger.info("Prepare to do main_func")
        main_func()
        logger.info("Finish main_func")
```
## Demo
![Alt Text](https://raw.githubusercontent.com/namkha1032/logab/refs/heads/main/demo.gif)