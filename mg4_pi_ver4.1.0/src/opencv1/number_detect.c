#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include "get_img.h"
#include "number.h"

static int device_cap = 0;
static int numbers[100];

void number_set_device(int device){
	device_cap = device;
}

void number_get(int *ans){
	int i;
	for(i = 0; i < NUM_LEN; i++){
		ans[i] = numbers[i];
	}
}

int number_detect(int dist){
	// 撮影サイズ[pixel]
	const int width_cap  = 320;
	const int height_cap = 240;
	
	// カメラからMIRS中心までの距離[cm]
	const int dist_center = 13;
	
	// カメラから数字ボードまでの標準撮影距離[cm]
	const int dist_std = 50;
	
	// 標準撮影距離にて撮影した数字のサイズ[pixel]
	const int width_std  =  72;
	const int height_std = 128;
	
	// 抽出エリアのレンジ
	const double range = 1.5;
	
	int i, j, number, count_cntr = 0, count_label = 0, count_num = 0;
	int width_min, width_max, height_min, height_max;
	CvMemStorage *storage;
	CvPoint point0, point1;
	CvRect rect[100], rect_temp;
	CvSeq *contour;
	IplImage *img_input, *img_gray, *img_gaus, *img_binr, *img_label, *img_temp;
	
	for(i = 0; i < sizeof(numbers)/sizeof(int); i++){
		numbers[i] = -1;
	}
	
	/* (1)エリアの抽出条件を設定 */
	// 撮影距離をMIRS中心基準からカメラ基準に修正
	dist -= dist_center;
	if(dist <= 0) return -1;
	
	// 数字サイズの判定条件 = 数字サイズ標準値 / (撮影距離/撮影距離標準値) * レンジ^+-1
	width_min  =  width_std * dist_std / dist / range;
	width_max  =  width_std * dist_std / dist * range;
	height_min = height_std * dist_std / dist / range;
	height_max = height_std * dist_std / dist * range;
	
	#ifdef __NUMBER_DEBUG__
	printf("width_min = %d, width_max = %d, height_min = %d, height_max = %d\n", width_min, width_max, height_min, height_max);
	#endif
	
	/* (2)画像のキャプチャ */
	if(get_img("./img/num_input.jpg", device_cap, width_cap, height_cap) != 0) return -1;
	if((img_input = cvLoadImage("./img/num_input.jpg", CV_LOAD_IMAGE_ANYCOLOR)) == NULL) return -1;
	
	/* (3)グレースケール・ガウシアンフィルタ・2値化 */
	img_gray = cvCreateImage(cvGetSize(img_input), IPL_DEPTH_8U, 1);
	img_gaus = cvCreateImage(cvGetSize(img_input), IPL_DEPTH_8U, 1);
	img_binr = cvCreateImage(cvGetSize(img_input), IPL_DEPTH_8U, 1);
	cvCvtColor(img_input, img_gray, CV_BGR2GRAY);
	cvSmooth(img_gray, img_gaus, CV_GAUSSIAN, 5, 0, 0, 0);
	cvThreshold(img_gaus, img_binr, 90, 255, CV_THRESH_BINARY_INV | CV_THRESH_OTSU);
	
	/* (4)画像から矩形の輪郭データを取得 */
	// cvFindContoursで元の画像が書き換えられてしまうので別名のデータにコピーして使う
	storage    = cvCreateMemStorage(0);
	img_temp   = cvCloneImage(img_binr);
	count_cntr = cvFindContours(img_temp, storage, &contour, sizeof(CvContour), CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE, cvPoint(0, 0));
	cvReleaseImage(&img_temp);
	
	for(i = 0; i < count_cntr; i++){
		rect[i] = cvBoundingRect(contour, 1);
		contour = contour->h_next;
	}
	
	/* (5)輪郭データをx座標順にソート (数字の並び順を把握するため) */
	for(i = 0; i < count_cntr-1; i++){
		for(j = count_cntr-1; j > i; j--){
			if(rect[j-1].x > rect[j].x){
				rect_temp = rect[j-1];
				rect[j-1] = rect[j];
				rect[j]   = rect_temp;
			}
		}
	}
	
	#ifdef __NUMBER_DEBUG__
	for(i = 0; i < count_cntr; i++){
		printf("cntr[%2d] : x0 = %3d, y0 = %3d, width = %3d, height = %3d\n", i, rect[i].x, rect[i].y, rect[i].width, rect[i].height);
	}
	#endif
	
	/* (6)条件に沿った輪郭データに注目して数字認識を行う */
	img_label = cvCloneImage(img_input);
	for(i = 0; i < count_cntr; i++){
		point0 = cvPoint(rect[i].x, rect[i].y);
		point1 = cvPoint(rect[i].x + rect[i].width, rect[i].y + rect[i].height);
		
		cvRectangle(img_label, point0, point1, CV_RGB(255, 255, 255), 1, 8, 0);
		
		if((rect[i].width > width_min && rect[i].width < width_max) && (rect[i].height > height_min && rect[i].height < height_max)){
			cvRectangle(img_label, point0, point1, CV_RGB(0, 255, 0), 3, 8, 0);
			
			img_temp = cvCreateImage(cvSize(rect[i].width, rect[i].height), IPL_DEPTH_8U, 1);
			cvSetImageROI(img_binr, rect[i]);
			cvCopyImage(img_binr, img_temp);
			number = number_search(img_temp);
			cvResetImageROI(img_binr);
			cvReleaseImage(&img_temp);
			
			#ifdef __NUMBER_DEBUG__
			printf("label[%2d] (cntr[%2d]) : number = %2d\n", count_label, i, number);
			#endif
			
			count_label++;
			if(number >= 0 && number <= 9){
				numbers[count_num] = number;
				count_num++;
			}
		}
	}
	
	#ifdef __NUMBER_DEBUG__
	printf("detected %d contours, %d labels, %d numbers\n", count_cntr, count_label, count_num);
	#endif
	
	/* (7)加工画像の保存 */
	cvSaveImage("./img/num_gray.jpg", img_gray, NULL);
	cvSaveImage("./img/num_gaus.jpg", img_gaus, NULL);
	cvSaveImage("./img/num_binr.jpg", img_binr, NULL);
	cvSaveImage("./img/num_label.jpg", img_label, NULL);
	
	/* (8)メモリの開放 */
	cvReleaseImage(&img_input);
	cvReleaseImage(&img_gray);
	cvReleaseImage(&img_gaus);
	cvReleaseImage(&img_binr);
	cvReleaseImage(&img_label);
	cvReleaseMemStorage(&storage);
	
	return count_num;
}
