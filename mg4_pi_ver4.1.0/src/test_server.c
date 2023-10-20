#include <stdio.h>
#include "server.h"

int main(){
	int num;
	char buf[256];
	
	printf("number?\n");
	fgets(buf, sizeof(buf), stdin);
	sscanf(buf, "%d", &num);
	
	if(server_info_number(num) == 0){
		printf("finished to upload\n");
	}else{
		printf("failed to upload\n");
	}
	
	return 0;
}
