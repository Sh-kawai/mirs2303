static double d_prev_l = 0.0;
static double d_prev_r = 0.0;

void ros_send_odom(){
  double d_curr_l, d_curr_r;
  double delta_l_m, delta_r_m;
  distance_ros_get(&d_curr_l, &d_curr_r); //[cm]
  
  delta_l_m = (d_curr_l - d_prev_l) / 100.0;
  delta_r_m = (d_curr_r - d_prev_r) / 100.0;
  
  // ΔlとΔrを送る(メートルに換算)
  Serial.print("odom");
  Serial.print(delta_l_m);
  Serial.print(",");
  Serial.print(delta_r_m);
  Serial.println();
}

void ros_reset(){
  d_prev_l = d_prev_r = 0.0;
  encoder_ros_reset();
}
