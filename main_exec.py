from main_func import exec_program
from logab import log_wrap
if __name__ == "__main__":
    with log_wrap(
        log_file="./app.log",
        log_level="debug", print_level="debug"):
        exec_program()