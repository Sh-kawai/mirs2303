#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include "number.h"

// ROI走査(0:黒, 1:白)
int number_search(const IplImage *img_src){
	int x, y, x0, x1, x2, y0, y1, y3, y4;
	int f1 = 0, f2 = 0, f3 = 0, f4 = 0, f5 = 0, f6 = 0, f7 = 0, f8 = 0, f9 = 0;
	int number = -1;
	
	// 矩形エリアをx座標で2つ, y座標で4つに区切る
	x0 = img_src->width  * 0/2;
	x1 = img_src->width  * 1/2;
	x2 = img_src->width  * 2/2;
	y0 = img_src->height * 0/4;
	y1 = img_src->height * 1/4;
	y3 = img_src->height * 3/4;
	y4 = img_src->height * 4/4;
	
	// f1
	for(x = x0; x < x1 * 1/2; x++){
		if(img_src->imageData[x + y1 * img_src->widthStep] == 255){
			f1 = 1;
			break;
		}
	}
	
	// f2
	for(x = x1; x < x2; x++){
		if(img_src->imageData[x + y1 * img_src->widthStep] == 255){
			f2 = 1;
			break;
		}
	}
	
	// f3
	for(x = x0; x < x1; x++){
		if(img_src->imageData[x + y3 * img_src->widthStep] == 255){
			f3 = 1;
			break;
		}
	}
	
	// f4
	for(x = x1; x < x2; x++){
		if(img_src->imageData[x + y3 * img_src->widthStep] == 255){
			f4 = 1;
			break;
		}
	}
	
	// f5
	for(y = y0; y < y1; y++){
		if(img_src->imageData[x1 + y * img_src->widthStep] == 255){
			f5 = 1;
			break;
		}
	}
	
	// f6
	for(y = y3; y < y4; y++){
		if(img_src->imageData[x1 + y * img_src->widthStep] == 255){
			f6 = 1;
			break;
		}
	}
	
	// f7
	for(y = y1; y < y3; y++){
		if(img_src->imageData[x1 + y * img_src->widthStep] == 255){
			f7 = 1;
			break;
		}
	}
	
	// f8, f9
	if(img_src->imageData[x1 + y1 * img_src->widthStep] == 255) f8 = 1;
	if(img_src->imageData[x1 + y3 * img_src->widthStep] == 255) f9 = 1;
	
	// 数字判別
	if(f1==1 && f2==1 && f3==1 && f4==1 && f5==1 && f6==1 && f7==0) number = 0;
	if(f1==0 && f2==1 && f3==1 && f4==0 && f5==1 && f6==1 && f7==1) number = 2;
	if(f1==0 && f2==1 && f3==0 && f4==1 && f5==1 && f6==1 && f7==1) number = 3;
	if(f1==1 && f2==1 && f3==0 && f4==1 && f5==0 && f6==0 && f7==1) number = 4;
	if(f1==1 && f2==0 && f3==0 && f4==1 && f5==1 && f6==1 && f7==1) number = 5;
	if(f1==1 && f2==0 && f3==1 && f4==1 && f5==1 && f6==1 && f7==1) number = 6;
	if(f1==1 && f2==1 && f3==0 && f4==1 && f5==1 && f6==0 && f7==0) number = 7;
	if(f1==1 && f2==1 && f3==0 && f4==1 && f5==1 && f6==1 && f7==1) number = 9;
	
	// 1と8の判別
	if(f1==1 && f2==1 && f3==1 && f4==1 && f5==1 && f6==1 && f7==1){
		number = 8;
		if(f8==1 || f9==1) number = 1;
		if((double)(x2 - x0) / (y4 - y0) < 0.3) number = 1;
	}
	
	return number;
}
