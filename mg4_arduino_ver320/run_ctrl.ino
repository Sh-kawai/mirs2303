static run_state_t run_state = STP;
static double speed_ref  = 0.0;
static double speed_curr = 0.0;
static double dist_ref   = 0.0;
static double dist_curr  = 0.0;
static double ang_vel_ref = 0.0; // ARC
static double ang_vel_curr = 0.0; // ARC
static double ang_dist_ref = 0.0; // ARC
static double ang_dist_curr = 0.0; // ARC
static double er  = 0.0 , er_d = 0.0 ;
static double er_sum  = 0.0;
static double er_prev  = 0.0;

void run_ctrl_execute() {
  // 直進制御において減速を開始する距離 [cm]
  const double dist_vel_down = 0.0;

  // 回転制御において減速を開始する角度 [deg]
  const double angle_vel_down = 0.0;

  // 直進制御における左右のタイヤの距離差の補正ゲイン
  const double Ks_p = 0.0 ; // 40.0            5.5
  const double Ks_i = 0.0 ; // 0.2  1.0        0.6
  const double Ks_d = 0.0 ; // 50.0  20.0  5.0 7.0

  // 回転制御における左右のタイヤの距離差の補正ゲイン
  const double Kr = 0.0;

  // ライントレース用PIDゲイン
  const double Kl_p = 0.4;
  const double Kl_i = 0.0;
  const double Kl_d = 1.6;

  int sign;
  double d_l, d_r, v_l, v_r, ratio, vel_ref, vel_mod;
  double vel_diff_ref; // 円弧運動のタイヤ速度差 ARC

  // 負の指令値に対応
  if (dist_ref >= 0.0) {
    sign = 1;
  } else {
    sign = -1;
  }

  distance_get(&d_l, &d_r);
  vel_ctrl_get(&v_l, &v_r);

  switch (run_state) {
    case STP:
      vel_ctrl_set(0.0, 0.0);
      break;
    case STR:
      //直線走行距離調整
      d_r *= K_STR_LR;
    
      // 直進距離
      dist_curr  = (d_l + d_r) / 2.0;
      speed_curr = (v_l + v_r) / 2.0 * sign;

      // 減速率
      ratio = sign * (dist_ref - dist_curr) / dist_vel_down;
      if (ratio < 0.0) ratio = 0.0;
      if (ratio > 1.0) ratio = 1.0;

      if (speed_ref == 0.0 || dist_ref == 0.0 || ratio == 0.0) {
        run_state = STP;
        vel_ctrl_set(0.0, 0.0);
      } else {
        // 減速の実行
        vel_ref = sign * speed_ref * ratio;

        // 左右のタイヤの距離差の補正
        er = d_l - d_r;
        er_sum += er;
        er_d = er - er_prev;
        vel_mod = Ks_p * er + Ks_i * er_sum  + Ks_d  * er_d ;
        er_prev = er;

        vel_ctrl_set((vel_ref - vel_mod), (vel_ref + vel_mod));
      }

      break;
    case ROT:
      // 回転角度
      dist_curr  = -(d_l - d_r) / D_TIRE * 180.0 / PI;
      speed_curr = -(v_l - v_r) / D_TIRE * 180.0 / PI * sign;

      // 減速率
      ratio = sign * (dist_ref - dist_curr) / angle_vel_down;
      if (ratio < 0.0) ratio = 0.0;
      if (ratio > 1.0) ratio = 1.0;

      if (speed_ref == 0.0 || dist_ref == 0.0 || ratio == 0.0) {
        run_state = STP;
        vel_ctrl_set(0.0, 0.0);
      } else {
        // 減速の実行＆角速度指令値→速度指令値に変換
        vel_ref = sign * speed_ref * ratio * D_TIRE / 2.0 * PI / 180.0;

        // 左右のタイヤの距離差の補正
        vel_mod = -(d_l + d_r) * Kr;

        vel_ctrl_set(-(vel_ref - vel_mod), (vel_ref + vel_mod));
      }

      break;
    case ARC: // 円弧運動 ARC
      // ROS2ornetworkxの場合は直進速度&回転速度
      // その他の場合左右タイヤの速度

      // 直進速度&回転速度の場合
      // 直進距離
      //dist_curr  = (d_l + d_r) / 2.0; // [cm]
      speed_curr = (v_l + v_r) / 2.0 * sign; //[cm]
      // 回転角度
      //ang_dist_curr  = -(d_l - d_r) / D_TIRE * 180.0 / PI; //[度]
      ang_vel_curr = -(v_l - v_r) / D_TIRE * 180.0 / PI * sign; //[度/s]

      // 減速率
      //ratio = sign * (dist_ref - dist_curr) / angle_vel_down;
      //if (ratio < 0.0) ratio = 0.0;
      //if (ratio > 1.0) ratio = 1.0;
      ratio = 1.0;
      
      if (speed_ref == 0.0 || dist_ref == 0.0 || ratio == 0.0) {
        run_state = STP;
        vel_ctrl_set(0.0, 0.0);
      } else {
        // 直線目標速度設定(&減速の実行)
        vel_ref = sign * speed_ref * ratio; //[cm/s]
        // 回転目標速度設定(左:-,右:+)(&減速の実行)
        vel_diff_ref = sign * ang_vel_ref * ratio * D_TIRE / 2.0 * PI / 180; // [rad/s]

        //誤差の補正

        vel_ctrl_set((vel_ref - vel_diff_ref), (vel_ref + vel_diff_ref));
        //Serial.print("vel_l:" + String(vel_ref - vel_diff_ref) + ", vel_r:" + String(vel_ref + vel_diff_ref));
        //Serial.println(", vel_rel:" + String(vel_ref) + ", vel_diff_ref:" + String(vel_diff_ref));
      }
      
      break;
    case LINE: // ライントレース
      int gray, light0, light1, light2, light3;

      gray = (BLACK + WHITE)/2;
      io_get_light(&light0, &light1, &light2, &light3);
      er = light1 - light2;
      er_prev = er;

      vel_ref = sign * speed_ref * ratio;

      if(light1 != WHITE && light2 != WHITE){
        //左右の値が両方ともwhiteじゃないなら
        vel_mod = Kl_p * er + Kl_d * (er - er_prev);
        vel_ctrl_set((vel_ref - vel_mod), (vel_ref + vel_mod));
      }else{
        vel_ctrl_set(0.0, 0.0);
      }

      break;
  }
}

