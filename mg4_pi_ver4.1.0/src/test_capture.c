#include <stdio.h>
#include "get_img.h"

int main(){
	char buf[256];
	int device;
	
	//カメラデバイスの設定 1台目:0、2台目:1
	printf("device number? [ 0 to 3 ]\n");
	fgets(buf, sizeof(buf), stdin);
	sscanf(buf, "%d", &device);
	
	if(get_img("./img/snap.jpg", device, 320, 240) == 0){
		printf("finished to capture\n");
	}else{
		printf("failed to capture\n");
	}
	return 0;
}
