#ifndef __NUMBER__
#define __NUMBER__

#include <cv.h>

//#define __NUMBER_DEBUG__

#define NUM_LEN 1 // 読み取る数字の最大個数

extern int  number_search(const IplImage *img_src);

extern int  number_detect(int dist);
extern void number_set_device(int device);
extern void number_get(int *ans);

#endif