void run_ctrl_set(run_state_t state, double speed, double dist) {
  if(run_state == state && speed_ref == abs(speed)){
    dist_ref = dist + dist_curr;
  } else if(run_state == state && dist_ref == dist){
    speed_ref = abs(speed);
  } else {
    run_state = state;
    speed_ref = abs(speed);
    dist_ref = dist;
    ang_vel_ref = 0.0;
    ang_dist_ref = 0.0;
    vel_ctrl_reset();
    er = 0;
    er_prev = 0;
    er_sum = 0;
  }
  /*
  run_state = state;
  speed_ref = abs(speed);
  dist_ref = dist;
  ang_vel_ref = 0.0;
  ang_dist_ref = 0.0;
  vel_ctrl_reset();
  er = 0;
  er_prev = 0;
  er_sum = 0;
  */
}

void run_ctrl_set_arc(run_state_t state, double speed, double dist, double ang_vel, double ang_dist) {
  run_ctrl_set(state, speed, dist);
  ang_vel_ref = ang_vel;
  ang_dist_ref = ang_dist;
}

void run_ctrl_get(run_state_t *state, double *speed, double *dist) {
  *state = run_state;
  *speed = speed_curr;
  *dist = dist_curr;
}

void run_ctrl_get_arc(run_state_t *state, double *speed, double *dist, double *ang_vel, double *ang_dist) {
  *state = run_state;
  *speed = speed_curr;
  *dist = dist_curr;
  *ang_vel = ang_vel_curr;
  *ang_dist = ang_dist_curr;
}
