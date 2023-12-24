import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import gspread
from datetime import datetime

#from mg4_jetson.src.modules.define import *
from define import *

# google drive 写真
class GDrive:
  # コンストラクタ(サービス認証&取得)
  def __init__(self):    
    #サービスアカウントキーを指定して認証を作成
    creds = service_account.Credentials.from_service_account_file(SERVICE_KEY_FILE, scopes=['https://www.googleapis.com/auth/drive'])
    
    #認証済みのサービスを取得
    self.service = build("drive", "v3", credentials=creds)
  
  # 画像アップロード(1枚)
  def upload(self, file_path, parent_folder_id=None):
    #フォルダー指定がない場合
    if parent_folder_id == None:
      print("アップロード先のフォルダーを指定してください。")
      return False
    
    #アップロードファイルのメタデータを設定
    file_metadata = {
      "name":os.path.basename(file_path), 
      "parents":[parent_folder_id],
    }
    
    #ファイルのアップロード
    media = MediaFileUpload(file_path)
    up_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    up_file_id = up_file.get("id")
    
    print(f"ファイルをアップロードしました。\nfile_id:{up_file_id}")
    return up_file_id
  
  # 画像削除(1枚)
  def delete(self, file_id):
    #ファイル削除
    try:
      self.service.files().delete(fileId=file_id).execute()
    except HttpError as e:
      if e.resp.status == 404:
        print("ファイルが見つかりませんでした。")
        return False
      else:
        print(f"エラーが発生しました: {e}")
        return False
    else: #正常に動作した場合
      print(f"ファイルが削除されました: {file_id}")
      return True
  
  # フォルダー内の全ての画像削除
  def delete_folder(self, folder_id):
    # Get the list of files in the folder
    files_list = self.service.files().list(q=f"'{folder_id}' in parents",
                                            fields='files(id)').execute()
    print(files_list)
    # Delete each file in the folder
    for file_info in files_list.get('files', []):
        file_id = file_info['id']
        self.service.files().delete(fileId=file_id).execute()
        print(f"File '{file_id}' deleted.")

# spreadsheet データベース
class GSpeadSheet:
  # コンストラクタ(サービス取得 & ワークシート取得)
  def __init__(self, sheet_id):    
    #サービスアカウントキーを指定して認証を作成
    creds = service_account.Credentials.from_service_account_file(SERVICE_KEY_FILE, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
    
    #認証済みのサービスを取得
    self.service = gspread.authorize(creds)
    
    #スプレッドシートを開く
    self.spreadsheet = self.service.open_by_key(sheet_id)
  
  # データ挿入(1行)
  def insert(self, data, sheet_name=None):
    if sheet_name == None:
      print("ワークシート名(sheet_name)を指定してください")
      return False
    
    #ワークシートを選択
    worksheet = self.spreadsheet.worksheet(sheet_name)
    print(data)
    #データの挿入
    worksheet.append_row(data)
    
    print(f"スプレッドシートにデータを記録しました。")
  
  # データ削除(1行)
  def delete(self, file_id, sheet_name=""):
    if sheet_name == None:
      print("ワークシート名(sheet_name)を指定してください")
      return False
    
    #ワークシートを選択
    worksheet = self.spreadsheet.worksheet(sheet_name)
    
    #列データを取得
    col_values = worksheet.col_values(2)
    
    #データの存在する行番号を取得
    macth_rows = [i+1 for i, value in enumerate(col_values) if value == file_id]
    
    #行の削除
    if len(macth_rows) != 0:
      for r in macth_rows:
        worksheet.delete_rows(r)
      print(f"スプレッドシートの{macth_rows}行目のデータを削除しました")

  # シート内のデータを全て削除
  def delete_all(self, sheet_name=""):
    if sheet_name == None:
      print("ワークシート名(sheet_name)を指定してください")
      return False
    
    #ワークシートを選択
    worksheet = self.spreadsheet.worksheet(sheet_name)
    
    #列データを取得
    col_values = worksheet.col_values(2)
    
    #データの存在する行番号を取得
    macth_rows = [i+1 for i, value in enumerate(col_values) if "ファイル" not in value]
    print(macth_rows)
    macth_rows.reverse()
    print(macth_rows)
    
    #行の削除
    if len(macth_rows) != 0:
      for r in macth_rows:
        if r != 1:
          worksheet.delete_rows(r)
      print(f"スプレッドシートの{macth_rows}行目のデータを削除しました")

if __name__ == "__main__":
  file_path = os.path.join(JETSON_PATH, "PuNITロゴ‗.png")
  file_name = os.path.basename(file_path)
  
  Drive = GDrive()
  SpSheet = GSpeadSheet(SHEET_ID)
  folder_id = G_FOLDER_TEST_ID
  sheet_test_name = SHEET_TEST_NAME
  
  while True:
    print("写真アップロード:0, 写真削除:1, all-delete:2")
    inp_int = int(input())
    
    if inp_int == 0:
      print("撮影場所を入力してください:")
      shoot_place = input()
      shoot_date = datetime.now()
      shoot_date = shoot_date.strftime('%Y-%m-%d_%H-%M-%S')
      
      file_id = Drive.upload(file_path, folder_id)
      
      data = [file_name, file_id, "公開", shoot_date, shoot_place]
      SpSheet.insert(data, sheet_test_name)
    elif inp_int == 1:
      print("削除するファイルのidを入力してください:")
      delete_file_id = input()
      
      #ファイル削除
      res = Drive.delete(delete_file_id)
      if res:
        SpSheet.delete(delete_file_id, sheet_test_name)
    elif inp_int == 2:
      print("all delete. Are you OK?[yes/no]")
      while True:
        print("now prohibit all_delete")
        break
        flag = input()
        if flag == "yes":
          print("do delete all pictures")
          #col_values = SpSheet.spreadsheet.worksheet(sheet_test_name).col_values(2)
          #for delete_file_id in col_values:
          #  #ファイル削除
          #  print(f"del: {delete_file_id}")
          #  res = Drive.delete(delete_file_id)
          #  if res:
          #    SpSheet.delete(delete_file_id, sheet_test_name)
          Drive.delete_folder(folder_id)
          SpSheet.delete_all(sheet_test_name)
          break
        elif flag == "no":
          break
        else:
          print("please fill out [yes] or [no] all!")