import smbus
import time

# 測定の時間間隔[ms]と範囲[cm]
T_USS = 50 / 1000  # 50 msを秒に変換
USS_MIN = 16
USS_MAX = 600

# センサからMIRS中心までの距離[cm]
DIST_CENTER = 10

# I2Cアドレス
ADDRESS_L = 0x70
ADDRESS_R = 0x71

# smbusインスタンスの初期化
bus = smbus.SMBus(1)  # 1はRaspberry PiのI2Cバス番号

def open(address):
    try:
        # ソフトウェアリビジョンの確認
        revision = bus.read_byte_data(address, 0x00)
        if revision == 0x06:
            print(f"USS at address {address} opened")
            return True
        else:
            print(f"Failed to open USS at address {address}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get(address):
    try:
        bus.write_byte_data(address, 0x00, 0x51)
        time.sleep(T_USS)
        
        lowbyte = bus.read_byte_data(address, 0x03)
        highbyte = bus.read_byte_data(address, 0x02)
        val = (highbyte << 8) + lowbyte
        
        if USS_MIN <= val <= USS_MAX:
            return val + DIST_CENTER
        else:
            return -1
    except Exception as e:
        print(f"Error: {e}")
        return -1

# メインプログラム
if __name__ == "__main__":
    if open(ADDRESS_L) and open(ADDRESS_R):
        try:
            while True:
                distance_l = get(ADDRESS_L)
                distance_r = get(ADDRESS_R)
                print(f"Left: {distance_l} cm, Right: {distance_r} cm")
                time.sleep(1)  # 1秒ごとに読み取る
        except KeyboardInterrupt:
            print("Program stopped by user")
