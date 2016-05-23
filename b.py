import cv2
import numpy as np
import copy
import math
import sys

def pupildetect(name):
    im=cv2.imread(name) # read picture
    #im = cv2.resize(im,(1000,1000), interpolation = cv2.INTER_AREA)
    #cv2.imshow('original',im)
    invert = np.invert(im) # inverting image colours
    invert2greyscale = cv2.cvtColor(invert, cv2.COLOR_BGR2GRAY) # convert inverted image to greyscale

    ret,thresh = cv2.threshold(invert2greyscale,220,255,cv2.THRESH_BINARY) # filtering the image based on its color
    ret1,final_filtered_image = cv2.threshold(invert2greyscale,220,255,cv2.THRESH_BINARY) # copy of the filtered image
    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # finding the contours in the image

    area = [] #array which stores the area of each contours
    perimeter = [] #array which stores the perimeter of each contour

    for i in range(0,len(contours)):
        area.append(cv2.contourArea(contours[i]))
        perimeter.append(cv2.arcLength(contours[i],True))

    sorted_area_of_the_contours = copy.deepcopy(area) # copying the area array into other array to make the new arrray in decending order
    sorted_area_of_the_contours.sort(reverse = True)
    minimum_error_index = 0 # stores the index of contour which has minimum deviaiton in radius
    minimum_error = 100 # stores the error of the radius value temporarily

    for i in range(0,4): # this algorithm finds the contour which hsa minimum deviaiton for the radius calculated
        index = area.index(sorted_area_of_the_contours[i])
        deviation = ((abs((math.sqrt(cv2.contourArea(contours[index]))/math.pi) - (cv2.arcLength(contours[index],True)/(math.pi*2))))/(cv2.arcLength(contours[index],True)/(math.pi*2)))*100
        print (deviation)
        if deviation < minimum_error:
            minimum_error_index = index
            minimum_error = deviation

    cnt =contours[minimum_error_index]

    # creating circle in the image
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(im,center,radius,(0,255,0),2)
    cv2.drawContours(im,contours,minimum_error_index,(0,0,255),2)
    return im
    #cv2.imshow("detected image",im)
    #cv2.imshow("final filteres image",final_filtered_image)
    #cv2.imshow('inverted',invert)
    #cv2.imshow('inverted to greyscale',invert2greyscale)
    #cv2.imshow('converted to binary',thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
