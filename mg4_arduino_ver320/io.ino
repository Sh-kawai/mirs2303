void io_open() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_SW, INPUT);
  pinMode(PIN_BATT, INPUT);
  pinMode(PIN_ROS, INPUT_PULLUP);
  pinMode(PIN_LIGHT_0, INPUT);
  pinMode(PIN_LIGHT_1, INPUT);
  pinMode(PIN_LIGHT_2, INPUT);
  pinMode(PIN_LIGHT_3, INPUT);
  digitalWrite(PIN_LED, LOW);
  digitalWrite(PIN_SW, HIGH);
  digitalWrite(PIN_BATT, LOW);
  digitalWrite(PIN_ROS, LOW);
  pinMode(PIN_TOUCH_1, INPUT_PULLUP);
  pinMode(PIN_TOUCH_2, INPUT_PULLUP);
  
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

void io_get_light(int *l0, int *l1, int *l2, int *l3){
  *l0 = analogRead(PIN_LIGHT_0);
  *l1 = analogRead(PIN_LIGHT_1);
  *l2 = analogRead(PIN_LIGHT_2);
  *l3 = analogRead(PIN_LIGHT_3);
}

double io_get_batt() {
  return analogRead(PIN_BATT) * 5.0 / 1024.0 / V_RATIO;
}
