#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <sys/time.h>

int main(){

        char buf[256];
        int device = 0;
	int width = 640;
	int height = 480;

	//カメラデバイスの設定 1台目:0、2台目:1
        printf("device number? [ 0 to 3 ]\n");
        fgets(buf, sizeof(buf), stdin);
        sscanf(buf, "%d", &device);


        cv::VideoCapture cap(device);//デバイスのオープン
        if(!cap.isOpened())//カメラデバイスが正常にオープンしたか確認．
        {
                //読み込みに失敗したときの処理
                return -1;
        }
        //cap.set(CV_CAP_PROP_FRAME_WIDTH,width);
        //cap.set(CV_CAP_PROP_FRAME_HEIGHT,height);
        cap.set(cv::CAP_PROP_FRAME_WIDTH,width);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT,height);

        //画像を格納するオブジェクト
        cv::Mat frame; 

        //cap.read(frame);
        //cv::imshow("win", frame);//画像を表示．
        //cv::waitKey(2000);


	while(1){
        	cap.read(frame);
        	cv::imshow("win", frame);//画像を表示．
		cv::waitKey(100); //100msec wait
	}


	//cv::waitKey(1000);
        cv::destroyAllWindows();

	return 0;
}
