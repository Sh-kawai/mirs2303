static double height_ref = 0.0;
static double h_err_prev = 0.0;
static double h_err_sum = 0.0;
static double pwm = 0.0;
static double pwm_prev = 0.0;

static volatile long count_e = 0;

static int a_curr_e, b_curr_e;

bool camera_ctrl_exec_height = true;

// カメラオープン
void camera_ctrl_open(){
  pinMode(PIN_ENC_A_E, INPUT);
  pinMode(PIN_ENC_B_E, INPUT);
  /*digitalWrite(PIN_ENC_A_E, HIGH);
  digitalWrite(PIN_ENC_B_E, HIGH);*/
  
  pinMode(PIN_DIR_E, OUTPUT);
  pinMode(PIN_PWM_E, OUTPUT);
  analogWrite(PIN_PWM_E, 0);
  
  attachInterrupt(INTERRUPT_E, camera_enc_change, CHANGE);
}

// 定期実行関数
void camera_ctrl_execute(){
  double height_curr = camera_get_height();
  
  if(camera_ctrl_exec_height){
    // 高さ用PID
    const double Kp = 0.01;
    const double Ki = 0.0;
    const double Kd = 0.0;
    double h_err_curr;
    
    Serial.println(height_ref - height_curr);
    
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
  }
  pwm_prev = pwm;

  _camera_motor_set(int(pwm));
}

// 昇降用モーター指令関数
void _camera_motor_set(int pwm){
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

// 昇降高さ指定関数
void camera_ctrl_set_height(double h){
  camera_ctrl_exec_height = true;
  height_ref = h;
}

// 昇降モータ(pwm)指定関数
void camera_ctrl_set_motor(int p){
  camera_ctrl_exec_height = false;
  height_ref = 0.0;
  h_err_prev = 0.0;
  h_err_sum = 0.0;
  pwm = p;
}

// 昇降機構リセット関数
void camera_ctrl_reset(){
  height_ref = 0.0;
  h_err_prev = 0.0;
  h_err_sum = 0.0;
  pwm = 0.0;
  pwm_prev = 0.0;

  _camera_motor_set(0);
  count_e = 0;
}

// カメラの高さ取得関数
double camera_get_height(){
  //return count_e * ELEV_PIT / ENC_RANGE_E;
  return count_e;
}

double camera_get_pwm(){
  return pwm;
}

// 昇降用モータエンコーダ関数
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
  
  a_curr_e = a_curr;
  b_curr_e = b_curr;
  
  /*if (digitalRead(PIN_ENC_A_E) != digitalRead(PIN_ENC_B_E))
    count_e++;//正転
  else {
    count_e--;//逆転
  }*/
}

void _test_enc_e(){
  Serial.print("a_curr = ");
  Serial.print(a_curr_e);
  Serial.print(" b_curr = ");
  Serial.println(b_curr_e);
}
