import os
import glob
import numpy as np
import cv2

from define import *

COSINE_THRESHOLD = 0.363
NORML2_THRESHOLD = 1.128

def init():
  train_dir = os.path.join(JETSON_PATH, "train")
  
  # キャプチャを開く
  capture = cv2.VideoCapture(0) # カメラ
  if not capture.isOpened():
    exit()
  
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
  
  return capture, dictionary, face_detector, face_recognizer

# 特徴を辞書と比較してマッチしたユーザーとスコアを返す関数
def match(recognizer, feature1, dictionary):
  for element in dictionary:
    user_id, feature2 = element
    score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
    if score > COSINE_THRESHOLD:
      return True, (user_id, score)
  return False, ("", 0.0)

def take_picture(capture):
  train_dir = os.path.join(JETSON_PATH, "train")
  tmp_path = os.path.join(train_dir, "tmp")
  save_path = os.path.join(tmp_path, "tmpman.jpg")
  ret, frame = capture.read()
  cv2.imwrite(save_path, frame)
  print(f"画像を撮影しました。path:{save_path}")

def recognition(capture, dictionary, face_detector, face_recognizer):
  while True:
    # フレームをキャプチャして画像を読み込む
    result, image = capture.read()
    if result is False:
      cv2.waitKey(0)
      break

    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
      image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # 入力サイズを指定する
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    print(height, width)

    # 顔を検出する
    result, faces = face_detector.detect(image)
    faces = faces if faces is not None else []

    response = []
    
    for face in faces:
      # 顔を切り抜き特徴を抽出する
      aligned_face = face_recognizer.alignCrop(image, face)
      feature = face_recognizer.feature(aligned_face)

      # 辞書とマッチングする
      result, user = match(face_recognizer, feature, dictionary)
      
      response.append([face, result, user])
      
      # 顔のバウンディングボックスを描画する
      box = list(map(int, face[:4]))
      color = (0, 255, 0) if result else (0, 0, 255)
      thickness = 2
      cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

      # 認識の結果を描画する
      id, score = user if result else ("unknown", 0.0)
      text = "{0} ({1:.2f})".format(id, score)
      position = (box[0], box[1] - 10)
      font = cv2.FONT_HERSHEY_SIMPLEX
      scale = 0.6
      cv2.putText(image, text, position, font, scale, color, thickness, cv2.LINE_AA)
      print(id, score)
    cv2.namedWindow("faceCV_realtime", cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("faceCV_realtime", image)
    
    # Escキーでプログラムを終了
    key = cv2.waitKey(1)
    if key == 27:
      break
    #Enterキーで写真撮影
    if key & 0xFF == 13:
      take_picture(capture)

  
if __name__ == "__main__":
  cap, dict, detector, recognizer = init()
  recognition(cap, dict, detector, recognizer)
  