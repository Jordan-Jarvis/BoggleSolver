#include "FindNumbers.h"
#include <math.h>

cv::Mat FindNumbers::showDigits(vector<cv::Mat> &digits, int color)
{
    vector<Mat> rows;
    Mat returnImg;
    cerr << digits.size();
    for(int i = 0; i < digits.size(); i++)
    {
        copyMakeBorder(digits[i], digits[i], 1, 1, 1, cv::BORDER_CONSTANT, 0, color);
    }


    return returnImg;
}  
cv::Mat FindNumbers::convertWhenColor(int &color, cv::Mat img)
{
    return img;
}


cv::Mat FindNumbers::preProcessImage(cv::Mat &img, bool skipDilate)
{   
    
    cv::adaptiveThreshold(img, img,255, cv::ADAPTIVE_THRESH_GAUSSIAN_C, cv::THRESH_BINARY, 11, 2);
    cv::bitwise_not(img,img);

    if (!skipDilate)
    {

        int dilation_type = 0;
        if( 0 == 0 )
        { dilation_type = MORPH_RECT; }


        Mat element = getStructuringElement( dilation_type,
        Size( 2 + 1, 2*1 ),
        Point( 0, 0 ) );
        //erode( img, img, element );
        dilate( img, img, element );

        //cv::dilate(img,img,0, Point(1, 0), 1, 1, 1);

    }
    return img;
}

bool compareContourAreas ( std::vector<cv::Point> contour1, std::vector<cv::Point> contour2 ) {
    double i = fabs( contourArea(cv::Mat(contour1)) );
    double j = fabs( contourArea(cv::Mat(contour2)) );
    return ( i < j );
}

vector<Point> FindNumbers::findCornersOfLargestPolygon(cv::Mat &img)
{
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    findContours(img, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    std::sort(contours.begin(), contours.end(), compareContourAreas);
    std::vector<cv::Point> biggestContour = contours[contours.size()-1];
    int br = 0;
    int tl = 100000;
    int bl = 100000;
    int tr = 0;
    vector<Point> square;
    square.push_back(biggestContour[0]);
    square.push_back(biggestContour[0]);
    square.push_back(biggestContour[0]);
    square.push_back(biggestContour[0]);
    for (int i = 0; i < biggestContour.size(); i++)
    {
        if (biggestContour[i].x + biggestContour[i].y > br){
            br = biggestContour[i].x + biggestContour[i].y;
            square[2] = biggestContour[i];
        }
        if (biggestContour[i].x + biggestContour[i].y < tl){
            tl = biggestContour[i].x + biggestContour[i].y;
            square[0] = biggestContour[i];
        }
        if (biggestContour[i].x - biggestContour[i].y < bl){
            bl = biggestContour[i].x - biggestContour[i].y;
            square[3] = biggestContour[i];
        }
        if (biggestContour[i].x - biggestContour[i].y > tr){
            tr = biggestContour[i].x - biggestContour[i].y;
            square[1] = biggestContour[i];
        }
    }

    return square;
}
int FindNumbers::distanceBetween(cv::Point &p1, cv::Point &p2)
{
    int a = p2.x - p1.x;
    int b = p2.y - p1.y;

    return sqrt(pow(a,2.) + pow(b,2.));
}
cv::Mat FindNumbers::cropAndWarp(cv::Mat &img, vector<Point> &cropRect)
{
    Point2f pt[4];
    Point2f pt2[4];
    float side;
    for (int i = 0; i < 4; i++)
    {
        pt[i] = static_cast<Point2f>(cropRect[i]);
        if (distanceBetween(cropRect[2],cropRect[1]) > side)
        {
            side = distanceBetween(cropRect[2],cropRect[1]);
        }
        if (distanceBetween(cropRect[0],cropRect[3]) > side)
        {
            side = distanceBetween(cropRect[0],cropRect[3]);
        }
        if (distanceBetween(cropRect[2],cropRect[3]) > side)
        {
            side = distanceBetween(cropRect[2],cropRect[3]);
        }
        if (distanceBetween(cropRect[1],cropRect[2]) > side)
        {
            side = distanceBetween(cropRect[1],cropRect[2]);
        }
    }
    pt2[1].x = side - 1;
    pt2[2].x = side - 1;
    pt2[2].y = side - 1;
    pt2[3].y = side - 1;
 
    warpPerspective(img, img, getPerspectiveTransform(pt, pt2),{500,425});
    return img;
}
std::vector<cv::Rect> FindNumbers::inferGrid(cv::Mat img)
{
    vector<Rect> p;
    int side = img.rows / 9;

    Rect rect;

    
    for (int j = 0; j < 9; j++)
    {
        for(int i = 0; i < 9; i++)
        { 
            rect.x = side * (i);
            rect.y = side * (j);
            rect.width = side;
            rect.height = side;
            p.push_back(rect);
        }
    }

    return p;

}
Mat FindNumbers::cutFromRect(Mat img, cv::Rect rect)
{
    cv::Mat crop = img(rect);
    return crop;
}
Mat FindNumbers::scaleAndCenter(Mat &img, int size, int margin, int background)
{
    return img;
}
int * FindNumbers::centerPad(int length)
{
    return 0;
}
Rect FindNumbers::findLargestFeature(Mat img, Point Tl, Point Br)
{
    Rect test;
    return test;
}
Mat FindNumbers::extractDigit(Mat img, Rect rectangle, int size)
{
    img = cutFromRect(img, rectangle);
    int margin;
    margin = ((img.cols + img.rows)/2) / 2.5;
    Point Tl;
    Point Br;
    Tl.x = img.cols;
    Tl.y = img.rows;
    Br.x = img.cols - margin;
    Br.y = img.rows - margin;
    
    Rect bbox = findLargestFeature(img, Tl, Br);
    cutFromRect(img, bbox);
    return img;
}

vector<Mat> FindNumbers::getDigits(Mat img, vector<Rect> squares, int size)
{
    vector<Mat> numbers;
    for (int i = 0; i < 81; i++)
    {
        numbers.push_back(extractDigit(img, squares[i], size));
    }
    return numbers;
}

Mat FindNumbers::parseGrid(Mat original)
{
    resize(original,original,{500,500});
    Mat originalBackup = original;
    preProcessImage(originalBackup,0);

    
    vector<Point> corners = findCornersOfLargestPolygon(originalBackup);
    for (int i = 0; i < 4; i++)
    {
        cout << corners[i].x << " x " << corners[i].y << " Y " << endl;
    }
    cropAndWarp(original, corners);
    vector<Rect> squares = inferGrid(original);
    vector<Mat> numbers;
    //numbers = getDigits(original.clone(), squares, 28);
    
    //showDigits(numbers, 255);
    return original;
}


vector<Mat> FindNumbers::extractSudoku(Mat &img)
{

    vector<Mat> p;
    return p;
}


