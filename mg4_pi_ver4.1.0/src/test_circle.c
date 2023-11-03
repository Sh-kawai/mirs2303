#include <stdio.h>
#include <unistd.h>
#include "circle.h"

int main(){
	int i, cg_x, cg_y, ratio, cir_x, cir_y, radius;
	
	if(circle_create() != 0) return -1;
	
	for(i = 0; i < 10; i++){
		circle_get_cg(&cg_x, &cg_y, &ratio);
		circle_get_cir(&cir_x, &cir_y, &radius);
		
		printf("count[%d] : cg_x  = %3d, ratio  = %3d\n", i, cg_x, ratio);
		printf("         : cir_x = %3d, radius = %3d\n", cir_x, radius);
		
		usleep(1000 * 1000);
	}
	
	circle_cancel();
	
	return 0;
}
