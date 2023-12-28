import csv

from define import *

class Handler:
  # コンストラクタ
  def __init__(self, path):
    self.path = path
  
  # データ入力
  def write(self, time, place, subject, class_name):
    fieldnames = ["time", "place", "subject", "class"]
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
      writer.writerow({"time": time, "place": place, "subject":subject, "class":class_name})

  # ラベルに対するデータ取得
  def read(self, name, label="time"):
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        subject = r["subject"]
        class_name = r["class"]
        #if time in image_name:
        if r[label] in name:
          return time, place, subject, class_name
      return None, None, None, None
  
  # 全データ取得
  def read_all(self):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        time = r["time"]
        place = r["place"]
        subject = r["subject"]
        class_name = r["class"]
        data.append({
          "time":time,
          "place":place,
          "subject":subject,
          "class":class_name,
        })
    return data

  # ラベルに対するデータ削除
  def delete_row(self, name, label="time"):
    data = []
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      fieldnames = reader.fieldnames
      for r in reader:
        #time = r["time"]
        #if time in image_name:
        if r[label] in name:
          continue
        else:
          data.append(r)
          
    with open(self.path, "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for d in data:
        writer.writerow(d)
  
  # 全データ削除
  def delete_all(self):
    with open(self.path, "r", newline="") as f:
      reader = csv.DictReader(f)
      fieldnames = reader.fieldnames
          
    with open(self.path, "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
    
    print("clean all csv file data")


if __name__ == "__main__":
  pic_csv = Handler(path=PIC_CSV_PATH)
  vid_csv = Handler(path=VID_CSV_PATH)
  sch_csv = Handler(path=SCH_CSV_PATH)
  
  print(len(pic_csv.read_all()))
  
  """pic_csv.write(time='1900-12-31_1_8', place="test", subject="test", class_name="test")
  print(pic_csv.read(name='1900-12-31_1_8'))
  
  vid_csv.write(time='1900-12-31_1_8', place="test", subject="test", class_name="test")
  print(vid_csv.read(name='1900-12-31_1_8'))
  
  sch_csv.write(time='1900-12-31_1_8', place="test", subject="test", class_name="test")
  print(sch_csv.read(name='1900-12-31_1_8'))
  
  print(sch_csv.read_all())"""