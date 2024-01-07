#include <stdio.h>
#include <unistd.h>
#include "arduino.h"
#include "request.h"

int main(){
	int mode, speed, dist, pit_y, yaw_z, pwm, height, time;
	double volt;
	//char buf[256];
	run_state_t state;
	
	if(arduino_open() != 0) return -1;


	while(1){
		printf("0:stop  1:straight  2:rotate  3:get_mode  4:get_volt 5:servo 6:camera -1:quit\n");
		scanf("%d",&mode);
		
		switch(mode){
		case 0:
			request_set_runmode(STP, 0, 0);
			break;
		case 1:
			printf("speed? [cm/s]\n");
			scanf("%d",&speed);
			printf("dist? [cm]\n");
			scanf("%d",&dist);
			
			request_set_runmode(STR, speed, dist);
			while(1){
				request_get_runmode(&state, &speed, &dist);
				if( state == STP ) break;
			}

			break;
		case 2:
			printf("speed? [deg/s]\n");
			scanf("%d",&speed);
			
			printf("angle? [deg]\n");
			scanf("%d",&dist);
			
			request_set_runmode(ROT, speed, dist);
			while(1){
				request_get_runmode(&state, &speed, &dist);
				if( state == STP ) break;
			}
			break;
		case 3:
			request_get_runmode(&state, &speed, &dist);
			//printf("state = %s\n",((state == STR) ? "STR" : (state == ROT) ? "ROT" : "STP"));
			printf("state = %d\n",state);
			break;
		case 4:
			request_get_batt(&volt);
			printf("batt = %4.2lf\n", volt);
			break;
		case 5:
			printf("pit_y? [deg]\n");
			scanf("%d",&pit_y);
			
			printf("yaw_z? [deg]\n");
			scanf("%d",&yaw_z);
			//request_set_runmode(STR, 10, 10);
			request_set_runmode(SER, pit_y, yaw_z);
			break;
		case 6:
			printf("pwm? (0~255)\n");
			scanf("%d", &pwm);
			printf("time[s]?(under 0 pwm stop) \n");
			scanf("%d", &time);
			//state, height, pwm
			//height=0: pwm値でずっと動作(2秒)
			//pwm=0: 目標高さに制御
			request_set_runmode(CAM, 0, pwm);
			if(time > 0){
				sleep(time);
				request_set_runmode(CAM, 0, 0);
			} else {
				sleep(1);
				while(1){
					request_get_cammode(&state, &height, &pwm);
					if(pwm == 0) break;
					usleep(100 * 1000);
				}
			}
			break;
		case -1:
			return 0;
		default:
			break;
		}
	}
	
	arduino_close();
	return 0;
}
