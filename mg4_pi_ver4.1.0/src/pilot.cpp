#include <stdio.h>
#include <unistd.h>
#include "arduino.h"
#include "io.h"
#include "request.h"
#include "uss.h"
#include "jetson_socket.h"
#include "keyboard.h"

int main(){
	double volt;
	run_state_t state;
	int speed_curr, dist_curr;
	Server Jetson(HOST, PORT);
	
	if(io_open() != 0) return -1;
	if(arduino_open() != 0) return -1;
	//if(uss_open_l() != 0) return -1;
	//if(uss_open_r() != 0) return -1;
	if(Jetson.s_open() != 0) return -1;
	
	printf("press enter to start\n");
	getchar();
	
	while(1){
		// ライントレース
		request_set_runmode(LINE, 25, 100);
		usleep(10 * 1000);
		while(1) {
			request_get_runmode(&state, &speed_curr, &dist_curr);
			if(state = STP) break;
			usleep(100 * 1000);
		}

		// 撮影処理
		// 昇降機構 書く
		// サーボ 書く
		// 撮影
		Jetson.round_trip("p1");



		break;
	}
	
	arduino_close();
	return 0;
}
