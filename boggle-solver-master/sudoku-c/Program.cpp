#include "opencv2/opencv.hpp"
#include <omp.h>
#include "FindNumbers.h"
using namespace cv;


int main(int argc, char** argv)
{
    VideoCapture cap;
    // open the default camera, use something different from 0 otherwise;
    // Check VideoCapture documentation.
    if(!cap.open(0))
        return 0;
    Mat frame;
    cap >> frame;
    int centerX = frame.size().width/2;
    int centerY = frame.size().height/2;
    int x1 = centerX - 170;
	int y1 = centerY - 170;
	int x2 = centerX + 170;
	int y2 = centerY + 170;
    cv::Point pt1(x1,y1); //was startPoint and endpoint
    cv::Point pt2(x2,y2);
    FindNumbers findNum;
    int font = cv::FONT_HERSHEY_SIMPLEX;
    int fontScale = 1;
    int color[3] = {255, 0, 0};
    int thickness = 2;
    int result[81] = {0};
    Mat img = frame;
    Mat cropped = frame;
    Mat gray = frame;
    int oldResult[81] = {0};
    int reallyOldResult[81] = {0};
    while (true)
    {
        cap >> frame;

		cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
		cv::rectangle(frame, pt1, pt2, cv::Scalar(255,0,0), 10);
        
        if( frame.empty() ) break; // end of video stream
        imshow("this is you, smile! :)", frame);
        if( waitKey(1) == 27 ) break; // stop capturing by pressing ESC 



        
        if( gray.empty() ) break; // end of video stream
        gray = gray(Rect(pt1, pt2));
        imshow(" gray! :)", gray);
        if( waitKey(2) == 27 ) break; // stop capturing by pressing ESC 
        //findNum.extractSudoku(gray);
        
        if( gray.empty() ) break; // end of video stream
        imshow("This is awesome :)", findNum.parseGrid(gray));
        if( waitKey(3) == 27 ) break;
        /*frame = cv2.putText(frame, 'Align sudoku board with square', org, font,  
		fontScale, color, thickness, cv2.LINE_AA) 
		gray = gray[y1:y2, x1:x2]
		cv2.imshow('Original',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		cv2.imshow('Original2',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		if (queue.qsize() < 10):
			queue.put((gray, result, cropped))*/
    }

    // the camera will be closed automatically upon exit
    // cap.close();
    return 0;
}