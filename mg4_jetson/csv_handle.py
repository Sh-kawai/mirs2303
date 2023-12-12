import os
import csv

from define import *

CSV_PATH = os.path.join(JETSON_PATH, f"pictures/picture_data.csv")

def write(time, place):
  fieldnames = ["time", "place"]
  file_exists = False
  try:
    with open(CSV_PATH, "r"):
      file_exists = True
  except FileNotFoundError:
    pass 
  with open(CSV_PATH, mode='a', newline='') as f:
    # JSONデータをバイト列にエンコードして書き込む
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # If the file didn't exist, write the header
    if not file_exists:
      writer.writeheader()

    # Write the new data
    writer.writerow({"time": time, "place": place})

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
  write(time="test", place="test")
  print(read("test"))
  #delete_row("test")
  print(read("test"))