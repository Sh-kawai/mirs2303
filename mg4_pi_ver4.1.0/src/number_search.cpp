#include <stdio.h>
#include <opencv2/opencv.hpp>
//#include <opencv2/highgui.hpp>
#include "number.h"

// ROI走査(0:黒, 1:白)
int number_search(const cv:: Mat src){
	int x, y, x0, x1, x2, y0, y1, y3, y4;
	int f1 = 0, f2 = 0, f3 = 0, f4 = 0, f5 = 0, f6 = 0, f7 = 0, f8 = 0, f9 = 0;
	int number = -1;
	
	// 矩形エリアをx座標で2つ, y座標で4つに区切る
	x0 = src.cols  * 0/2;
	x1 = src.cols  * 1/2;
	x2 = src.cols  * 2/2;
	y0 = src.rows * 0/4;
	y1 = src.rows * 1/4;
	y3 = src.rows * 3/4;
	y4 = src.rows * 4/4;
	
	//printf("x2 = %d   y4 = %d src.cols=%d \n", x2,y4,src.cols);
	//printf("chanels = %d\n", src.channels());

	// 画面上に数字パターンを表示
	#ifdef __NUMBER_DEBUG__
	for(y = 0; y < src.rows; ++y){
		for(x = 0; x < src.cols; ++x){
			if( src.data[ y * src.step + x * src.elemSize()  ] >= 200){
				printf("1");
			}else{
				printf(" ");
			}
		}
		printf("\n");
	}
	#endif

	// f1
	for(x = x0; x < x1 * 1/2; x++){
		if( src.data[ y1 * src.step + x * src.elemSize()  ] <= 200){
			f1 = 1;
			break;
		}
	}
	
	// f2
	for(x = x1; x < x2; x++){
		if( src.data[ y1 * src.step + x * src.elemSize()  ] <= 200){
			f2 = 1;
			break;
		}
	}
	
	// f3
	for(x = x0; x < x1; x++){
		if( src.data[ y3 * src.step + x * src.elemSize()  ] <= 200){
			f3 = 1;
			break;
		}
	}
	
	// f4
	for(x = x1; x < x2; x++){
		if( src.data[ y3 * src.step + x * src.elemSize()  ] <= 200){
			f4 = 1;
			break;
		}
	}
	
	// f5
	for(y = y0; y < y1; y++){
		if( src.data[ y * src.step + x1 * src.elemSize()  ] <= 200){
			f5 = 1;
			break;
		}
	}
	
	// f6
	for(y = y3; y < y4; y++){
		if( src.data[ y * src.step + x1 * src.elemSize()  ] <= 200){
			f6 = 1;
			break;
		}
	}
	
	// f7
	for(y = y1; y < y3; y++){
		//if( src.data[ x1 + y * src.cols ] >= 200){
		if( src.data[ y * src.step + x1 * src.elemSize()  ] <= 200){
			f7 = 1;
			break;
		}
	}
	
	// f8, f9
	if( src.data[ y1 * src.step + x1 * src.elemSize()  ] <= 200) f8 = 1;
	if( src.data[ y3 * src.step + x1 * src.elemSize()  ] <= 200) f9 = 1;

	#ifdef __NUMBER_DEBUG__
	printf("f1=%d  f2=%d  f3=%d  f4=%d  f5=%d   f6=%d  f7=%d  f8=%d  f9=%d\n", f1,f2,f3,f4,f5,f6,f7,f8,f9);  
	#endif
	
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
