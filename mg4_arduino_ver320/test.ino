void test_encoder() {
  long enc_l, enc_r;
  char str[100];

  while (1) {
    encoder_get(&enc_l, &enc_r);
    sprintf(str, "enc_l = %6ld, enc_r = %6ld\n", enc_l, enc_r);
    Serial.print(str);
    delay(T_CTRL);
  }
}

void test_distance() {
  double dist_l, dist_r;
  char str[100], str_l[10], str_r[10];

  while (1) {
    distance_get(&dist_l, &dist_r);
    sprintf(str, "dist_l = %s, dist_r = %s\n",
            dtostrf(dist_l, 6, 1, str_l),
            dtostrf(dist_r, 6, 1, str_r));
    Serial.print(str);
    delay(T_CTRL);
  }
}

void test_motor(int pwm_l, int pwm_r) {
  motor_set(pwm_l, pwm_r);
  while (1) {
        delay(T_CTRL);
  }
}

void test_vel_ctrl(double vel_l, double vel_r) {
  int i = 0;
  char str[100], str_l[10], str_r[10];
  char str_v[10];
  double variance ;
  static long count = 0;
  static int count_max = 1000; //10秒

  vel_ctrl_set(vel_l, vel_r);

  while (1) {
    vel_ctrl_execute();
    if (i >= 10) {
      vel_ctrl_get(&vel_l, &vel_r);
      vel_ctrl_get_vari(&variance);
     sprintf(str, "vel_l = %s, vel_r = %s   variance= %s \n", 
              dtostrf(vel_l, 6, 1, str_l),
              dtostrf(vel_r, 6, 1, str_r),
              dtostrf(variance, 6, 1, str_v));
      Serial.print(str);
      i = 0;
    }
    i++;
    delay(T_CTRL);
    count++;
    if( count > count_max ) break;
  }
  test_motor(0, 0);
}

void test_run_ctrl(run_state_t state, double speed, double dist) {
  int i = 0;
  char str[100], str_dist[10], str_speed[10];

  run_ctrl_set(state, speed, dist);

  while (1) {
    run_ctrl_execute();
    vel_ctrl_execute();
    if (i >= 10) {
      run_ctrl_get(&state, &speed, &dist);
      sprintf(str, "state = %s, speed = %s, dist = %s\n",
              ((state == STR) ? "STR" : (state == ROT) ? "ROT" : "STP"),
              dtostrf(speed, 6, 1, str_speed),
              dtostrf(dist, 6, 1, str_dist));
      Serial.print(str);
      i = 0;
    }
    i++;
    //if( state == STP ) break;
    delay(T_CTRL);
  }
}

void test_batt() {
  double batt;
  char str[100], str_batt[10];

  while (1) {
    batt = io_get_batt();
    sprintf(str, "volt = %s\n", dtostrf(batt, 4, 2, str_batt));
    Serial.print(str);
    delay(T_CTRL);
  }
}

void test_decode() {
  command_data_t command_data = {30000, -255, 0};
  middle_data_t  middle_data;
  serial_data_t  serial_data;

  while (1) {
    middle_data  = raspi_encode2(command_data);
    serial_data  = raspi_encode1(middle_data);
    middle_data  = raspi_decode1(serial_data);
    command_data = raspi_decode2(middle_data);
    Serial.println(command_data.val[0]);
    Serial.println(command_data.val[1]);
    Serial.println(command_data.val[2]);
    delay(1000);
  }
}

void test_arc_move(double speed, double dist, double ang_vel, double ang_dist){
  run_ctrl_set_arc(ARC, speed, dist, ang_vel, ang_dist);
  while(1){
    run_ctrl_execute();
    vel_ctrl_execute();
  }
}
void test_arc_move_sim(double speed){
  int ang_vel = 0;
  double dist = 1000.0;
  double ang_dist = 1000.0;
  while(1){
    Serial.print("ang_vel_ref:" + String(ang_vel) + ", ");
    run_ctrl_set_arc(ARC, speed, dist, ang_vel, ang_dist);
    run_ctrl_execute();
    //vel_ctrl_execute();

    ang_vel++;
    if(ang_vel > 180){
      ang_vel = -179;
    }
    delay(10000/360);
  }
}

void test_servo(){
  servo_ctrl_set(0);
  Serial.println(String(servo_ctrl_get()));
  delay(1000);
  servo_ctrl_set(180);
  Serial.println(String(servo_ctrl_get()));
  delay(1000);
  servo_ctrl_set(75);
  Serial.println(String(servo_ctrl_get()));
  delay(1000);
  servo_ctrl_set(90);
  Serial.println(String(servo_ctrl_get()));
  delay(1000);
  servo_ctrl_set(180);
  Serial.println(String(servo_ctrl_get()));
  delay(1000);
}

void test_servo_rot(){
  int angle = 0;
  int a = 1;
  while(1){
    servo_ctrl_set(angle);
    Serial.println(String(servo_ctrl_get()));
    delay(2);
    angle += a;
    if(angle >= 180) a = -1;
    if(angle == 0) a = 1;
  }
}
