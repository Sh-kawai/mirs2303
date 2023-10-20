#include <stdio.h>
#include "arduino.h"
#include "direction.h"
#include "number.h"
#include "uss.h"

int main(){
	int i, dist;
	int ans[NUM_LEN];
	char buf[256];
	
	//if(io_open() != 0) return -1;
	if(arduino_open() != 0) return -1;
	if(uss_open_l() != 0) return -1;
	if(uss_open_r() != 0) return -1;
	
	printf("dist? [cm]\n");
	fgets(buf, sizeof(buf), stdin);
	sscanf(buf, "%d", &dist);
	
	if(direction_correct(dist) == 0){
		printf("finished to correct\n");
	}else{
		printf("failed to correct\n");
	}
	
	number_detect(dist);
	number_get(ans);
	
	for(i = 0; i < NUM_LEN; i++){
		printf("number[%d] = %d\n", i, ans[i]);
	}
	
	arduino_close();
	return 0;
}
