import cv2
import numpy as np
a=[]
def ret2Val (i):
	def ret2val(event,x,y,flags,param):
		if event==cv2.EVENT_LBUTTONDOWN :
			a.append([x,y])
	image=cv2.imread(i)
	cv2.namedWindow('Click',0)
	cv2.setMouseCallback('Click',ret2val)
	while(1) :
		cv2.imshow('Click',image)
		if cv2.waitKey(20) & 0xFF ==27 :
			break
			
		if len(a) == 2:
			cv2.destroyAllWindows()
			return sorted(a,key=lambda x : x[1] )
			
			exit(0)
	
	return [0,0]
