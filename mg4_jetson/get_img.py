import cv2
from datetime import datetime
import os
import time

import csv_handle
import schedule
from define import *

_camera_flag = False

# カメラオープン
def cap_init(cap_path=0):
    global _camera_flag
    
    # capture open
    cap = cv2.VideoCapture(cap_path)
    if not cap.isOpened():
        print("エラー: カメラを開けませんでした。")
        return None
    
    print(f"open capture {cap_path}")
    
    _camera_flag = True
    
    # capture setting
    height = 720
    width = 1280
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    return cap

# カメラ　終了
def cap_end(cap):
    global _camera_flag
    
    #capture release
    cap.release()
    cv2.destroyAllWindows()
    
    _camera_flag = False
    
    print("capture release")

def cap_flag():
    return _camera_flag

# 画像取得（即時)
def get_img():
    capture = cap_init()
    save_path = _save_img(capture=capture)
    cap_end(cap=capture)
    return save_path

# 定期撮影
def get_auto_img(q_stop, q_save_e=None, show=False):
    capture = cap_init()
    
    auto_time = 30
    start_time = time.time()

    while True:
        # 1フレームの画像を取得
        ret, frame = capture.read()

        keyInp = cv2.waitKey(1)

        if len(q_stop) != 0:
            if q_stop.pop():
                print("[get_auto_img] stop request")
                break
        
        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            print("KeyInput q: finish get_img()")
            break

        elapsed_time = time.time() - start_time
        remaining_time = int(auto_time - elapsed_time)
        if remaining_time <= 0:
            res = _save_img(capture=capture)
            if res and q_save_e != None:
                print("save_img event")
                q_save_e.put(res)
            start_time = time.time()
        
        if show:
            # 画像をウィンドウに表示
            text = f"{remaining_time}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.imshow("frame", frame)
    
    # 解放
    cap_end(capture)
    
def _save_img(capture):
    pic_csv = csv_handle.Handler(path=PIC_CSV_PATH)
    # 現在の時刻を取得
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')  # 時刻のフォーマットを指定
    
    # 画像取得
    ret, frame = capture.read()
    
    # 画像を保存
    save_path = os.path.join(PICTURE_DIR, f"{time_str}.png")
    cv2.imwrite(save_path, frame)
    if os.path.isfile(save_path):
        print(f"保存しました:{time_str}.png")
        print(f"保存先:{save_path}")
        
        # add csv data
        now_sch = schedule.now_schedule()
        place = now_sch["place"]
        subject = now_sch["subject"]
        class_name = now_sch["class"]
        pic_csv.write(time=time_str, place=place, subject=subject, class_name=class_name)
        print(f"csv recode:{time_str}, {place}, {subject}")
        
        return save_path
    
    return None

# 顔学習用撮影(クリック)
def get_train_img():
    capture = cap_init()
    while(True):
        # 1フレームの画像を取得
        ret, frame = capture.read()
        
        keyInp = cv2.waitKey(1)
        
        # qを押されたら停止
        if keyInp & 0xFF == ord('q'):
            print("KeyInput q: finish get_img()")
            break

        elif keyInp & 0xFF == 13:
            ret, frame = capture.read()
            train_path = os.path.join(JETSON_PATH, "train")
            print("保存名を入力してください")
            save_name = input()
            save_child_dir = os.path.join(train_path, save_name)
            if not os.path.exists(save_child_dir):
              os.makedirs(save_child_dir)
              os.chmod(save_child_dir, 0o777)
              print(f"フォルダの作成:{save_name}")
            save_path = os.path.join(save_child_dir, f"{save_name}.png")
            if cv2.imwrite(save_path, frame):
              print(f"保存しました:{save_path}")
            else:
              print(f"保存に失敗しました:{save_path}")

        # 画像をウィンドウに表示
        height, width, _ = frame.shape
        txt = f"h:{height} w:{width}"
        cv2.putText(frame, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("frame", frame)
    
    cap_end(cap=capture)

# 動画撮影
def save_movie(fps=30, rec_time=30):
    vid_csv = csv_handle.Handler(path=VID_CSV_PATH)
    cap = cap_init()
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(JETSON_PATH, f"videos/{time_str}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()

    print("Recording for {} seconds...".format(rec_time))
    
    now_sch = schedule.now_schedule()
    place = now_sch["place"]
    subject = now_sch["subject"]
    class_name = now_sch["class"]
    vid_csv.write(time=time_str, place=place, subject=subject, class_name=class_name)

    while (time.time() - start_time) < rec_time:
        ret, frame = cap.read()
        frame_cp = frame

        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        out.write(frame)
        
        # 表示用
        text = f"{int(time.time() - start_time)}/{rec_time} recoding..."
        cv2.putText(frame_cp, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("Frame", frame_cp)
        
        #time.sleep(0.033)

    out.release()
    cap_end(cap=cap)

    print("Recording completed. Video saved as", output_file)
    return output_file

def check_cam():
    cap = cap_init()
    while True:
        # 1フレームの画像を取得
        ret, frame = cap.read()
        
        keyInp = cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("frame", frame)
    cap_end(cap=cap)

def test_video():
    cap = cap_init()
    
    fps = 30
    rec_time = 10
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_file = os.path.join(JETSON_PATH, f"videos/test.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    print(fourcc)
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()

    while (time.time() - start_time) < rec_time:
        ret, frame = cap.read()
        frame_cp = frame

        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        out.write(frame)
        
        # 表示用
        text = f"{int(time.time() - start_time)}/{rec_time} recoding..."
        cv2.putText(frame_cp, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("Frame", frame_cp)
        
        #time.sleep(0.033)

    out.release()
    cap_end(cap=cap)

    print("Recording completed. Video saved as", output_file)
    return output_file

if __name__ == "__main__":
    #save_img()
    #save_movie()
    #get_train_img()
    #check_cam()
    test_video()