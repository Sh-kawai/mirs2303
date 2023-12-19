import cv2
from datetime import datetime
import os
import time
import csv_handle
from define import *

def save_img(capture, place=""):
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

def get_img(place="", loop=False, time_auto=False):
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

        if time_auto:
            save_img(capture=capture, place=place)
            time.sleep(30)
        #elif keyInp & 0xFF == 13:
        else:
            save_img(capture=capture, place=place)
            if not loop:
                break

        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            break

    # 解放
    capture.release()
    cv2.destroyAllWindows()

def save_movie():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = 30
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(JETSON_PATH, f"videos/{time_str}.mp4")

    fource = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fource, fps, (frame_width, frame_height))

    record_duration = 30
    start_time = time.time()

    print("Recording for {} seconds...".format(record_duration))

    while (time.time() - start_time) > record_duration:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        cv2.imshow("Frame", frame)

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.033)

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    print("Recording completed. Video saved as", output_file)

if __name__ == "__main__":
    get_img(place="Dlab", loop=True, time_auto=True) 
    #save_movie()