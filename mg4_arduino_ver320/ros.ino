static double d_prev_l = 0.0;
static double d_prev_r = 0.0;

static double linear_x = 0.0;
static double angular_z = 0.0;
static double vel_r = 0.0;
static double vel_l = 0.0;

void ros_send_odom(){
  double d_curr_l, d_curr_r;
  double delta_l_m, delta_r_m;
  distance_ros_get(&d_curr_l, &d_curr_r); //[cm]
  
  delta_l_m = (d_curr_l - d_prev_l) / 100.0;
  delta_r_m = (d_curr_r - d_prev_r) / 100.0;
  
  // ΔlとΔrを送る(メートルに換算)
  Serial.print("rosodom");
  Serial.print(delta_l_m);
  Serial.print(",,,");
  Serial.print(delta_r_m);
  Serial.println();
}

void ros_serial_recv(){
  if(Serial.available() > 0){
    String receivedData = Serial.readStringUntil('\n');

    int rosIndex = receivedData.indexOf("rosvel");
    int rosNum = 6;
    int commandIndex = receivedData.indexOf(",,,");
    int commandNum = 3;

    if(commandIndex != -1){
      String linear_x_str = receivedData.substring(rosNum, commandIndex);
      String angular_z_str = receivedData.substring(commandIndex + commandNum);

      linear_x = linear_x_str.toDouble() / 1000.0;
      angular_z = angular_z_str.toDouble() / 1000.0;
    } else {
      linear_x = 0.0;
      angular_z = 0.0;
    }
    /*Serial.print("x:");
    Serial.print(linear_x);
    Serial.print(", z:");
    Serial.println(angular_z);*/
  }
}

void ros_recv_vel(){
  float wh_rad = R_TIRE / 100.0;
  float wh_sep = D_TIRE / 100.0;
  
  ros_serial_recv();

  vel_r = (linear_x/wh_rad) + ((angular_z*wh_sep)/(2.0*wh_rad));
  vel_l = (linear_x/wh_rad) - ((angular_z*wh_sep)/(2.0*wh_rad));

  vel_ctrl_set(vel_l, vel_r);
  
  Serial.print("r:");
  Serial.print(vel_r);
  Serial.print("[cm/s], l:");
  Serial.print(vel_l);
  Serial.println("[cm/s]");
}

void ros_reset(){
  d_prev_l = d_prev_r = 0.0;
  encoder_ros_reset();
}
