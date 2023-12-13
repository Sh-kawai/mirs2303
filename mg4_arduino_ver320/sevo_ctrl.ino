//Servoオブジェクト
static Servo sv_y; // 縦 y軸
static Servo sv_z; // 横 z軸

void servo_open(){
  sv_y.attach(PIN_SER_Y);
  sv_z.attach(PIN_SER_Z);
}

void servo_set(int pit_y, int yaw_z){
  sv_y.write(pit_y);
  sv_z.write(yaw_z);
}

void servo_get(int *pit_y, int *yaw_z){
  *pit_y = sv_y.read();
  *yaw_z = sv_z.read();
}
