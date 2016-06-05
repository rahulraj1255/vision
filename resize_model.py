import cv2
import numpy as np
from outer import encContour
# Takes the name of front and side view of model and either of front and side view of real image 
# Returns the name of newly created images scaled according to height
def resize_model(mfront,mside,rimg):
	mf=encContour(mfront)
	ms=encContour(mside)
	rimg=encContour(rimg)
	et_mf = tuple(mf[mf[:, :, 1].argmin()][0])
	eb_mf = tuple(mf[mf[:, :, 1].argmax()][0])
	et_ms = tuple(ms[ms[:, :, 1].argmin()][0])
	eb_ms = tuple(ms[ms[:, :, 1].argmax()][0])
	et_rimg = tuple(rimg[rimg[:, :, 1].argmin()][0])
	eb_rimg = tuple(rimg[rimg[:, :, 1].argmax()][0])
	
	hf=eb_mf[1]-et_mf[1]
	hs=eb_ms[1]-et_ms[1]
	hrimg=eb_rimg[1]-et_rimg[1]
	ratios=[float(hf)/hrimg,float(hs)/hrimg]
	f=cv2.imread(mfront)
	s=cv2.imread(mside)
	print f.shape,s.shape
	#exit(0)
	floating1=float(f.shape[1])/ratios[0]
	floating2=float(f.shape[0])/ratios[0]
	f1=cv2.resize(f,(int(floating1),int(floating2)),interpolation=cv2.INTER_CUBIC)
	floating1=float(s.shape[1])/ratios[1]
	floating2=float(s.shape[0])/ratios[1]
	s1=cv2.resize(s,(int(floating1),int(floating2)),interpolation=cv2.INTER_CUBIC)
	cv2.imwrite('mfront.jpg',f1)
	cv2.imwrite('mside.jpg',s1)
	return 'mfront.jpg','mside.jpg'
