import RPi.GPIO as GPIO
import time

# ピンの設定
PIN_SW_F = 7

def open(pin=PIN_SW_F):
    try:
        # GPIOのモード設定
        GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering schemeを使用

        # ピンのセットアップ
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        print("GPIO opened pin:", pin)
        return True
    except Exception as e:
        print(f"Failed to open GPIO: {e}")
        return False

def get(pin=PIN_SW_F):
    sw_f = GPIO.input(pin)
    return sw_f

def close():
  GPIO.cleanup()

# メインプログラム
if __name__ == "__main__":
    if open():
        try:
            while True:
                print(get())
                time.sleep(0.1)  # 1秒ごとにスイッチの状態を読み取る
        finally:
            close()  # プログラム終了時にGPIOをクリーンアップ
