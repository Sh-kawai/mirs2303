import os
import csv

import face_main, gdrive_class
from define import *

import kari_make_pic

def csv_read(image_name):
  csv_path = os.path.join(JETSON_PATH, f"test/picture_data.csv")
  with open(csv_path, "r", newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
      time = r["time"]
      place = r["place"]
      if time in image_name:
        return time, place
  
  return None, None


def csv_delete_row(image_name):
  csv_path = os.path.join(JETSON_PATH, f"test/picture_data.csv")
  data = []
  with open(csv_path, "r", newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
      time = r["time"]
      if time in image_name:
        continue
      else:
        data.append(r)
  
  with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "place"])
    for d in data:
      writer.writerow(d)

Drive = gdrive_class.GDrive()
SpSheet = gdrive_class.GSpeadSheet(SHEET_ID)

# 画像作成
file_path = kari_make_pic.make_time_pic()

test_dir = os.path.join(JETSON_PATH, f"test")
for image_name in os.listdir(test_dir):
  if image_name.split(".")[1] == "csv":
    continue
  # 顔認証
  known_names = ["abe", "asou"]
  prohibit_names = ["abe"]
  image_path, names, delete_flag = face_main.recognize_person(image_name, known_names, prohibit_names, show=True)

  if delete_flag:
    # 画像削除
    if os.path.exists(image_path):
      os.remove(image_path)
      print("削除対象者を検出しました。")
      print(f"{image_name}を削除しました。")
  else:
    # 画像&データ アップロード
    file_id = Drive.upload(file_path, GDRIVE_FOLDER_ID)
    shoot_date, shoot_place = csv_read(image_name)
    data = [image_name, file_id, "公開", shoot_date, shoot_place]
    SpSheet.insert(data, "メインデータ")
    
    # csvデータ行削除
    csv_delete_row(image_name)
    
    # 画像削除
    if os.path.exists(image_path):
      os.remove(image_path)
      print(f"{image_name}を削除しました。")