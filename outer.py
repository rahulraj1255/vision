import cv2
import numpy as np
from matplotlib import pyplot as plt
def encContour(i):
	image=cv2.imread(i)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,8)

	can=cv2.Canny(gray,120,200)
	closing=cv2.morphologyEx(can,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
	contours,hei=cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	#x=np.zeros(closing.shape,dtype=np.uint8)
	#cv2.drawContours(x,contours,0,(255),2)
	#cv2.imwrite('TEST.jpg',x)
	if len(contours) == 1 :
		return contours[0]
	else:
		k=0
		t=contours[0]
		for i in contours :
			if cv2.arcLength(t,True) < cv2.arcLength(i,True):
				t=i
		return t
	
