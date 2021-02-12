
#include "opencv2/opencv.hpp"
using namespace cv;
using namespace std;

class FindNumbers {

    private:
        
        Mat showDigits(vector<cv::Mat> &digits, int color);
        cv::Mat convertWhenColor(int &color, cv::Mat img);
        
        vector<Point> findCornersOfLargestPolygon(cv::Mat &img);
        int distanceBetween(cv::Point &p1, cv::Point &p2);
        cv::Mat cropAndWarp(cv::Mat &img, vector<Point> &cropRect);
        std::vector<cv::Rect> inferGrid(cv::Mat img);
        Mat cutFromRect(Mat img, cv::Rect rect);
        Mat scaleAndCenter(Mat &img, int size, int margin, int background);
        int * centerPad(int length);
        Rect findLargestFeature(Mat img, Point Tl, Point Br);
        Mat extractDigit(Mat img, Rect rectangle, int size);
        vector<Mat> getDigits(Mat img, vector<Rect> squares, int size);
        
    public:
        Mat parseGrid(Mat original);
        cv::Mat preProcessImage(cv::Mat &img, bool skipDilate);     
        vector<Mat> extractSudoku(Mat &img);
    

};