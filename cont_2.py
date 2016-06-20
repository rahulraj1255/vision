import cv2
import numpy as np

def retCont(i):
	'''
	inputs:
		i: name of the image
	outputs:
		2 enclosing-contours having largest arc lengths.
		x: image file in which the contour is rendered
	'''
	image=cv2.imread(i)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,8)

	can=cv2.Canny(gray,120,200)
	closing=cv2.morphologyEx(can,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
	contours,hei=cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	x=np.zeros(closing.shape,dtype=np.uint8)
	#cv2.drawContours(x,contours,0,(255),2)
	#cv2.imwrite('TEST.jpg',x)
	#print x.shape
	if len(contours) == 1 :
		return contours[0],[],x
	elif len(contours) == 2:
		return contours[0],contours[1],x
	else:
		k=0
		t={}
		t1=contours[0]
		t2=contours[1]
		if cv2.arcLength(t2,True) > cv2.arcLength(t1,True):
				t=t1
				t1=t2
				t2=t

		for i in contours :
			if cv2.arcLength(t1,True) < cv2.arcLength(i,True):
				t1=i
			if cv2.arcLength(t2,True) < cv2.arcLength(i,True) and cv2.arcLength(t1,True) > cv2.arcLength(i,True):
				t2=i
		return t1,t2,x
