"""
これは、顔認識のためのk-nearest-neighbors（KNN）アルゴリズムの使用例です。

この例は、大量の既知の人物を認識し、計算時間内で未知の人物に対して予測を行いたい場合に役立ちます。

アルゴリズムの概要：
KNN分類器は、まずラベル付けされた（既知の）顔画像のセットで訓練され、そのトレーニングセット内で最も類似した顔（ユークリッド距離に基づく最も近い顔特徴を持つ画像）をk個見つけ、それらのラベルに対して多数決（おそらく重み付き）を行うことによって、未知の画像内の人物を予測します。

たとえば、k=3の場合、トレーニングセット内で与えられた画像に最も近い3つの顔画像がバイデンの画像1枚とオバマの画像2枚であれば、結果は「オバマ」となります。

* この実装では、近隣の顔に重みを付ける重み付き投票が使用されています。

使用方法：

1. 認識したい既知の人物の画像セットを準備します。各既知の人物についてのサブディレクトリ内に画像を整理します。

2. 適切なパラメータを指定して、「train」関数を呼び出します。モデルをディスクに保存して、モデルを再訓練せずに再利用できるようにする場合は、「model_save_path」を渡すことを忘れないでください。

3. トレーニングしたモデルを「predict」に渡して、未知の画像内の人物を認識します。

注意：この例を実行するには、scikit-learnがインストールされている必要があります！次のコマンドでインストールできます：

$ pip3 install scikit-learn
"""

import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition

from define import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.5):
    """
    トレーニングされたKNN分類器を使用して、指定された画像内の顔を認識します

    :param X_img_path: 認識対象の画像へのパス
    :param knn_clf: （オプション）KNN分類器オブジェクト。指定しない場合、model_pathを指定する必要があります
    :param model_path: （オプション）pickled KNN分類器へのパス。指定しない場合、knn_clfを指定する必要があります
    :param distance_threshold: （オプション）顔分類の距離閾値。閾値が大きいほど、未知の人物を既知の人物として誤分類する可能性が高くなります
    :return: 認識された顔の名前と境界ボックスのリスト：[(名前、境界ボックス)、...]
        認識できなかった人物の場合、名前として「unknown」が返されます
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("無効な画像パスです: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("KNN分類器を指定する必要があります。knn_clfまたはmodel_pathを指定してください")

    # トレーニングされたKNNモデルをロード（指定された場合）
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # 画像ファイルを読み込んで顔の位置を検出
    #face_recognition
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)
    

    # 画像内に顔が見つからない場合、空の結果を返す
    if len(X_face_locations) == 0:
        print("人物は検出されませんでした。")
        return []
    else:
        print("{}人検出しました。".format(len(X_face_locations)))

    # 画像内の顔のエンコーディングを検出
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # KNNモデルを使用してテスト顔の最適な一致を見つける
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # クラスを予測し、閾値内でない分類を削除
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def show_prediction_labels_on_image(img_path, predictions):
    """
    顔認識の結果を視覚的に表示します。

    :param img_path: 認識対象の画像へのパス
    :param predictions: predict関数の結果
    :return:
    """
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # 顔を囲む四角をPillowモジュールを使用して描画
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # 顔の下に名前を表示
        text_bbox = draw.textbbox((left, bottom - 10), name)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Pillowのドキュメントに従って描画ライブラリをメモリから削除
    del draw

    # 結果画像を表示
    pil_image.show()

# メイン動作
if __name__ == "__main__":
    test_path = os.path.join(JETSON_PATH, "test")
    train_model_path = os.path.join(JETSON_PATH, "trained_knn_model.clf")

    # トレーニング済み分類器を使用して未知の画像に対して予測を行う
    for image_file in os.listdir(test_path):
        if image_file == "picture_data.csv":
            continue
        full_file_path = os.path.join(test_path, image_file)

        print("{} で顔を検出中...".format(image_file))

        # トレーニング済み分類器モデルを使用して画像内のすべての人物を見つける
        # 注：分類器ファイル名または分類器モデルインスタンスのどちらかを渡すことができます
        predictions = predict(full_file_path, model_path=train_model_path)

        # コンソールに結果を表示
        for name, (top, right, bottom, left) in predictions:
            print("- {} は ({}, {}) にいます".format(name, left, top))

        # 結果を画像上にオーバーレイして表示
        show_prediction_labels_on_image(os.path.join(test_path, image_file), predictions)
