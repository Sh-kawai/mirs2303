import os
import glob
import numpy as np
import cv2
from PIL import Image, ImageDraw

#from mg4_jetson.src.modules.define import *
from define import *

COSINE_THRESHOLD = 0.363
NORML2_THRESHOLD = 1.128

# 特徴&顔認証モデルの取得
def init():
  # 学習モデルの取得
  train_dir = os.path.join(JETSON_PATH, "train")
  
  # 特徴を読み込む
  dictionary = []
  files = glob.glob(os.path.join(train_dir, "*/*.npy"))
  for file in files:
    feature = np.load(file)
    user_id = os.path.splitext(os.path.basename(file))[0]
    dictionary.append((user_id, feature))
    
  # モデルを読み込む
  model_folder = os.path.join(JETSON_PATH, "faceCV_models")
  weights = os.path.join(model_folder, "yunet_n_640_640.onnx")
  face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
  weights = os.path.join(model_folder, "face_recognizer_fast.onnx")
  face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
  
  return dictionary, face_detector, face_recognizer

# 公開可能か判断
def check_prohibit(delete_users, recognition_data):
  for face, match_flag, user in recognition_data:
    if user in delete_users:
      return True
  return False

# 特徴を辞書と比較してマッチしたユーザーとスコアを返す関数
def match(recognizer, feature1, dictionary):
  for element in dictionary:
    user_id, feature2 = element
    score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
    if score > COSINE_THRESHOLD:
      return True, (user_id, score)
  return False, ("unknown", 0.0)

# 顔認証の実行
def recognition(img_path, dictionary, face_detector, face_recognizer):
  recognition_data = []
  
  # キャプチャを開く
  capture = cv2.VideoCapture(img_path) # 画像ファイル
  if not capture.isOpened():
    exit()
  
  # フレームをキャプチャして画像を読み込む
  result, image = capture.read()
  if result is False:
    cv2.waitKey(0)
    return recognition_data

  # 画像が3チャンネル以外の場合は3チャンネルに変換する
  channels = 1 if len(image.shape) == 2 else image.shape[2]
  if channels == 1:
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  if channels == 4:
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

  # 入力サイズを指定する
  height, width, _ = image.shape
  face_detector.setInputSize((width, height))

  # 顔を検出する
  result, faces = face_detector.detect(image)
  faces = faces if faces is not None else []
  
  for face in faces:
    # 顔を切り抜き特徴を抽出する
    aligned_face = face_recognizer.alignCrop(image, face)
    feature = face_recognizer.feature(aligned_face)

    # 辞書とマッチングする
    result, user = match(face_recognizer, feature, dictionary)
    recognition_data.append([face, result, user])
    
  return recognition_data

# 顔認証結果の画像表示
def show_recognition_image(img_path, recognition_data):
  pil_image = Image.open(img_path).convert("RGB")
  draw = ImageDraw.Draw(pil_image)
  
  for face, match_flag, user in recognition_data:
    # 顔を囲む四角をPillowモジュールを使用して描画
    x, y, w, h = list(map(int, face[:4]))
    color = (0, 255, 0) if match_flag else (0, 0, 255)
    draw.rectangle(((x, y), (x+w, y+h)), outline=color)
    
    # 認識の結果を描画
    id, score = user
    text = "{}({:.2f})".format(id, score)
    text_bbox = draw.textbbox((x, y - 10), text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.rectangle(((x, y - text_height - 10), (x+w, y)), fill=color, outline=color)
    draw.text((x + 6, y - text_height - 5), text, fill=(255,255,255,255))
  
  # Pillowのドキュメントに従って描画ライブラリをメモリから削除
  del draw

  # 結果画像を表示
  pil_image.show()

if __name__ == '__main__':
  img_dir = PICTURE_DIR
  dictionary, detector, recognizer = init()
  for image_file in os.listdir(img_dir):
    img_path = os.path.join(img_dir, image_file)
    recognition_data = recognition(img_path, dictionary, detector, recognizer)
    delete_flag = check_prohibit()
    print()
    show_recognition_image(img_path, recognition_data)
    