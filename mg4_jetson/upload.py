import os
import faceCV_recognition
import google_drive, csv_handle, get_img
from define import *

def upload(image_file, debug=False, gdrive_main=False):
  Drive = google_drive.GDrive()
  SpSheet = google_drive.GSpeadSheet(SHEET_ID)
  pic_csv = csv_handle.Handler(PIC_CSV_PATH)
  vid_csv = csv_handle.Handler(VID_CSV_PATH)
  
  # 画像の絶対パス
  pic_dir = PICTURE_DIR
  image_path = os.path.join(pic_dir, image_file)
  
  # 顔認証(opencv)
  delete_users = [] # 公開禁止者
  dictionary, detector, recognizer = faceCV_recognition.init()
  # 顔認証の実行
  res = faceCV_recognition.recognition(image_path, dictionary, detector, recognizer)
  # 公開有無の判別
  delete_flag = faceCV_recognition.check_prohibit(delete_users, res)
  # 撮影画像の表示
  if debug:
    faceCV_recognition.show_recognition_image(image_path, res)

  if delete_flag:
    # 画像削除
    if os.path.exists(image_path):
      os.remove(image_path)
      print("削除対象者を検出しました。")
      print(f"{image_file}を削除しました。")
  else:
    if gdrive_main:
      folder_id = G_FOLDER_MAIN_ID
      sheet_name = SHEET_MAIN_NAME
    else:
      folder_id = G_FOLDER_TEST_ID
      sheet_name = SHEET_TEST_NAME
    # 画像&データ アップロード
    file_id = Drive.upload(image_path, folder_id)
    shoot_date, shoot_place, shoot_subject = pic_csv.read(name=image_file)
    data = [image_file, file_id, "公開", shoot_date, shoot_place, shoot_subject]
    SpSheet.insert(data, sheet_name)
    
    # csvデータ行削除
    pic_csv.delete_row(name=image_file)
    
    # 画像削除
    if os.path.exists(image_path):
      os.remove(image_path)
      print(f"{image_file}を削除しました。")

def main(debug=False, gdrive_main=False):
  # 認証写真の取得
  pic_dir = PICTURE_DIR
  for image_file in os.listdir(pic_dir):
    if image_file.split(".")[1] == "csv":
      continue
    
    upload(image_file=image_file, debug=debug, gdrive_main=gdrive_main)
  
  pic_csv = csv_handle.Handler(PIC_CSV_PATH)
  vid_csv = csv_handle.Handler(VID_CSV_PATH)
  print("clean csv file data")
  pic_csv.delete_all()

if __name__ == "__main__":
  #get_img.get_img()
  main(debug=False, gdrive_main=False)