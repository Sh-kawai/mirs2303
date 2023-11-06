import os

import face_main, faceCV_recognition
import gdrive_class, csv_handle, get_img
from define import *

def main():
  Drive = gdrive_class.GDrive()
  SpSheet = gdrive_class.GSpeadSheet(SHEET_ID)

  test_dir = os.path.join(JETSON_PATH, "test")
  for image_file in os.listdir(test_dir):
    if image_file.split(".")[1] == "csv":
      continue
    
    # 画像の絶対パス
    image_path = os.path.join(test_dir, image_file)
    
    # 顔認証
    known_names = ["abe", "asou"]
    prohibit_names = ["abe"]
    #names, delete_flag = face_main.recognize_person(image_path, known_names, prohibit_names, show=True)
    
    delete_users = ["riki"]
    dictionary, detector, recognizer = faceCV_recognition.init()
    res = faceCV_recognition.recognition(image_path, dictionary, detector, recognizer)
    delete_flag = faceCV_recognition.check_prohibit()
    faceCV_recognition.show_recognition_image(image_path, res)

    if delete_flag:
      # 画像削除
      if os.path.exists(image_path):
        os.remove(image_path)
        print("削除対象者を検出しました。")
        print(f"{image_file}を削除しました。")
    else:
      # 画像&データ アップロード
      file_id = Drive.upload(image_path, GDRIVE_FOLDER_ID)
      shoot_date, shoot_place = csv_handle.read(image_file)
      data = [image_file, file_id, "公開", shoot_date, shoot_place]
      SpSheet.insert(data, "メインデータ")
      
      # csvデータ行削除
      csv_handle.delete_row(image_file)
      
      # 画像削除
      if os.path.exists(image_path):
        os.remove(image_path)
        print(f"{image_file}を削除しました。")

if __name__ == "__main__":
  get_img.get_img()
  main()