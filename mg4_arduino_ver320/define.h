/* 変数型の定義 */
typedef enum {
  STP = 0,
  STR,
  ROT,
  ARC,
  LINE,
  SER,
  CAM,
} run_state_t;

typedef struct {
  unsigned char val[7];
} serial_data_t;

typedef struct {
  unsigned char val[6];
} middle_data_t;

typedef struct {
  signed short val[3];
} command_data_t;

/* ピン配置 */
// mega interrupt pin(num)
// 2(0) 3(1) 21(2) 20(3) 19(4) 18(5)
#define INTERRUPT_R  3
#define INTERRUPT_L  2
#define INTERRUPT_E  4

#define PIN_ENC_A_R 20
#define PIN_ENC_B_R 28
#define PIN_ENC_A_L 21
#define PIN_ENC_B_L 34
#define PIN_ENC_A_E 19
#define PIN_ENC_B_E 40
#define PIN_DIR_L   46
#define PIN_PWM_L    3
#define PIN_DIR_R   44
#define PIN_PWM_R    2
#define PIN_DIR_E   48
#define PIN_PWM_E    5
#define PIN_SER_Y    4 // 縦 y軸
#define PIN_SER_Z    6 // 横 z軸
#define PIN_SW      10
#define PIN_LED     13
#define PIN_BATT    A5
#define PIN_LIGHT_0 A0
#define PIN_LIGHT_1 A1
#define PIN_LIGHT_2 A2
#define PIN_LIGHT_3 A3
#define PIN_TOUCH_1 1
#define PIN_TOUCH_2 1


/*
#define INTERRUPT_L  0
#define INTERRUPT_R  1

#define PIN_ENC_A_L  2
#define PIN_ENC_B_L  4
#define PIN_ENC_A_R  3
#define PIN_ENC_B_R  7
#define PIN_DIR_R    8
#define PIN_PWM_R    9
#define PIN_DIR_L   12
#define PIN_PWM_L   11
#define PIN_SW      10
#define PIN_LED     13
#define PIN_BATT    19
*/

/* パラメータ */
// 動作周期 [ms]
#define T_CTRL 10 

//直進走行距離ゲイン
#define K_STR_LR 1.003

// タイヤ半径 [cm] 3.2
//#define R_TIRE     4.269
#define R_TIRE    7.4

// タイヤ間隔 [cm] 25.0
//#define D_TIRE    32.0
#define D_TIRE    32.0

// エンコーダ分解能 (A相立上り/立下りを利用するため2倍)
#define ENC_RANGE (13*2) 

// ギア比　（該当するものを選択）
// 1/14 ギア  13 and 212/289
#define GEAR_RATIO 13.734
// 1/19 ギラ  19 and 38/187
//#define GEAR_RATIO 19.203
// 1/27 ギラ  26 and 103/121
//#define GEAR_RATIO 27.851

// 左タイヤに対する右タイヤの回転比
#define L_R_RATIO  1.0 

// バッテリ入力の分圧比
#define V_RATIO 0.5 

// ライントレース白黒
#define BLACK  1010
#define WHITE   960

// 昇降用モーター
// ねじピッチ(隣り合うねじ山の幅)
#define ELEV_PIT 0.2
// エンコーダ分解能
#define ENC_RANGE_E 5

//昇降部分の最大高さ
#define HIGH_MAX 30
