import os

import face_combine, face_recognition_knn
from define import *

import kari_make_pic

def recognize_person(image_path, known_names, prohibit_names, show=False):
  #絶対パス
  model_save_path = os.path.join(JETSON_PATH, "trained_knn_model.clf")
  knn_path = os.path.join(JETSON_PATH, "knn_clf")
  image_file = os.path.basename(image_path)
  
  print(f"{known_names}のモデルを取得 ")
  clf_files = []
  for known_name in known_names:
    knn_name = known_name + "_knn_model.json"
    clf_files.append(os.path.join(knn_path, knn_name))
  
  X, y = face_combine.data_read(clf_files)
  knn_clf = face_combine.save_clf(X, y, model_save_path=model_save_path, n_neighbors=3)
  
  print(f"{image_file} で顔を検出中...")
  
  predictions = face_recognition_knn.predict(image_path, model_path=model_save_path)
  
  names = []
  delete_flag = False
  for item in predictions:
    names.append(item[0])
    if item[0] in prohibit_names:
      delete_flag = True
  print(f"検出された人物:{names}")

  if show:
    face_recognition_knn.show_prediction_labels_on_image(image_path, predictions)
    
  return names ,delete_flag
  

if __name__ == "__main__":
  #引数
  image_path = "/home/mirs2303/program/mirs2303/mg4_jetson/test/13_abs227-jpp01055407.jpg"
  #image_path = kari_make_pic.make_time_pic()
  known_names = ["abe", "asou"]
  prohibit_names = ["abe"]
  #関数
  names ,delete_flag = recognize_person(image_path, known_names, prohibit_names, show=True)
  
  print(f"削除対象者の有無:{delete_flag}")