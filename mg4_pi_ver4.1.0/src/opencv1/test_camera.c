#include <stdio.h>
#include <opencv/highgui.h>
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

	CvCapture *capture = cvCreateCameraCapture(device);
	if(capture == NULL){
		return -1;
	}

	cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_WIDTH,width);
	cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_HEIGHT,height);

	char name[] = "usbcam";
	cvNamedWindow(name,CV_WINDOW_AUTOSIZE);

	IplImage *image;

	while(cvWaitKey(1) == -1){
		image = cvQueryFrame(capture);
		cvShowImage(name,image);
	}

	cvDestroyWindow(name);
	cvReleaseCapture(&capture);

	return 0;
}
