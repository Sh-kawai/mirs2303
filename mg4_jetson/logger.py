import inspect
import os

def print_logger(log_txt):
    caller_frame = inspect.stack()[1]
    caller_file = os.path.basename(caller_frame.filename)
    print(f"[{caller_file}] {log_txt}")