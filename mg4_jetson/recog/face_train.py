import json
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from tqdm import tqdm

from define import *

def train(train_dir, save_dir, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    """
    顔認識のためのk-nearest neighbors（KNN）分類器をトレーニングします。

    :param train_dir: 各既知の人物についてのサブディレクトリを含むディレクトリ

     （ディレクトリ構造の詳細はソースコードを参照してください）

     構造:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...

    :param model_save_path: （オプション）モデルをディスクに保存するためのパス
    :param n_neighbors: （オプション）分類時に重みづけする近傍の数。指定しない場合は自動で選択されます
    :param knn_algo: （オプション）KNN分類のための基本データ構造。デフォルトはball_treeです
    :param verbose: トレーニングの詳細を表示するかどうか
    :return: トレーニングされたKNN分類器を返します
    """
    X = []
    y = []

    # トレーニングセット内の各人物をループ
    if not train_dir:
        return None
      
    model_name = os.path.basename(train_dir)

    # 現在の人物の各トレーニング画像をループ
    img_files = image_files_in_folder(train_dir)
    
    for img_path in tqdm(img_files, desc="Inner Loop", leave=False):
        image = face_recognition.load_image_file(img_path)
        face_bounding_boxes = face_recognition.face_locations(image)

        if len(face_bounding_boxes) != 1:
            # トレーニング画像に人物がいない場合（または複数の人物がいる場合）、画像をスキップ
            if verbose:
                print("画像 {} はトレーニングに適していません: {}".format(img_path, "顔が見つからない" if len(face_bounding_boxes) < 1 else "複数の顔が見つかりました"))
        else:
            # 現在の画像の顔エンコーディングをトレーニングセットに追加
            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(model_name)
           
    # KNN分類器を作成してトレーニング
    #knn_clf_data = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    #knn_clf_data.fit(X, y)
    
    knn_clf_data = {"x":[], "y":[]}
    for x_, y_ in zip(X, y):
      knn_clf_data["x"].append(x_.tolist())
      knn_clf_data["y"].append(y_)
    
    # トレーニングされたKNN分類器を保存
    model_save_file = model_name + "_knn_model.json"
    model_save_path = os.path.join(save_dir, model_save_file)
    with open(model_save_path, 'wb') as f:
      # JSONデータをバイト列にエンコードして書き込む
      json_data = json.dumps(knn_clf_data).encode("utf-8")
      f.write(json_data)

    return json_data
  
if __name__ == "__main__":
    train_folder = os.path.join(JETSON_PATH, "train")
    knn_path = os.path.join(JETSON_PATH, "knn_clf")
    
    # ステップ1：KNN分類器をトレーニングしてディスクに保存
    # モデルがトレーニングされて保存されたら、次回からこのステップをスキップできます。
    print("KNN分類器のトレーニング...")
    train_dirs = os.listdir(train_folder)
    for train_dir in tqdm(train_dirs, desc="Outer Loop", leave=False):
      train_path = os.path.join(train_folder, train_dir)
      classifier = train(train_path, knn_path,  n_neighbors=3, verbose=True)
    print("トレーニング完了！")