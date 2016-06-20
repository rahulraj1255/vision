import cv2
import numpy as np
from matplotlib import pyplot as plt
def encContour(i):
	if type(i) == np.ndarray:
		image=i
	else:
		image=cv2.imread(i)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,8)
	#plt.imshow(thresh,cmap='gray')
	#plt.show()
	
	can=cv2.Canny(gray,120,200)
	#plt.imshow(can,cmap='gray')
	#plt.show()
	
	closing=cv2.morphologyEx(can,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
	#plt.imshow(closing)
	#plt.show()
	contours,hei=cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	#x=np.zeros(closing.shape,dtype=np.uint8)
	
	
	if len(contours) == 1 :
		#cv2.drawContours(x,contours,0,(255),2)
		#plt.imshow(x,'gray')
		#plt.show()
		return contours[0]
	else:
		k=0
		t=contours[0]
		for i in contours :
			if cv2.arcLength(t,False) < cv2.arcLength(i,False):
				t=i

	#cv2.drawContours(x,[t],0,(255),2)
	#plt.imshow(x,'gray')
	#plt.show()
	#print 'asdf'
	return t
def give_extindices(f):
	fl=f[:,:,0].argmin()
	fr=f[:,:,0].argmax()
	ft=f[:,:,1].argmin()
	fb=f[:,:,1].argmax()

	return {"top":ft,"left":fl,"right":fr,"bottom":fb}
