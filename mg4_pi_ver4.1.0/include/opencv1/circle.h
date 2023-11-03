#ifndef __CIRCLE__
#define __CIRCLE__

#include <cv.h>

//#define __CIRCLE_DEBUG__

extern void color_binarize(const IplImage *img_src, IplImage *img_dst, int code, CvScalar lower, CvScalar upper);

extern int  circle_create();
extern void circle_cancel();
extern void circle_set_device(int device);
extern void circle_get_cg(int *x_g, int *y_g, int *ratio_g);
extern void circle_get_cir(int *x_g, int *y_g, int *radius_g);
extern int  circle_detect();

#endif
