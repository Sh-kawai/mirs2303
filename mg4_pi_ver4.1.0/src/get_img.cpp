#include <unistd.h>
#include <opencv2/opencv.hpp>
#include "get_img.h"

int get_img(const char *filename, int device, int width, int height){

	cv::VideoCapture cap(device);//デバイスのオープン
	//cap.open(0);//こっちでも良い．

	if(!cap.isOpened())//カメラデバイスが正常にオープンしたか確認．
	{
		//読み込みに失敗したときの処理
		return -1;
	}


	//画像サイズの設定（幅と高さ）
	//cap.set(CV_CAP_PROP_FRAME_WIDTH,width);
	//cap.set(CV_CAP_PROP_FRAME_HEIGHT,height);
	cap.set(cv::CAP_PROP_FRAME_WIDTH,width);
	cap.set(cv::CAP_PROP_FRAME_HEIGHT,height);

	//画像を格納するオブジェクト
	cv::Mat frame; 

	// 1フレームを取り込む
	cap.read(frame);
	cv::imwrite(filename, frame);

	#ifdef __GET_IMG_DEBUG__
	cv::imshow("win", frame);//画像を表示．
	cv::waitKey(1000);
	cv::destroyAllWindows();
	#endif

	return 0;

}
