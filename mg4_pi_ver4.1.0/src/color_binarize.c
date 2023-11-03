#include <stdio.h>
#include <cv.h>
#include <highgui.h>

/*
---------------------------------------------------------------
【関数名】 : color_binarize
【概要  】 : 色空間を用いた2値化
【引数  】 : img_src = 入力画像 (8bit符号なし3ch)
           : img_dst = 出力画像 (8bit符号なし1ch)
           : code    = 色空間の指定 (CV_BGR2HSV, CV_BGR2Labなど)
           : lower   = ch毎の閾値 (備考参照)
           : upper   = ch毎の閾値 (備考参照)
【備考  】 : lower <= upperの場合, lower以上upper以下の範囲を抽出
           : lower >  upperの場合, upper以下lower以上の範囲を抽出
---------------------------------------------------------------
*/

void color_binarize(const IplImage *img_src, IplImage *img_dst, int code, CvScalar lower, CvScalar upper){
	int i, k;
	CvScalar scalar = cvScalarAll(0);
	CvMat *lut;
	IplImage *img_color, *img_ch[3];
	
	/* (1)2値化条件を表すLUTの作成 (256行*1列, 8bit符号なし3ch) */
	lut = cvCreateMat(256, 1, CV_8UC3);
	for(i = 0; i < 256; i++){
		for(k = 0; k < 3; k++){
			if(lower.val[k] <= upper.val[k]){
				if((lower.val[k] <= i) && (i <= upper.val[k])){
					scalar.val[k] = 255;
				}else{
					scalar.val[k] = 0;
				}
			}else{
				if((i <= upper.val[k]) || (lower.val[k] <= i)){
					scalar.val[k] = 255;
				}else{
					scalar.val[k] = 0;
				}
			}
		}
		
		cvSet1D(lut, i, scalar);
	}
	
	/* (2)codeに基づいたカラー変換 */
	img_color = cvCreateImage(cvGetSize(img_src), img_src->depth, 3);
	cvCvtColor(img_src, img_color, code);
	
	/* (3)LUT変換による2値化 */
	cvLUT(img_color, img_color, lut);
	
	/* (4)2値化画像をch毎に分解 */
	img_ch[0] = cvCreateImage(cvGetSize(img_color), img_color->depth, 1);
	img_ch[1] = cvCreateImage(cvGetSize(img_color), img_color->depth, 1);
	img_ch[2] = cvCreateImage(cvGetSize(img_color), img_color->depth, 1);
	cvSplit(img_color, img_ch[0], img_ch[1], img_ch[2], NULL);
	
	/* (5)全chのANDを取る */
	cvZero(img_dst);
	cvAnd(img_ch[0], img_ch[1], img_dst, NULL);
	cvAnd(img_dst,   img_ch[2], img_dst, NULL);
	
	/* (6)メモリの解放 */
	cvReleaseImage(&img_color);
	cvReleaseImage(&img_ch[0]);
	cvReleaseImage(&img_ch[1]);
	cvReleaseImage(&img_ch[2]);
	cvReleaseMat(&lut);
}
