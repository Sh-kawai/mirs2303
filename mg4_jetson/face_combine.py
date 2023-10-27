import os
import json
import numpy as np
import pickle
from sklearn import neighbors
import math

from define import *

def data_read(clf_files):
  X = []
  y = []
  for clf_file in clf_files:
      with open(clf_file, 'rb') as f:
          loaded_data = json.load(f)
          X.extend([np.array(data) for data in loaded_data["x"]])
          y.extend(loaded_data["y"])
  
  return X, y

def save_clf(X, y, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', debug=False):
          
  # KNN分類器を作成してトレーニング
  knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
  knn_clf.fit(X, y)
  
  # 重みづけのための近傍の数を決定
  if n_neighbors is None:
    n_neighbors = int(round(math.sqrt(len(X))))
    if debug:
      print("自動的にn_neighborsを選択しました:", n_neighbors)

  # トレーニングされたKNN分類器を保存
  if model_save_path is not None:
    with open(model_save_path, 'wb') as f:
      pickle.dump(knn_clf, f)
      
# メイン動作
if __name__ == "__main__":
  model_save_path = os.path.join(JETSON_PATH, "trained_knn_model.clf")
  knn_path = os.path.join(JETSON_PATH, "knn_clf")
  class_names = ["abe", "asou"]
  clf_files = []
  for class_name in class_names:
    knn_name = class_name + "_knn_model.json"
    clf_files.append(os.path.join(knn_path, knn_name))  
  
  X, y = data_read(clf_files, debug=True)
  save_clf(X, y, model_save_path=model_save_path, n_neighbors=3, debug=True)
  