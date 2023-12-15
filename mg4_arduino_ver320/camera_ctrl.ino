static double height_ref = 0.0;
static double height_curr = 0.0;
static double h_err_curr = 0.0;
static double h_err_prev = 0.0;
static double h_err_sum = 0.0;
static double pwm = 0.0;
static double pwm_prev = 0.0;
static double err_curr = 0.0;
static double err_prev = 0.0;
static double vel_ref = 0.0;
static double vel_curr = 0.0;

static volatile long count_e = 0;

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
  
  h_err_curr = height_ref - height_curr;
  h_err_sum += h_err_curr;
  
  pwm = Kp * h_err_curr + Ki * h_err_sum + Kd * (h_err_curr - h_err_prev);

  int accel_pwm = 500; //[value/s]

  if(pwm - pwm_prev > accel_pwm * (T_CTRL / 1000.0)){
    pwm = pwm_prev + accel_pwm * (T_CTRL / 1000.0);
  } else if(pwm - pwm_prev > -accel_pwm * (T_CTRL / 1000.0)){
    pwm = pwm_prev - accel_pwm * (T_CTRL / 1000.0);
  }
  
  h_err_prev = h_err_curr;
  pwm_prev = pwm;

  camera_motor_set(int(pwm));
}


void camera_motor_set(int pwm){
  //モータ回転方向の補正
  //pwm *= -1;
  
  if(pwm > 255) pwm = 255;
  if(pwm < -255) pwm = -255;
  
  if (pwm > 0) {
    digitalWrite(PIN_DIR_E, HIGH);
    analogWrite(PIN_PWM_E, pwm);
  } else {
    digitalWrite(PIN_DIR_E, LOW);
    analogWrite(PIN_PWM_E, -pwm);
  }
}


static void camera_enc_change() {
  int a_curr, b_curr;
  static int a_prev = LOW, b_prev = LOW;

  a_curr = digitalRead(PIN_ENC_A_E);
  b_curr = digitalRead(PIN_ENC_B_E);

  // 正転 : [L, H]→(L, L)→[H, L]→(H, H)→[L, H]
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) count_e++;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) count_e++;

  // 逆転 : [L, L]→(L, H)→[H, H]→(H, L)→[L, L]
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) count_e--;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) count_e--;

  a_prev = a_curr;
  b_prev = b_curr;
}
