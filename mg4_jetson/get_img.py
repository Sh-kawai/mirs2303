import cv2
from datetime import datetime
import os
import time
import csv_handle
from define import *

def cap_init(cap_path=0):
    cap = cv2.VideoCapture(cap_path)
    if not cap.isOpened():
        print("エラー: カメラを開けませんでした。")
        return None
    
    height = 720
    width = 1280
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    return cap

def save_img(capture, place="", subject=""):
    pic_csv = csv_handle.Handler(path=PIC_CSV_PATH)
    # 現在の時刻を取得
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')  # 時刻のフォーマットを指定
    # 画像を保存
    ret, frame = capture.read()
    pic_dir = os.path.join(JETSON_PATH, "pictures")
    save_path = os.path.join(pic_dir, f"{time_str}.png")
    cv2.imwrite(save_path, frame)
    pic_csv.write(time=time_str, place=place, subject=subject)
    print(f"保存しました:{time_str}.png")
    print(f"保存先:{save_path}")
    if os.path.isfile(save_path):
        print("treu")

def get_img(place="", time_auto=False, click=False):
    # カメラを起動
    capture = cap_init()

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
        if click:
            if keyInp & 0xFF == 13:
                save_img(capture=capture)
                break
        else:
            save_img(capture=capture)
            break
        
        # 画像をウィンドウに表示
        height, width, _ = frame.shape
        txt = f"h:{height} w:{width}"
        cv2.putText(frame, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("frame", frame)

    # 解放
    capture.release()
    cv2.destroyAllWindows()

def save_movie(place="", subject=""):
    vid_csv = csv_handle.Handler(path=VID_CSV_PATH)
    cap = cap_init()
    
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
    vid_csv.write(time=start_time, place=place, subject=subject)

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
    get_img(place="Dlab", time_auto=False, click=True) 
    #save_movie()