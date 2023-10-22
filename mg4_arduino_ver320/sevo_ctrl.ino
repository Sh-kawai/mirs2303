static Servo servo;

void servo_open(){
  servo.attach(PIN_SERVO, 500, 2400);
  pinMode(PIN_SERVO, OUTPUT);
}

void servo_ctrl_set(int angle){
  servo.write(angle);
}

void servo_ctrl_get(int *angle){
  *angle = servo.read();
}
