//Servoオブジェクト
static Servo sv_y; // 縦 y軸
static Servo sv_z; // 横 z軸
static const int min_ang = 70;

void servo_open(){
  sv_y.attach(PIN_SER_Y);
  sv_z.attach(PIN_SER_Z);
  servo_set(35, 35);
}

void servo_set(int pit_y, int yaw_z){
  sv_y.write(pit_y + min_ang);
  sv_z.write(yaw_z + min_ang);
}

void servo_get(int *pit_y, int *yaw_z){
  *pit_y = sv_y.read() - min_ang;
  *yaw_z = sv_z.read() - min_ang;
}
