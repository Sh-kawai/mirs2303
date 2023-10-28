from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

import csv_handle
from define import *

def make_time_pic():
  
  # 画像サイズを指定
  image_width = 1920  # 幅 (フルHD)
  image_height = 1080  # 高さ (フルHD)

  # 新しい画像を作成
  image = Image.new("RGB", (image_width, image_height), (255, 255, 255))  # 白色の背景

  # 現在の時刻を取得
  current_time = datetime.now()
  time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')  # 時刻のフォーマットを指定

  # テキストを追加するためのフォントとサイズを指定
  font_size = 150
  font = ImageFont.truetype("arial.ttf", font_size)  # フォントファイルのパスを指定

  # テキストを画像に追加
  draw = ImageDraw.Draw(image)
  text_color = (0, 0, 0)  # テキストの色 (黒色)
  text_position = (50, 50)  # テキストを表示する位置 (x, y)
  draw.text(text_position, time_str, fill=text_color, font=font)
  
  # 画像に黒い枠を追加
  border_color = (0, 0, 0)  # 枠の色 (黒色)
  border_thickness = 10  # 枠の太さ (ピクセル)
  border_box = [(0, 0), (image.width - 1, image.height - 1)]
  draw.rectangle(border_box, outline=border_color, width=border_thickness)
  
  # 画像を保存
  test_dir = os.path.join(JETSON_PATH, "test")
  save_path = os.path.join(test_dir, f"{time_str}.png")
  image.save(save_path)
  
  print(f"{save_path}に画像を保存しました。")
  
  #データの保存
  place = "仮体育館"
  data = [time_str, place]
  csv_handle.write(data)
  
  return save_path
  
if __name__ == "__main__":
  make_time_pic()