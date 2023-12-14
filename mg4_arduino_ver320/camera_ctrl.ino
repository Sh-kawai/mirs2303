static double height_ref = 0.0;
static double height_curr = 0.0;
static double h_err_prev = 0.0;
static double h_err_sum = 0.0;
static double err_curr = 0.0;
static double err_prev = 0.0;
static double vel_ref = 0.0;
static double vel_curr = 0.0;

void camera_ctrl_open(){
  pinMode(PIN_DIR_E, OUTPUT);
  pinMode(PIN_PWM_E, OUTPUT);
  analogWrite(PIN_PWM_E, 0);
  
  attachInterrupt(INTERRUPT_E, camera_enc_change, CHANGE);
}

void camera_ctrl_execute(){
  // 高さ用PID
  const double Kp = 1.0;
  const double Ki = 1.0;
  const double Kd = 0.0;
  
  double h_ctrl, h_err_curr;
  
  h_err_curr = height_ref - height_curr;
  h_err_sum += h_err;
  
  h_ctrl = Kp * h_err_curr + Ki * h_err_sum + Kd * (h_err_curr - h_err_prev);
}

void camera_vel_ctrl(){
  // PIDゲイン
  const double Kp = 1.0; //0.5
  const double Ki = 1.0; //0.7
  const double Kd = 0.0;

  int pwm_l, pwm_r;
  double dist_curr, err_curr;

  // 速度 [cm/s] = 距離の差分 [cm] / (制御周期 [ms] / 1000)
  distance_get(&dist_curr_l, &dist_curr_r);
  vel_curr = (dist_curr - dist_prev) / T_CTRL * 1000.0;

  // 誤差の計算
  err_curr = vel_ref - vel_curr;
  err_sum += err_curr;

  vari += abs(err_curr);
  varian = vari / count;
  count ++;

  // PID制御
  pwm = Kp * err_curr + Ki * err_sum + Kd * (err_curr - err_prev);

  // 速度指令値 = 0 なら強制的に停止
  if (vel_ref_l == 0.0) pwm_l = 0;
  if (vel_ref_r == 0.0) pwm_r = 0;

  camera_motor_set(pwm);

  dist_prev = dist_curr;
  err_prev  = err_curr;
}

void camera_motor_set(int pwm){
  //モータ回転方向の補正
  //pwm *= -1;
  
  if(pwm > 255) pwm = 255;
  if(pwm < -255) pwm = -255;
  
  if (pwm_l > 0) {
    digitalWrite(PIN_DIR_E, HIGH);
    analogWrite(PIN_PWM_E, pwm);
  } else {
    digitalWrite(PIN_DIR_E, LOW);
    analogWrite(PIN_PWM_E, -pwm);
  }
}
