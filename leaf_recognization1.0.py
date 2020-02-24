import cv2
import numpy
import math
from PIL import Image
from resizeimage import resizeimage

# mouse callback function
x1=y1=x2=y2=0
flag=0
img = cv2.imread('./leaves/zelkova_serrata/12992008865346.jpg');
height, width, channels = img.shape
img = cv2.resize(img,(400, 400), interpolation = cv2.INTER_CUBIC)
cv2.imshow('res',img)

def draw_circle(event,x,y,flags,param):

    if event == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(img,(x,y),6,(255,0,0),-1)
        global flag
        global x1,x2,y1,y2
        flag= flag+1
        if flag == 1:
            x1=x
            y1=y
            print x,y
        elif flag == 2:
            x2=x
            y2=y
            print x,y
            distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
            print distance
            slope = (float(y2-y1)/(x2-x1))
            print slope
            angle = (math.atan(slope)*180)/math.pi
            print "angle is ",angle
            #imgt = cv2.imread('./leaves/zelkova_serrata/12992008490378.jpg');
            num_rows,num_cols = img.shape[:2]
            rot_mtx = cv2.getRotationMatrix2D((num_rows/2 ,num_cols/2), angle, 1)
            rotated = cv2.warpAffine(img, rot_mtx, (num_rows,num_cols))
            cv2.imshow("Rotated", rotated)
            
            
            
# Create a black image, a window and bind the function to window

cv2.imshow('Original', img)
cv2.setMouseCallback('Original',draw_circle)

gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray', gimg)

#blur an image
blur = cv2.medianBlur(gimg,5)
#blur = cv2.GaussianBlur(gimg,(5,5),0)
#cv2.imshow('blur', blur)
#blur2 = cv2.blur(thresh,(5,5))


#thresholding
ret, thresh = cv2.threshold(blur, 106, 255, cv2.THRESH_BINARY)
cv2.imshow('Threshold', thresh)


#extract  border

laplacian = cv2.Laplacian(thresh, cv2.CV_64F)
#cv2.imshow('laplace', laplacian)

def findLeafContour(contours):
    maxArea = 0
    contour_index = -1
    for i in range(1,len(contours)):        
        area  =  cv2.contourArea(contours[i])
        #print area
        if area > maxArea and area < 60000:
              maxArea = area
              contour_index = i
              
    return contour_index

#find contours

_,contours,heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print "len is ",len(contours)

if len(contours) > 0:
   #c = max(contours, key=cv2.contourArea)
    leaf_contour_index = findLeafContour(contours)
    if leaf_contour_index == -1:
        print "Not contour detected in -1"
        exit()
else:
    print "Not contour detected"
    exit()

#print "leaf_contour_index is ",leaf_contour_index
cv2.drawContours(img,contours, leaf_contour_index, (100,215,0),5)
cv2.drawContours(img,contours, -1, (0,0,255),3)
cv2.imshow('contours', img)

leaf_contour = contours[leaf_contour_index]
#1.LeafArea
area = cv2.contourArea(leaf_contour)
print "Area is " , area

#2.Leaf Perimeter
perimeter = cv2.arcLength(leaf_contour, True)
print "Perimeter is " , perimeter

#3.Height                          
cv2.waitKey(0)
cv2.destroyAllWindows()


