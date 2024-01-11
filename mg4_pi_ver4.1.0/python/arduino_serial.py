import serial
import time

from define import *

# シリアルポートの設定
serial_port = None

def open(port='/dev/ttyACM0', baud=115200, timeout=1):
  global serial_port
  try:
    serial_port = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    time.sleep(2)
    recv_clear()
    send_clear()
    print("Arduino opened")
    return serial_port
  except serial.SerialException:
    print("Failed to open Arduino")
    return None

def close():
  global serial_port
  serial_port.close()
  print("Arduino closed")

def recv_clear():
  global serial_port
  serial_port.reset_input_buffer()

def send_clear():
  global serial_port
  serial_port.reset_output_buffer()

def _read():
  global serial_port
  val = [0] * 7
  while serial_port.in_waiting >= 7:
    val[0] = serial_port.read()[0]
    if val[0] >= 0x80:
      for i in range(1, 7):
        val[i] = serial_port.read()[0]
      return val
  return None

def _write(data):
  global serial_port
  serial_port.write(bytearray(data))

def recv():
  data = _read()
  if data:
    return _decode2(_decode1(data))
  return None

def send(command_data):
  _write(_encode1(_encode2(command_data)))

def _decode1(data):
  middle_data = [
    ((data[0] << 1) & 0xfe) | ((data[1] >> 6) & 0x01),
    ((data[1] << 2) & 0xfc) | ((data[2] >> 5) & 0x03),
    ((data[2] << 3) & 0xf8) | ((data[3] >> 4) & 0x07),
    ((data[3] << 4) & 0xf0) | ((data[4] >> 3) & 0x0f),
    ((data[4] << 5) & 0xe0) | ((data[5] >> 2) & 0x1f),
    ((data[5] << 6) & 0xc0) | ((data[6] >> 1) & 0x3f),
  ]
  return middle_data

def _decode2(middle_data):
  command_data = []
  # 符号付きでデコード
  for i in range(0, len(middle_data), 2):
    bytes_pair = middle_data[i:i+2]
    signed_int = int.from_bytes(bytes_pair, byteorder='big', signed=True)
    command_data.append(signed_int)
  return command_data

def _encode1(middle_data):
  serial_data = [
    0x80 | ((middle_data[0] >> 1) & 0x7f),
    ((middle_data[0] << 6) & 0x40) | ((middle_data[1] >> 2) & 0x3f),
    ((middle_data[1] << 5) & 0x60) | ((middle_data[2] >> 3) & 0x1f),
    ((middle_data[2] << 4) & 0x70) | ((middle_data[3] >> 4) & 0x0f),
    ((middle_data[3] << 3) & 0x78) | ((middle_data[4] >> 5) & 0x07),
    ((middle_data[4] << 2) & 0x7c) | ((middle_data[5] >> 6) & 0x03),
    ((middle_data[5] << 1) & 0x7e),
  ]
  return serial_data

def _encode2(command_data):
  middle_data = [
    (command_data[0] >> 8) & 0xff,
    command_data[0] & 0xff,
    (command_data[1] >> 8) & 0xff,
    command_data[1] & 0xff,
    (command_data[2] >> 8) & 0xff,
    command_data[2] & 0xff,
  ]
  return middle_data


if __name__ == "__main__":
    # 使用例
    serial_port = open()
    if serial_port:
        # Arduinoとの通信処理
        while True:
            print(f"STP:{STP}, STR:{STR}, ROT:{ROT}, ARC:{ARC}, LINE:{LINE}, SER:{SER}, CAM:{CAM}, ROS:{ROS}")
            data = input().split()
            if len(data) == 3:
                for i, d in enumerate(data):
                    if i == 0:
                      d = int(d) + 1
                    data[i] = int(d)
                recv_clear()
                send(data)
                time.sleep(1)
                print(recv())
        close()
