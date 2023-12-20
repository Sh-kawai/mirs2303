import os
import csv

from define import *

class Handler:
  def __init__(self, path):
    self.path = path
  
  def write(self, time, place):
    fieldnames = ["time", "place"]
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
      writer.writerow({"time": time, "place": place})

  def read(self, image_name):
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        if time in image_name:
          return time, place
    return None, None
  
  def read_all(self):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        data.append([time, place])
    return data


  def delete_row(self, image_name):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      fieldnames = reader.fieldnames
      for r in reader:
        time = r["time"]
        if time in image_name:
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
  
  pic_csv.write(time="test", place="test")
  print(pic_csv.read(image_name="test"))
  
  vid_csv.write(time="test", place="test")
  print(vid_csv.read(image_name="test"))