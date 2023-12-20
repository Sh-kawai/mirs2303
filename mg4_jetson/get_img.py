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
    csv_handle.write(path=PIC_CSV_PATH ,time=time_str, place=place)
    print(f"保存しました:{time_str}.png")

def get_img(place="", time_auto=False):
    # カメラを起動
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("エラー: カメラを開けませんでした。")
        return False

    auto_time = 30
    start_time = time.time()
    while(True):
        # 1フレームの画像を取得
        ret, frame = capture.read()
        
        keyInp = cv2.waitKey(1)
        
        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            print("KeyInput q: finish get_img()")
            break

        if time_auto:
            elapsed_time = time.time() - start_time
            remaining_time = int(auto_time - elapsed_time)
            text = f"{remaining_time}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            if remaining_time <= 0:
                save_img(capture=capture, place=place)
                start_time = time.time()
        #elif keyInp & 0xFF == 13:
        else:
            save_img(capture=capture, place=place)
            break
        
        # 画像をウィンドウに表示
        cv2.imshow("frame", frame)

    # 解放
    capture.release()
    cv2.destroyAllWindows()

def save_movie(place=""):
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

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    record_duration = 30
    start_time = time.time()

    print("Recording for {} seconds...".format(record_duration))
    csv_handle.write(path=VID_CSV_PATH, time=start_time, place=place)

    while (time.time() - start_time) < record_duration:
        ret, frame = cap.read()
        frame_cp = frame

        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        text = f"{int(time.time() - start_time)}/{record_duration}"
        cv2.putText(frame_cp, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("Frame", frame_cp)
        out.write(frame)

        #time.sleep(0.033)

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    print("Recording completed. Video saved as", output_file)

if __name__ == "__main__":
    #get_img(place="Dlab", time_auto=True) 
    save_movie()