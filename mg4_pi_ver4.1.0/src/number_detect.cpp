#include <stdio.h>
#include <opencv2/opencv.hpp>
//#include <opencv2/highgui.hpp>

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
	//const int width_cap  = 640;
	//const int height_cap = 480;
	
	// カメラからMIRS中心までの距離[cm]
	//const int dist_center = 13;
	const int dist_center = 0;
	
	// カメラから数字ボードまでの標準撮影距離[cm]
	const int dist_std = 50;
	
	// 標準撮影距離にて撮影した数字のサイズ[pixel]
	const int width_std  =  72;
	const int height_std = 128;
	
	// 抽出エリアのレンジ
	const double range = 1.5;
	
	int i, j, number, count_label = 0, count_num = 0;
	int width_min, width_max, height_min, height_max;

	printf("Start number_detect \n");

	cv::Mat img_input, img_gray, img_gaus, img_binr, img_label, img_temp;
	
	for(i = 0; i < (int)(sizeof(numbers)/sizeof(int)); i++){
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
	
	// (2)画像のキャプチャ 
	if(get_img("img/img_input.jpg", device_cap, width_cap, height_cap) != 0) return -1;
	img_input = cv::imread("img/img_input.jpg");
	//img_input = cv::imread("img/snap2.jpg");

	#ifdef __NUMBER_DEBUG__
    	cv::imshow( "Input image", img_input );
    	cv::waitKey(0);
	#endif
	
	// (3)グレースケール・ガウシアンフィルタ・2値化

	//グレースケール
	cv::cvtColor(img_input, img_gray, cv::COLOR_BGR2GRAY);
	#ifdef __NUMBER_DEBUG__
    	cv::imshow( "GRAY", img_gray );
    	cv::waitKey(0);
	#endif

	//ガウシアンフィルタ
	cv::GaussianBlur(img_gray, img_gaus, cv::Size(5, 5), 0.0);
	#ifdef __NUMBER_DEBUG__
    	cv::imshow( "Gussian Filterd", img_gaus );
    	cv::waitKey(0);
	#endif

	// 2値化処理（判別分析2値化法（大津の方法））
	cv::threshold(img_gaus, img_binr, 0, 255, cv::THRESH_OTSU);
	#ifdef __NUMBER_DEBUG__
    	cv::imshow( "BINARY", img_binr );
    	cv::waitKey(0);
	#endif
	
	// (4)画像から矩形の輪郭データを取得 

	std::vector< std::vector<cv::Point> > contours;
	std::vector<cv::Vec4i> hierarchy;

	img_temp = img_binr.clone();

	//輪郭データを取得
	//cv::findContours(img_temp, contours, hierarchy, CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE);
	cv::findContours(img_temp, contours, hierarchy, cv::RETR_LIST, cv::CHAIN_APPROX_SIMPLE);

	//抽出された輪郭の数
	//std::size_t count_cntr; 
	int count_cntr; 
	count_cntr = contours.size();
	//printf("count_cntr = %d\n", count_cntr) ;

	std::vector< cv::Point>  rect_i;
	
	//cv::Rect (始点x, 始点y, 幅, 高さ)の情報持つオブジェクト
	cv::Rect rect[100], rect_temp;

	// 点群に外接する傾いていない矩形を取得
	for(i = 0; i < count_cntr ; i++ ){
		rect_i = contours[i];
		rect[i] = cv::boundingRect(rect_i) ;
		//printf("rect[i].x = %d\n", rect[i].x) ;
	}

	//return 0;
	
	// (5)輪郭データをx座標順にソート (数字の並び順を把握するため) 
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

	
	// (6)条件に沿った輪郭データに注目して数字認識を行う 
	cv::Point point0, point1;
	img_label = img_input.clone();
	for(i = 0; i < count_cntr; i++){
		point0 = cv::Point(rect[i].x, rect[i].y);
		point1 = cv::Point(rect[i].x + rect[i].width, rect[i].y + rect[i].height);
		
		cv::rectangle(img_label, point0, point1, CV_RGB(255, 255, 255), 1, 8, 0);
		#ifdef __NUMBER_DEBUG__
    		//cv::imshow( "Rectangle", img_label );
    		//cv::waitKey(0);
		#endif
		
		if((rect[i].width > width_min && rect[i].width < width_max) && (rect[i].height > height_min && rect[i].height < height_max)){

			#ifdef __NUMBER_DEBUG__
			// 数字ボードの大きさに合致する四角形を太い緑で囲う
			cv::rectangle(img_label, point0, point1, CV_RGB(0, 255, 0), 3, 8, 0);
    			cv::imshow( "LB Rectangle", img_label );
    			cv::waitKey(0);
			#endif

			cv::Rect roi(rect[i].x, rect[i].y, rect[i].width, rect[i].height );
			cv::Mat img_binr_roi = img_binr(roi);

			#ifdef __NUMBER_DEBUG__
    			cv::imshow( "BINR_ROI", img_binr_roi );
    			cv::waitKey(0);
			#endif

			cv::imwrite("./img/img_binr_roi.jpg", img_binr_roi);
			//return 0;

			number = number_search(img_binr_roi);
			
			//#ifdef __NUMBER_DEBUG__
			printf("label[%2d] (cntr[%2d]) : number = %2d\n", count_label, i, number);
			//#endif
			
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

	
	// (7)加工画像の保存 

	#ifdef __NUMBER_DEBUG__
	cv::imwrite("./img/img_gray.jpg", img_gray);
	cv::imwrite("./img/img_gaus.jpg", img_gaus);
	cv::imwrite("./img/img_binr.jpg", img_binr);
	cv::imwrite("./img/img_label.jpg", img_label);
	#endif
	
	// 数字として認識された画像の数を返す
	return count_num;
}
