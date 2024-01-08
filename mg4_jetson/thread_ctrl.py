import threading
import collections
import time

active_thread = {}
active_q = {}

def thread_start(label, func, kwargs={}):
  if label in active_thread:
    start_flag = False
    return start_flag
  else:
    q_stop = collections.deque([], 1)
    kwargs["q_stop"] = q_stop
    thread = threading.Thread(target=func, kwargs=kwargs, daemon=True)
    thread.start()
    active_thread[label] = thread
    active_q[label] = q_stop
    start_flag = True
    return start_flag

def thread_finish(label):
  if label in active_thread:
    thread = active_thread.pop(label)
    q_stop = active_q.pop(label)
    q_stop.append(True)
    thread.join()
    fin_flag = True
    return fin_flag
  else:
    fin_flag = False
    return fin_flag

def thread_finish_all():
  for label in active_q.keys():
    thread = active_thread.pop(label)
    q_stop = active_q.pop(label)
    q_stop.append(True)
    thread.join()
  return

def auto_thread_run(label, func, kwargs={}):
  # thread check
  auto_thread_check(label=label)
  
  if label in active_thread:
    thread_flag = False
    return thread_flag
  else:
    thread = threading.Thread(target=func, kwargs=kwargs, daemon=True)
    thread.start()
    active_thread[label] = thread
    thread_flag = True
    return thread_flag

def auto_thread_check(label):
  if label in active_thread:
    running_thread = threading.enumerate()
    thread = active_thread.pop(label)
    if thread in running_thread:
      active_thread[label] = thread
      fin_flag = False
      return fin_flag
    else:
      fin_flag = True
      return fin_flag
  else:
    fin_flag = True
    return fin_flag

def _test_print(q_stop):
  num = 0
  while True:
    if len(q_stop) != 0:
      if q_stop.pop():
        break
    print(num)
    num += 1
    time.sleep(1)

def _test_print_auto():
  max = 20
  for num in range(max):
    print(num)
    num += 1
    time.sleep(1)

if __name__ == "__main__":
  print("thread_start")
  thread_start("test", _test_print)
  input()
  thread_finish("test")
  print("thread_finish")
  
  print("auto_thread_run")
  auto_thread_run("test_auto", _test_print_auto)
  while True:
    inp = input()
    if auto_thread_check("test_auto"):
      print("have finished")
      break
    else:
      print("running")
      if inp == "q":
        break
  