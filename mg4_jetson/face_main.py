import os

import face_combine, face_recognition_knn
from define import *

def recognize_person(image_name, known_names, prohibit_names, show=False):
  model_save_path = os.path.join(JETSON_PATH, "trained_knn_model.clf")
  knn_path = os.path.join(JETSON_PATH, "knn_clf")
  test_path = os.path.join(JETSON_PATH, "test")
  full_file_path = os.path.join(test_path, image_name)
  
  print(f"{known_names}のモデルを取得 ")
  clf_files = []
  for known_name in known_names:
    knn_name = known_name + "_knn_model.json"
    clf_files.append(os.path.join(knn_path, knn_name))
  
  X, y = face_combine.data_read(clf_files)
  face_combine.save_clf(X, y, model_save_path=model_save_path, n_neighbors=3)
  
  print(f"{image_name} で顔を検出中...")
  
  predictions = face_recognition_knn.predict(full_file_path, model_path=model_save_path)
  
  names = []
  delete_flag = False
  for item in predictions:
    names.append(item[0])
    if item[0] in prohibit_names:
      delete_flag = True
  print(f"検出された人物:{names}")

  if show:
    face_recognition_knn.show_prediction_labels_on_image(os.path.join(test_path, image_name), predictions)
    
  return full_file_path, names ,delete_flag
  

if __name__ == "__main__":
  #引数
  image_name = "001_ed.jpg"
  known_names = ["abe", "asou"]
  prohibit_names = ["abe"]
  #関数
  image_path, names ,delete_flag = recognize_person(image_name, known_names, prohibit_names, show=True)
  
  print(f"削除対象者の有無:{delete_flag}")