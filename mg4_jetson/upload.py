import os
import faceCV_recognition
import google_drive, csv_handle, get_img
from define import *

def main(debug=False):
  # google drive
  Drive = google_drive.GDrive()
  SpSheet = google_drive.GSpeadSheet(SHEET_ID)
  pic_csv = csv_handle.Handler(PIC_CSV_PATH)
  vid_csv = csv_handle.Handler(VID_CSV_PATH)

  # 認証写真の取得
  pic_dir = os.path.join(JETSON_PATH, "pictures")
  for image_file in os.listdir(pic_dir):
    if image_file.split(".")[1] == "csv":
      continue
    
    # 画像の絶対パス
    image_path = os.path.join(pic_dir, image_file)
    
    # 顔認証(face_recognition)
    #known_names = ["abe", "asou"] # 識別対象者
    #prohibit_names = ["abe"] # 公開禁止者
    #names, delete_flag = face_main.recognize_person(image_path, known_names, prohibit_names, show=True)
    
    # 顔認証(opencv)
    delete_users = ["riki"] # 公開禁止者
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
      # 画像&データ アップロード
      file_id = Drive.upload(image_path, GDRIVE_FOLDER_ID)
      shoot_date, shoot_place = pic_csv.read(image_name=image_file)
      data = [image_file, file_id, "公開", shoot_date, shoot_place]
      SpSheet.insert(data, "メインデータ")
      
      # csvデータ行削除
      pic_csv.delete_row(path=PIC_CSV_PATH, image_name=image_file)
      
      # 画像削除
      if os.path.exists(image_path):
        os.remove(image_path)
        print(f"{image_file}を削除しました。")

if __name__ == "__main__":
  get_img.get_img()
  main(debug=False)