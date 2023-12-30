void slave() {
  double speed, dist, dist_l, dist_r;
  double ang_vel, ang_dist;
  run_state_t state;
  command_data_t command_data;

  while (1) {
    double batt = io_get_batt();
    /*if (batt < 6.5) {
      Serial.print("low battery = ");
      Serial.println(batt);
      run_ctrl_set(STP, 0, 0);
      delay(T_CTRL);
      continue;
    }*/
    if (raspi_receive(&command_data) == 0) {
      Serial.println(command_data.val[0]);
      switch (command_data.val[0]) {
        case -1: // シリアル通信テスト
          test_serial(command_data.val[1], command_data.val[2]);
          break;
        case 1: // 停止
          run_ctrl_set(STP, 0, 0);
          break;
        case 2: //　直進運動
          Serial.println("STR");
          run_ctrl_set(STR, command_data.val[1], command_data.val[2]);
          break;
        case 3: // 回転運動
          Serial.println("ROT");
          run_ctrl_set(ROT, command_data.val[1], command_data.val[2]);
          break;
        case 4: // 円弧運動
          Serial.println("ARC");
          dist = 1000.0;
          ang_dist = 1000.0;
          run_ctrl_set_arc(ARC, command_data.val[1], dist, command_data.val[2], ang_dist);
          break;
        case 5: // ライントレース
          Serial.println("LINE");
          run_ctrl_set(LINE, command_data.val[1], command_data.val[2]);
          break;
        case 6: // サーボモーター
          Serial.println("SER");
          servo_set(command_data.val[1], command_data.val[2]);
          break;
        case 7: // 昇降用モーター
          Serial.println("CAM");
          camera_ctrl_set(command_data.val[1], command_data.val[2]);
          break;
        case 10:
          run_ctrl_get(&state, &speed, &dist);
          command_data.val[0] = ((state == STR) ? 2 : (state == ROT) ? 3 : 1);
          command_data.val[1] = (short)speed;
          command_data.val[2] = (short)dist;
          raspi_send(command_data);
          break;
        case 11:
          distance_get(&dist_l, &dist_r);
          command_data.val[0] = (short)dist_l;
          command_data.val[1] = (short)dist_r;
          raspi_send(command_data);
          break;
        case 12:
          command_data.val[0] = (short)(io_get_batt() * 100.0);
          raspi_send(command_data);
          break;
        default:
          break;
      }
    }
    run_ctrl_execute();
    vel_ctrl_execute();
    camera_ctrl_execute();
    delay(T_CTRL);
  }
}
