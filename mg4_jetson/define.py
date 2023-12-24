import os

#JETSON_PATH = "/home/mirs2303/mirs2303/mg4_jetson"
JETSON_PATH = os.path.relpath(os.path.dirname(__file__))
PICTURE_DIR = os.path.join(JETSON_PATH, "pictures")
PIC_CSV_PATH = os.path.join(PICTURE_DIR, "picture_data.csv")
VID_CSV_PATH = os.path.join(JETSON_PATH, "videos/video_data.csv")
SCH_CSV_PATH = os.path.join(JETSON_PATH, "schedule_app/schedule.csv")
G_FOLDER_MAIN_ID = "1CONPdtwSL4rP9xj4kQDjPVK7Fi-I8GkE"
G_FOLDER_TEST_ID = "1GPnSliJqIBAYrhpTz7bVfYHzt7LzaRYf"
SHEET_ID = "1e6MzBqjgl8S1QtGBeQOWqrg8rwIqeiarAl570BGflG0"
SHEET_MAIN_NAME = "メインデータ"
SHEET_TEST_NAME = "テストデータ"
SERVICE_JSON = "photo-test-393509-a09fbab1df81.json"
#HOST = "172.25.19.3"
HOST = "192.168.1.2"
PORT = 8080