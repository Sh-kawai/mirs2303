import csv_handle
from datetime import datetime
from define import *

subject_time = {
  "1":["8:50:00", "9:35:00"],
  "2":["9:35:00", "10:30:00"],
  "3":["10:30:00", "11:15:00"],
  "4":["11:15:00", "12:00:00"],
  "5":["13:10:00", "13:55:00"],
  "6":["13:55:00", "14:40:00"],
  "7":["14:50:00", "15:35:00"],
  "8":["15:35:00", "16:20:00"],
  "-1":["00:00:00", "23:59:59"],
}

def get_start_time(num):
  return subject_time[num][0]
def get_finish_time(num):
  return subject_time[num][1]
  
def get_schedule():
  schedule_csv = csv_handle.Handler(path=SCH_CSV_PATH)
  schedule = schedule_csv.read_all()
  return schedule

def set_schedule(year=None, month=None, day=None, weekday=None, start=None, finish=None, place=""):
  args = [year, month, day, weekday, start, finish]
  if None not in args:
    time = f"{year}-{month}-{day}_{weekday}_{start}_{finish}"
    schedule_csv = csv_handle.Handler(path=SCH_CSV_PATH)
    schedule_csv.write(time, place)
  else:
    print("not match format : 'YYYY-mm-dd_WEK_(num)_(num)'")

set_schedule(2023, 12, 21, "TUE", 1, 2)

def now_schedule():
  schedule = get_schedule()
  # YY-mm-ss HH:MM:SS.
  now = datetime.today().now()
  # YY-mm-ss
  now_date = now.date()
  # HH:MM:SS.
  now_time = now.time()
  
  for sch in schedule:
    date, wk_day, start, finish = sch[0].split("_")
    if date == str(now_date):
      start_str = get_start_time(start)
      finish_str = get_finish_time(finish)
      
      # "HH:MM:SS"
      start_time = datetime.strptime(start_str, "%H:%M:%S").time()
      finish_time = datetime.strptime(finish_str, "%H:%M:%S").time()
      
      if start_time < now_time and now_time < finish_time:
        return sch
  return None

print(now_schedule())