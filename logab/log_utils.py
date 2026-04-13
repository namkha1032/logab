import builtins
import logging
import os
import shutil
import time
import traceback
from contextlib import contextmanager
from functools import partial
from datetime import datetime
    
class ABFormatter(logging.Formatter):
    file_index = 3
    nu_index = 4
    original_print = builtins.print

    def __init__(self, log_file, is_format_lib):
        init_len = [len(str(os.getpid())), 19, 4, 7, 2, 8]
        self.log_file = log_file
        self.is_format_lib = is_format_lib
        self.attr_list = ['process', 'asctime', 'levelname', 'pathname', 'lineno', 'funcName']
        self.max_lengths = {key:val for key, val in zip(self.attr_list, init_len)}
        self.just_multiple_lines = False
        self.cwf = os.getcwd().split("/")[-1]
        super().__init__()

    # -------------------- methods static --------------------

    @staticmethod
    def logab_custom_print(print_level, *args, **kwargs):
        # Combine arguments into a single message
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '')
        message = sep.join(str(arg) for arg in args) + end
        frame_list = traceback.extract_stack()
        is_custom_print = all(na in frame_list[-2].name for na in ["custom", "print"])
        frame = frame_list[-2] if not is_custom_print else frame_list[-3]
        filename = frame.filename
        funcname = frame.name
        lineno = frame.lineno

        # Log the message at the specified print_level
        logging.log(print_level, message, extra={
                'file_id': filename,
                'func_id': funcname,
                'line_id': lineno
            })
    
    @staticmethod
    def format_seconds(seconds):
        if seconds <= 0:
            return "0 seconds"
        units = [
            ("day", 86400),    # 24 * 60 * 60
            ("hour", 3600),    # 60 * 60
            ("minute", 60),
            ("second", 1)
        ]
        result = []
        remaining = float(seconds)
        for unit_name, unit_seconds in units[:-1]:
            if remaining >= unit_seconds:
                value = int(remaining // unit_seconds)
                remaining = remaining % unit_seconds
                result.append(f"{value} {unit_name}{'s' if value > 1 else ''}")
        if remaining > 0 or not result: 
            if remaining.is_integer():
                result.append(f"{int(remaining)} second{'s' if remaining != 1 else ''}")
            else:
                result.append(f"{remaining:.4f} seconds".rstrip('0').rstrip('.'))
        return " ".join(result)

    # -------------------- methods instance --------------------

    def modify_record_path(self, record):
        abs_list = record.pathname.split("/")
        path_type = "user" # user | logab | python
        for idx, fold in enumerate(reversed(abs_list), start=1):
            if fold == "logab":
                path_type = "logab"
                record.pathname =  "logab"
                record.lineno = 0
                break
            elif fold == "site-packages" or "python3" in fold:
                path_type = "python"
                record.pathname = "/".join(abs_list[-idx:])
                break
            elif fold == self.cwf:
                path_type = "user"
                record.pathname = "/".join(abs_list[-(idx-1):])
                break
        return path_type, record
    
    def update_max_length(self, record):
        rewrite=False
        for field in self.max_lengths:
            newlen = len(str(getattr(record, field, '')))
            if self.max_lengths[field] < newlen:
                rewrite = True
                self.max_lengths[field] = max(self.max_lengths[field], newlen)
        if rewrite and self.log_file:
            self.rewrite_log()

    def rewrite_log(self):
        bak_path = f"{self.log_file}.bak"
        with open (bak_path, mode='w', encoding='utf-8') as file_backup:
            bak_path = file_backup.name
            with open (self.log_file, 'r', encoding='utf-8') as file_log:
                for idx, line in enumerate(file_log):
                    line = line.strip()
                    if line.startswith("----"):
                        hor_line = self.draw_horizontal_line()
                        file_backup.write(f"{hor_line}\n")
                    else:
                        attr_list =line.split("|")
                        newline_arr = []
                        for attr_idx, attr in enumerate(attr_list):
                            if attr_idx > 4:
                                break
                            if attr_idx == self.file_index:
                                lo_li_arr = attr.strip().split(":")
                                new_li = lo_li_arr[0].rjust(self.max_lengths[self.attr_list[self.file_index]])
                                new_lo = lo_li_arr[1].ljust(self.max_lengths[self.attr_list[self.nu_index]])
                                newline_arr.append(f"{new_li}:{new_lo}")
                            else:
                                attr = attr.strip()
                                attr = attr.ljust(self.max_lengths[self.attr_list[attr_idx + (1 if attr_idx > self.file_index else 0)]])
                                newline_arr.append(attr)
                        newline_arr.append("|".join(attr_list[5:]).strip())
                        file_backup.write(f"{' | '.join(newline_arr)}\n")
        try:
            shutil.copyfile(bak_path, self.log_file)
            os.remove(bak_path)
        except Exception as e:
            pass

    def apply_message_format(self, record):
        # Define message format
        record.msg = record.getMessage().strip("\n")
        self._style._fmt = (
            f'%(process){self.max_lengths["process"]}d | '
            f'%(asctime){self.max_lengths["asctime"]}s | '
            f'%(levelname)-{self.max_lengths["levelname"]}s | '
            f'%(pathname){self.max_lengths["pathname"]}s:%(lineno)-{self.max_lengths["lineno"]}d | '
            f'%(funcName)-{self.max_lengths["funcName"]}s | '
            f'%(message)s'
        )
        
        # Handle multi-line message
        old_msg_list = record.getMessage().split("\n")
        new_msg_list = []
        result_msg = ""
        for msg in old_msg_list:
            record.msg = msg
            new_msg_list.append(super().format(record))
        
        # Handle multi-line horizontal line
        upper_line = f"{self.draw_horizontal_line()}\n" if (len(old_msg_list) > 1 and self.just_multiple_lines == False) else ""
        lower_line = f"\n{self.draw_horizontal_line()}" if len(old_msg_list) > 1 else ""
        self.just_multiple_lines = True if len(old_msg_list) > 1 else False
        
        # Form final message
        msg_rows = "\n".join(new_msg_list)
        result_msg = f"{upper_line}{msg_rows}{lower_line}"
        return result_msg

    # -------------------- methods utils --------------------

    def draw_horizontal_line(self):
        placement='+'
        hor_arr = ['-'*(self.max_lengths[item]) for item in self.attr_list]
        hor_arr[self.file_index] = hor_arr[self.file_index] + hor_arr[self.nu_index] + '-'
        hor_arr.pop(self.nu_index)
        hor_arr.append('-'*50)
        hor_line = f'-{placement}-'.join(hor_arr)
        return hor_line
    
    def print_raw(self, content, mode='a', end_char="\n"):
        if self.log_file:
            with open(self.log_file, mode, encoding='utf-8') as file:
                file.write(f"{content}{end_char}")
        else:
            self.original_print(f"{content}{end_char}", end="", flush=True)
    
    # -------------------- methods overwrite --------------------

    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.strftime("%Y-%m-%d %H:%M:%S")
    
    def format(self, record):
        if hasattr(record, 'func_id'):
            record.pathname = record.file_id
            record.funcName = record.func_id
            record.lineno = record.line_id
        path_type, record = self.modify_record_path(record)
        if path_type != "python" or self.is_format_lib:
            self.update_max_length(record)
            result_msg = self.apply_message_format(record)
            return result_msg
        else:
            return record.getMessage()

class ABFilter(logging.Filter):
    def __init__(self, ignore_libs = []):
        super().__init__()
        self.ignore_libs = ignore_libs

    def filter(self, record):
        is_log = False if (hasattr(record, 'file_id') and any(lib in record.file_id for lib in self.ignore_libs)) else True
        return is_log

@contextmanager
def log_wrap(log_file=None, log_level="info", print_level="info", is_format_lib=False, ignore_libs=[]):
    # Set up log configuration
    log_level=getattr(logging, log_level.upper(), logging.info)
    formatter = ABFormatter(log_file=log_file, is_format_lib=is_format_lib)
    handler = logging.StreamHandler() if log_file == None else logging.FileHandler(log_file, mode='a', encoding='utf-8')
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()

    # Clear existing handlers and filters
    root_logger.handlers.clear()
    root_logger.filters.clear()

    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Set up log filter
    if len(ignore_libs) > 0:
        filterer = ABFilter(ignore_libs=ignore_libs)
        root_logger.addFilter(filterer)
    
    # Set up print configuration
    print_level=getattr(logging, print_level.upper(), logging.info)
    builtins.print = partial(ABFormatter.logab_custom_print, print_level)
    
    # Print table header
    header_list = [
        ('PID', formatter.max_lengths['process']), 
        ('Time', formatter.max_lengths['asctime']), 
        ('Lvl', formatter.max_lengths['levelname']), 
        ('File:Nu', formatter.max_lengths['pathname'] + formatter.max_lengths['lineno'] + 1), 
        ('Function', formatter.max_lengths['funcName']), 
        ('Message', 0)
    ]
    header_list_pad = []
    for idx, header_item in enumerate(header_list):
        pad_header = header_item[0].ljust(header_item[1]) if idx != formatter.file_index else header_item[0].rjust(header_item[1])  
        header_list_pad.append(pad_header)
    header_str = f"{' | '.join(header_list_pad)}\n{formatter.draw_horizontal_line()}"
    formatter.print_raw(header_str, mode='w')

    start_time = time.time()
    try:
        yield
    except Exception as e:
        # Catch and write error message
        root_logger.error(e)
        hor_line = formatter.draw_horizontal_line()
        tb = traceback.format_exc()
        formatter.print_raw(hor_line)
        formatter.print_raw(tb, end_char="")
        exit()
    finally:
        # Write execution time
        end_time = time.time()
        hor_line = formatter.draw_horizontal_line()
        formatter.print_raw(hor_line)
        root_logger.info(f"Execution time {ABFormatter.format_seconds(end_time-start_time)}")
        builtins.print = formatter.original_print
        root_logger.removeHandler(handler)
        if len(ignore_libs) > 0:
            root_logger.removeFilter(filterer)

def log_init():
    logger = logging.getLogger()
    return logger