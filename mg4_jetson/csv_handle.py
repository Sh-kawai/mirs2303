import os
import csv

from define import *

CSV_PATH = os.path.join(JETSON_PATH, f"test/picture_data.csv")

def write(data):
  with open(CSV_PATH, mode='a', newline='') as f:
      # JSONデータをバイト列にエンコードして書き込む
      writer = csv.writer(f)
      writer.writerow(data)

def read(image_name):
  with open(CSV_PATH, "r", newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
      time = r["time"]
      place = r["place"]
      if time in image_name:
        return time, place
  
  return None, None


def delete_row(image_name):
  data = []
  with open(CSV_PATH, "r", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
      time = r["time"]
      if time in image_name:
        continue
      else:
        data.append(r)
        
  with open(CSV_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for d in data:
      writer.writerow(d)

if __name__ == "__main__":
  data = ["test", "test"]
  write(data)
  print(read("test"))
  delete_row("test")
  print(read("test"))