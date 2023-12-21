import os
import csv

from define import *

class Handler:
  def __init__(self, path):
    self.path = path
  
  def write(self, time, place, subject):
    fieldnames = ["time", "place", "subject"]
    file_exists = False
    try:
      with open(self.path, "r"):
        file_exists = True
    except FileNotFoundError:
      pass 
    with open(self.path, mode='a', newline='') as f:
      # JSONデータをバイト列にエンコードして書き込む
      writer = csv.DictWriter(f, fieldnames=fieldnames)

      # If the file didn't exist, write the header
      if not file_exists:
        writer.writeheader()

      # Write the new data
      writer.writerow({"time": time, "place": place, "subject":subject})

  def read(self, name, label="time"):
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        subject = r["subject"]
        #if time in image_name:
        if name in r[label]:
          return time, place, subject
    return None, None, None
  
  def read_all(self):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        subject = r["subject"]
        data.append([time, place, subject])
    return data


  def delete_row(self, name, label="time"):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      fieldnames = reader.fieldnames
      for r in reader:
        #time = r["time"]
        #if time in image_name:
        if name == r[label]:
          continue
        else:
          data.append(r)
          
    with open(self.path, "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for d in data:
        writer.writerow(d)

if __name__ == "__main__":
  pic_csv = Handler(path=PIC_CSV_PATH)
  vid_csv = Handler(path=VID_CSV_PATH)
  sch_csv = Handler(path=SCH_CSV_PATH)
  
  pic_csv.write(time="test", place="test", subject="test")
  print(pic_csv.read(name="test"))
  
  vid_csv.write(time="test", place="test", subject="test")
  print(vid_csv.read(name="test"))
  
  sch_csv.write(time="test", place="test", subject="test")
  print(sch_csv.read(name="test"))