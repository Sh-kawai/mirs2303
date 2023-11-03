#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <cv.h>
#include <highgui.h>
#include "circle.h"
#include "get_img.h"

static void *thread_code(void*);
static pthread_t task_id;

// デバイス番号
static int device_cap = 0;

// 2値化にて1としたエリアの割合[%]と重心座標[pixel]
static int cg_x = -1;
static int cg_y = -1;
static int ratio = 0;

// 検出した円の中心座標[pixel]と半径[pixel]
static int cir_x = -1;
static int cir_y = -1;
static int radius = 0;

void *thread_code(void *t){
	// 実行周期[ms]
	const int t_circle = 10;
	
	while(1){
		circle_detect();
		usleep(t_circle * 1000);
	}
	
	return 0;
}

int circle_create(){
	int policy;
	struct sched_param param;
	
	// スレッドの生成
	if(pthread_create(&task_id, NULL, thread_code, NULL) != 0){
		printf("failed to create circle thread\n");
		return -1;
	}
	
	// スレッドパラメータの確認
	pthread_getschedparam(task_id, &policy, &param);
	printf("circle thread created (plicy = %s, priority = %d)\n",
		((policy == SCHED_FIFO) ? "SCHED_FIFO" : (policy == SCHED_RR) ? "SCHED_RR" : (policy == SCHED_OTHER) ? "SCHED_OTHER" : "???"),
		param.sched_priority);
	
	return 0;
}

void circle_cancel(){
	pthread_cancel(task_id);
	printf("circle thread canceled\n");
}

void circle_set_device(int device){
	device_cap = device;
}

void circle_get_cg(int *x_g, int *y_g, int *ratio_g){
	*x_g = cg_x;
	*y_g = cg_y;
	*ratio_g = ratio;
}

void circle_get_cir(int *x_g, int *y_g, int *radius_g){
	*x_g = cir_x;
	*y_g = cir_y;
	*radius_g = radius;
}

int circle_detect(){
	// 撮影サイズ[pixel]
	const int width_cap  = 320;
	const int height_cap = 240;
	
	// 2値化パラメータ
	// ch0 = Hue        (0～360)
	// ch1 = Saturation (0～255)
	// ch2 = Brightness (0～255)
	// ch3 = 未使用
	CvScalar lower = cvScalar(0, 0, 0, 0);
	CvScalar upper = cvScalar(5, 255, 255, 0);
	
	// 円検出における中心座標間の最小間隔[pixel]
	// 小さすぎると正しく抽出されるべき円の近傍に間違った円が検出される
	// 逆に大きすぎると円検出に失敗する
	const int min_dist = 50;
	
	// Cannyのエッジ検出器で用いる二つの閾値の高い方の値
	// 低い方はこの値を1/2したものになる
	const int param1 = 20;
	
	// 中心検出計算時の閾値
	// これに対応する値が大きい円から順に検出される
	// 小さすぎると誤検出が多くなる
	const int param2 = 25;
	
	// 検出すべき円の最小半径[pixel]
	const int min_radius = 20;
	
	int i, x, y, count_val = 0, count_cir = 0;
	long x_sum = 0, y_sum = 0;
	float *p;
	CvMemStorage *storage;
	CvSeq *circles;
	IplImage *img_input, *img_binr, *img_gaus, *img_label;
	
	/* (1)画像のキャプチャ */
	if(get_img("./img/cir_input.jpg", device_cap, width_cap, height_cap) != 0) return -1;
	if((img_input = cvLoadImage("./img/cir_input.jpg", CV_LOAD_IMAGE_ANYCOLOR)) == NULL) return -1;
	
	/* (2)赤色を抽出して2値化する */
	img_binr = cvCreateImage(cvGetSize(img_input), IPL_DEPTH_8U, 1);
	color_binarize(img_input, img_binr, CV_BGR2HSV, lower, upper);
	
	/* (3)2値化で1と判定された面積の比率とその重心座標を求める */
	for(y = 0; y < img_binr->height; y++){
		for(x = 0; x < img_binr->width; x++){
			if(img_binr->imageData[x + img_binr->widthStep * y] > 0){
				x_sum += x;
				y_sum += y;
				count_val++;
			}
		}
	}
	
	ratio = count_val * 100 / (img_binr->width * img_binr->height);
	if(count_val != 0){
		cg_x = x_sum / count_val;
		cg_y = y_sum / count_val;
	}else{
		cg_x = -1;
		cg_y = -1;
	}
	
	/* (4)Hough変換のための前処理 (画像の平滑化を行なわないと誤検出が発生しやすい) */
	img_gaus = cvCreateImage(cvGetSize(img_input), IPL_DEPTH_8U, 1);
	cvSmooth(img_binr, img_gaus, CV_GAUSSIAN, 11, 11, 0, 0);
	
	/* (5)Hough変換で円を検出し座標を取得する (param2 に敏感) */
	storage   = cvCreateMemStorage(0);
	circles   = cvHoughCircles(img_gaus, storage, CV_HOUGH_GRADIENT, 1, min_dist, param1, param2, min_radius, MAX(img_gaus->width, img_gaus->height));
	count_cir = circles->total;
	img_label = cvCloneImage(img_input);
	
	if(count_cir > 0){
		//for(i = 0; i < count_cir; i++)
		for(i = 0; i < 1 ; i++)
		{
			p = (float *)cvGetSeqElem(circles, i);
			cir_x = cvRound(*p);
			cir_y = cvRound(*(p+1));
			radius = cvRound(*(p+2));
			
			cvCircle(img_label, cvPoint(cir_x, cir_y), 3, CV_RGB(0, 255, 0), -1, 8, 0);
			cvCircle(img_label, cvPoint(cir_x, cir_y), radius, CV_RGB(255, 0, 0), 3, 8, 0);
		}
	}else{
		cir_x = -1;
		cir_y = -1;
		radius = 0;
	}
	
	#ifdef __CIRCLE_DEBUG__
	printf("cg_x  = %3d, cg_y  = %3d, ratio  = %3d\n", cg_x, cg_y, ratio);
	printf("cir_x = %3d, cir_y = %3d, radius = %3d\n", cir_x, cir_y, radius);
	#endif
	
	/* (6)加工画像の表示と保存 */
	#ifdef __CIRCLE_DEBUG__
	cvNamedWindow("window", 1);
	cvShowImage("window", img_label);
	cvWaitKey(500);
	//cvDestroyWindow("window");
	#endif
	
	cvSaveImage("./img/cir_binr.jpg", img_binr, NULL);
	cvSaveImage("./img/cir_gaus.jpg", img_gaus, NULL);
	cvSaveImage("./img/cir_label.jpg", img_label, NULL);
	
	/* (7)メモリの開放 */
	cvReleaseImage(&img_input);
	cvReleaseImage(&img_binr);
	cvReleaseImage(&img_gaus);
	cvReleaseImage(&img_label);
	cvReleaseMemStorage(&storage);
	
	return count_cir;
}
