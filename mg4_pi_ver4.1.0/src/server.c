#include <stdio.h>
#include <stdlib.h>
#include "server.h"

int server_info_number(int num){
	FILE *fp;
	
	if((fp = fopen("info_number.data", "w")) == NULL) return -1;
	fprintf(fp, "%d\n", num);
	fclose(fp);
	
	return system("scp info_number.data mirs@172.21.24.51:./info/");
}
