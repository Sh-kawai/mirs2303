void io_open() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_SW, INPUT);
  pinMode(PIN_BATT, INPUT);
  pinMode(PIN_ROS, INPUT_PULLUP);
  pinMode(PIN_LIGHT_L, INPUT);
  pinMode(PIN_LIGHT_R, INPUT);
  digitalWrite(PIN_LED, LOW);
  digitalWrite(PIN_SW, HIGH);
  digitalWrite(PIN_BATT, LOW);
  digitalWrite(PIN_ROS, LOW);
  pinMode(PIN_CAM_H, INPUT_PULLUP);
  pinMode(PIN_CAM_L, INPUT_PULLUP);
  
}

void io_set_led(int val) {
  digitalWrite(PIN_LED, val);
}

int io_get_led() {
  return digitalRead(PIN_LED);
}

int io_get_sw() {
  return digitalRead(PIN_SW);
}

int io_get_ros(){
  return digitalRead(PIN_ROS);
}

void io_get_light(int *l0, int *l1){
  *l0 = analogRead(PIN_LIGHT_L);
  *l1 = analogRead(PIN_LIGHT_R);
}

double io_get_batt() {
  return analogRead(PIN_BATT) * 5.0 / 1024.0 / V_RATIO;
}

void io_get_camera(int *high, int*low){
  *high = digitalRead(PIN_CAM_H);
  *low = digitalRead(PIN_CAM_L);
}
