#ifndef __NUMBER__
#define __NUMBER__

#include <opencv2/opencv.hpp>

#define __NUMBER_DEBUG__

#define NUM_LEN 1 // 読み取る数字の最大個数

extern int  number_detect(int dist);
extern int  number_search(const cv::Mat img_src);
extern void number_set_device(int device);
extern void number_get(int *ans);

#endif
