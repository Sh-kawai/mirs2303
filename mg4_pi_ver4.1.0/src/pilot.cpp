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
	Server Jetson(HOST, PORT);
	
	if(io_open() != 0) return -1;
	if(arduino_open() != 0) return -1;
	//if(uss_open_l() != 0) return -1;
	//if(uss_open_r() != 0) return -1;
	if(Jetson.s_open() != 0) return -1;
	
	printf("press enter to start\n");
	getchar();
	
	while(1){
		// 処理を記述
		request_set_runmode(STR, 25, 100);
		break;
	}
	
	arduino_close();
	return 0;
}
