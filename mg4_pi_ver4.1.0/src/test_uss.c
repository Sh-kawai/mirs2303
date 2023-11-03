#include <stdio.h>
#include <unistd.h>
#include "uss.h"

int main(){
	long uss_l, uss_r;
	int flag_l = 0, flag_r = 0;
	
	//if(uss_open_l() != 0) return -1;
	//if(uss_open_r() != 0) return -1;
	if(uss_open_l() != 0){
		printf(" left uss open faild !!\n");
		flag_l = -1;
	}
	if(uss_open_r() != 0){
		printf(" right uss open faild !!\n");
		flag_r = -1;
	}
	if( flag_l == -1 && flag_r == -1) return -1;
	
	while(1){
		uss_l = uss_get_l();
		usleep(500 * 1000);
		
		uss_r = uss_get_r();
		usleep(500 * 1000);
		
		printf("uss_l = %6ld, uss_r = %6ld\n", uss_l, uss_r);
		usleep(10 * 1000);
	}
	
	return 0;
}
