import csv_handle
from datetime import datetime
from define import *

sub_time = ["8:50:00", "9:35:00", "10:30:00", "11:15:00", "12:00:00", "13:10:00", "13:55:00", "14:40:00", "14:50:00", ""]

schedule_csv = csv_handle.Handler(path=SCH_CSV_PATH)
schedule = schedule_csv.read_all()
now_date = datetime.now().hour

print(schedule)
print(now_date)

if schedule[0][0].split("_")[0] == str(now_date):
  print("aaaa")
  
def get_schedule():
  pass