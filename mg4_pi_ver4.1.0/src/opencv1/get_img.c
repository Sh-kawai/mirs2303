#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <opencv/highgui.h>
#include "get_img.h"

int get_img(const char *filename, int device, int width, int height){

        CvCapture *capture = cvCreateCameraCapture(device);
        if(capture == NULL){
                return -1;
        }

	//画像サイズの設定（幅と高さ）	
	cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_WIDTH,width);
        cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_HEIGHT,height);

        char name[] = "usbcam";
        cvNamedWindow(name,CV_WINDOW_AUTOSIZE);

        IplImage *image;

//      画像の取り込みと保存
        image = cvQueryFrame(capture);
        cvSaveImage(filename, image, 0);
	
	return 0;
}
