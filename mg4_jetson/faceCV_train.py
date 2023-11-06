import os
import numpy as np
import cv2

from define import *

def face_cut():
  # トレーニングセット内の各人物をループ
  train_dir = os.path.join(JETSON_PATH, "train")

  for class_name in os.listdir(train_dir):
    class_dir = os.path.join(train_dir, class_name)
    if not os.path.isdir(class_dir):
      continue
    
    # 現在の人物の各トレーニング画像をループ
    img_files = os.listdir(class_dir)
    
    for img_file in img_files:
      path = os.path.join(class_dir, img_file)
  
      # 画像を開く
      image = cv2.imread(path)
      if image is None:
        continue

      # 画像が3チャンネル以外の場合は3チャンネルに変換する
      channels = 1 if len(image.shape) == 2 else image.shape[2]
      if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
      if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

      # モデルを読み込む
      weights = os.path.join(JETSON_PATH, "yunet_n_640_640.onnx")
      face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
      weights = os.path.join(JETSON_PATH, "face_recognizer_fast.onnx")
      face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

      # 入力サイズを指定する
      height, width, _ = image.shape
      face_detector.setInputSize((width, height))

      # 顔を検出する
      _, faces = face_detector.detect(image)

      # 検出された顔を切り抜く
      aligned_faces = []
      if faces is not None:
        for face in faces:
          aligned_face = face_recognizer.alignCrop(image, face)
          aligned_faces.append(aligned_face)
          
      # 画像を表示、保存する
      for i, aligned_face in enumerate(aligned_faces):
        #cv2.imshow("aligned_face {:03}".format(i + 1), aligned_face)
        cv2.imwrite(os.path.join(class_dir, "{}{:03}.jpg".format(class_name, i + 1)), aligned_face)

def train():
  # トレーニングセット内の各人物をループ
  train_dir = os.path.join(JETSON_PATH, "train")

  for class_name in os.listdir(train_dir):
    class_dir = os.path.join(train_dir, class_name)
    if not os.path.isdir(class_dir):
      continue
    
    # 現在の人物の各トレーニング画像をループ
    img_files = os.listdir(class_dir)
    
    for img_file in img_files:
      if class_name in img_file:
        path = os.path.join(class_dir, img_file)
        
        # 画像を開く
        image = cv2.imread(path)
        if image is None:
          continue
        
        # モデルを読み込む
        weights = os.path.join(JETSON_PATH, "face_recognizer_fast.onnx")
        face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        
        # 特徴を抽出する
        face_feature = face_recognizer.feature(image)
        print(face_feature)
        print(type(face_feature))

        # 特徴を保存する
        save_path = os.path.join(class_dir, class_name)
        np.save(save_path, face_feature)

if __name__ == '__main__':
  face_cut()
  train()