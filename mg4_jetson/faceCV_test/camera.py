import cv2
import os

from define import *

def get_img():
    # カメラを起動
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("エラー: カメラを開けませんでした。")
        return False

    while(True):
        # 1フレームの画像を取得
        ret, frame = capture.read()
        # 画像をウィンドウに表示
        cv2.imshow("frame", frame)

        keyInp = cv2.waitKey(1)
        if keyInp & 0xFF == 13:
            #撮影
            ret, frame = capture.read()
            save_dir = os.path.join(JETSON_PATH, "faceCV_test/train")
            print("保存名を入力してください")
            save_name = input()
            save_child_dir = os.path.join(save_dir, save_name)
            if not os.path.exists(save_child_dir):
              os.makedirs(save_child_dir)
              os.chmod(save_child_dir, 0o777)
              print(f"フォルダの作成:{save_name}")
            save_path = os.path.join(save_child_dir, f"{save_name}.png")
            if cv2.imwrite(save_path, frame):
              print(f"保存しました:{save_path}")
            else:
              print(f"保存に失敗しました:{save_path}")

        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            break

    # 解放
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    get_img()