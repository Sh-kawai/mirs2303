// 割り込みに使用する変数 (volatileをつけて宣言)
static volatile long count_l = 0;
static volatile long count_r = 0;
static volatile long count_ros_l = 0;
static volatile long count_ros_r = 0;

static int a_curr_l, b_curr_l;

void encoder_open() {
  pinMode(PIN_ENC_A_L, INPUT);
  pinMode(PIN_ENC_B_L, INPUT);
  pinMode(PIN_ENC_A_R, INPUT);
  pinMode(PIN_ENC_B_R, INPUT);
  digitalWrite(PIN_ENC_A_L, HIGH);
  digitalWrite(PIN_ENC_B_L, HIGH);
  digitalWrite(PIN_ENC_A_R, HIGH);
  digitalWrite(PIN_ENC_B_R, HIGH);
  attachInterrupt(INTERRUPT_L, enc_change_l, CHANGE);
  attachInterrupt(INTERRUPT_R, enc_change_r, CHANGE);
}

void encoder_get(long *cnt_l, long *cnt_r) {
  *cnt_l = count_l;
  *cnt_r = count_r;

  // エンコーダ回転方向の補正
  *cnt_l *= -1;
  //*cnt_r *= -1;
}

void encoder_reset() {
  count_l = 0;
  count_r = 0;
}

void encoder_ros_get(long *cnt_l, long *cnt_r) {
  *cnt_l = count_ros_l;
  *cnt_r = count_ros_r;

  // エンコーダ回転方向の補正
  *cnt_l *= -1;
  //*cnt_r *= -1;
}

void encoder_ros_reset() {
  count_ros_l = 0;
  count_ros_r = 0;
}

static void enc_change_l() {
  int a_curr, b_curr;
  static int a_prev = LOW, b_prev = LOW;

  a_curr = digitalRead(PIN_ENC_A_L);
  b_curr = digitalRead(PIN_ENC_B_L);

  /*// 正転 : [L, H]→(L, L)→[H, L]→(H, H)→[L, H]
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) count_l++;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) count_l++;

  // 逆転 : [L, L]→(L, H)→[H, H]→(H, L)→[L, L]
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) count_l--;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) count_l--;*/

  if (a_curr != b_curr){
    count_l++;
    count_ros_l++;
  } else {
    count_l--;
    count_ros_l--;
  }

  a_prev = a_curr;
  b_prev = b_curr;
  
  a_curr_l = a_curr;
  b_curr_l = b_curr;
}

static void enc_change_r() {
  int a_curr, b_curr;
  static int a_prev = LOW, b_prev = LOW;

  a_curr = digitalRead(PIN_ENC_A_R);
  b_curr = digitalRead(PIN_ENC_B_R);

  /*// 正転 : [L, H]→(L, L)→[H, L]→(H, H)→[L, H]
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) count_r++;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) count_r++;

  // 逆転 : [L, L]→(L, H)→[H, H]→(H, L)→[L, L]
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) count_r--;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) count_r--;*/

  if (a_curr != b_curr){
    count_r++;
    count_ros_r++;
  } else {
    count_r--;
    count_ros_r--;
  }

  a_prev = a_curr;
  b_prev = b_curr;
}

void _test_enc_l(){
  Serial.print("a_curr_l = ");
  Serial.print(a_curr_l);
  Serial.print(" b_curr_l = ");
  Serial.println(b_curr_l);
}
