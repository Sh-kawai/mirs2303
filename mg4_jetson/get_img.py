import cv2
from datetime import datetime
import os
import csv_handle
from define import *

def get_img(place="", loop=False):
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
            # 現在の時刻を取得
            current_time = datetime.now()
            time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')  # 時刻のフォーマットを指定
            # 画像を保存
            ret, frame = capture.read()
            pic_dir = os.path.join(JETSON_PATH, "pictures")
            save_path = os.path.join(pic_dir, f"{time_str}.png")
            cv2.imwrite(save_path, frame)
            csv_handle.write(time=time_str, place=place)
            print(f"保存しました:{time_str}.png")
            if not loop:
                break

        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            break

    # 解放
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    get_img(place="kari", loop=True)