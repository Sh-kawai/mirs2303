 /*
  Ver1.0からの変更点　　　RaspberryPi と２バイトデータのシリアル通信をできるようにした 
  Ver2.0からの変更点　　　RaspberryPi とのシリアル通信の速度を9600bps から 115200bpsに変更した
 */

#include <Servo.h>
#include "define.h"

void setup() {
  io_open();
  encoder_open();
  motor_open();
  servo_open();
  camera_ctrl_open();
  raspi_open();
}

void loop() { 
  /*
  いずれか一つの関数を有効にする。
  どの関数も無限ループになっている。しがたってこの loop 関数は実際にはループしない。
  */

  /* RasPi からの指令で動作させるとき、slave を有効にする。*/
  //slave();
  
  /* --------------機能のテスト---------------------------------------------
    テスト関数 test_*() のいずれかを有効にする。
    実行時にシリアルモニタを立ち上げて値を確認する。
  ------------------------------------------------------------------------- */

  /* モータ動作テスト 引数：左モータのPWM値、右モータのPWM値　（範囲は -255～255）*/
  //test_motor(50, 50);
  
  //エンコーダ(AB相)
  //test_enc_l();
  //test_enc_e();

  /* エンコーダテスト（モータを回転させて行う）*/
  //motor_set(-50, -50) ;test_encoder();
  /* 距離計のテスト（モータを回転させて行う）*/
  //motor_set(50, 50) ; test_distance();

  /* 速度制御のテスト　引数：左モータの速度[cm/s]、右モータの速度[cm/s] */
  //test_vel_ctrl(-25, -25);
  /* 走行制御のテスト　
    引数：モード（直進：STR or 回転：ROT or ライントレース:LINE)、速度[cm/s] or 角速度[deg/s]、距離[cm] or 角度 の速度[deg] 
    距離 > 0 ：前進、角度 < 0 ：後退　（速度は常に > 0）
    角度 > 0 ：反時計回り、角度 < 0 ：時計回り　（角速度は常に > 0）
  */
  //test_run_ctrl(STR, 25, 50);
  //test_run_ctrl(ROT,60, 3600);
  //test_run_ctrl(LINE, 20, 1000);
  
  //test_lintrace(20);

  /*円弧運動テスト 引数：直進距離[cm]、直進速度[cm/s]、回転角度[rad]、回転速度[deg/s] */
  //test_arc_move(10, 100, 45 ,90);
  //test_arc_move_sim(100);
  
  /*サーボモーターテスト*/
  //test_servo(0, 0);
  /* 引数: 最小角度[度], 最大角度[度, 角速度 */
  //test_servo_rot(0, 60, 1);
  
  /*フォトリフレクタ*/
  //test_get_light();

  /*昇降用モータ*/
  /*pwm指定制御　引数:pwm値(int)*/
  //test_camera_ctrl_motor(-255);
  /*高さ指定制御　引数:目標高さ[cm](0以上)*/
  //test_camera_ctrl_height(-10000.0);
  //test_camera_max();
  //test_camera_touch();

  //test_io_cam();

  /* バッテリー値の確認 */
  test_batt();

  /* シリア通信のエンコード、デコーダ値の確認 */
  //test_encode();
  //test_decode();

  /* ros slam */
  //test_ros();
}
