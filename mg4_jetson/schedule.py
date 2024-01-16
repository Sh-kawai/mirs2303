from datetime import datetime

import csv_handle
from define import *

# 授業時間
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

# 開始 (時限 to 時間)
def get_start_time(num):
  return subject_time[num][0]
# 終了 (時限 to 時間)
def get_finish_time(num):
  return subject_time[num][1]

# スケジュールそのまま取得
def get_schedule():
  schedule_csv = csv_handle.Handler(path=SCH_CSV_PATH)
  schedule = schedule_csv.read_all()
  return schedule

# スケジュール挿入
def set_schedule(year=None, month=None, day=None, start=None, finish=None, place="", subject="", class_name=""):
  args = [year, month, day, start, finish, class_name]
  if None not in args:
    time = f"{year}-{month}-{day}_{start}_{finish}"
    schedule_csv = csv_handle.Handler(path=SCH_CSV_PATH)
    schedule_csv.write(time, place, subject, class_name)
  else:
    print("not match format : 'YYYY-mm-dd_(num)_(num)'")

# 現在のスケジュール取得 (時限 to 時間)
def now_schedule():
  schedule = get_schedule()
  # YY-mm-ss HH:MM:SS.
  now = datetime.today().now()
  # YY-mm-ss
  now_date = now.date()
  # HH:MM:SS.
  now_time = now.time()
  
  for sch in schedule:
    print(sch)
    date, start, finish = sch["time"].split("_")
    place = sch["place"]
    subject = sch["subject"]
    class_name = sch["class"]
    print(date, now_date)
    if date == str(now_date):
      start_str = get_start_time(start)
      finish_str = get_finish_time(finish)
      
      # "HH:MM:SS"
      start_time = datetime.strptime(start_str, "%H:%M:%S").time()
      finish_time = datetime.strptime(finish_str, "%H:%M:%S").time()

      print(start_time, now_time, finish_time)
      
      if start_time < now_time and now_time < finish_time:
        res = {
          "date":date,
          "start":start_str,
          "finish":finish_str,
          "place":place,
          "subject":subject,
          "class":class_name,
        }
        return res
  res = {
          "date":None,
          "start":None,
          "finish":None,
          "place":None,
          "subject":None,
          "class":None,
        }
  return res

if __name__ == "__main__":
  #set_schedule(2024, 1, 16, 3, 4, "Dlab", "工学基礎3" ,"D4")
  print(get_schedule())
  print(now_schedule())
  print(now_schedule()["class"])