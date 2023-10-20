#include <stdio.h>
#include "number.h"

int main(){
	int i, dist;
	int ans[NUM_LEN];
	char buf[256];
	
	printf("dist? [cm]\n");
	fgets(buf, sizeof(buf), stdin);
	sscanf(buf, "%d", &dist);
	
	number_detect(dist);
	number_get(ans);
	
	for(i = 0; i < NUM_LEN; i++){
		printf("number[%d] = %d\n", i, ans[i]);
	}
	
	return 0;
}
