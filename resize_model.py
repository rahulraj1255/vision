import cv2
import numpy as np
from outer import encContour
from give_extpoints import give_extpoints

# Takes the name of front , side view and image with arms stretched out of model and either of front and side view of real image 
# Returns the name of newly created images scaled according to height
def ratioheight(mfront,mfrontf,mside,rimg) :
	m=encContour(mfront)
	mf=encContour(mfrontf)
	ms=encContour(mside)
	r=encContour(rimg)
	mp=give_extpoints(m)
	mfp=give_extpoints(mf)
	msp=give_extpoints(ms)
	rp=give_extpoints(r)
	heightm=mp['bottom'][1]-mp['top'][1]
	heightmf=mfp['bottom'][1]-mfp['top'][1]
	heightms=msp['bottom'][1]-msp['top'][1]
	heightr=rp['bottom'][1]-rp['top'][1]
	ratios=[float(heightm)/heightr,float(heightmf)/heightr,float(heightms)/heightr]
	return ratios
def resize_model(mfront,mfrontf,mside,rimg):
	mf=encContour(mfront)
	ms=encContour(mside)
	mff=encContour(mfrontf)
	rimgc=encContour(rimg)
	et_mf = tuple(mf[mf[:, :, 1].argmin()][0])
	eb_mf = tuple(mf[mf[:, :, 1].argmax()][0])
	et_ms = tuple(ms[ms[:, :, 1].argmin()][0])
	eb_ms = tuple(ms[ms[:, :, 1].argmax()][0])
	et_mff = tuple(mf[mf[:, :, 1].argmin()][0])
	eb_mff = tuple(mff[mff[:, :, 1].argmax()][0])
	et_rimg = tuple(rimgc[rimgc[:, :, 1].argmin()][0])
	eb_rimg = tuple(rimgc[rimgc[:, :, 1].argmax()][0])
	
	hf=eb_mf[1]-et_mf[1]
	hs=eb_ms[1]-et_ms[1]
	hff=eb_mff[1]-et_mff[1]
	hrimg=eb_rimg[1]-et_rimg[1]
	ratios=[float(hf)/hrimg,float(hs)/hrimg,float(hff)/hrimg]
	f=cv2.imread(mfront)
	s=cv2.imread(mside)
	ff=cv2.imread(mfrontf)
	#print f.shape,s.shape
	#exit(0)
	floating1=float(f.shape[1])/ratios[0]
	floating2=float(f.shape[0])/ratios[0]
	f1=cv2.resize(f,(int(floating1),int(floating2)),interpolation=cv2.INTER_CUBIC)
	floating1=float(s.shape[1])/ratios[1]
	floating2=float(s.shape[0])/ratios[1]
	s1=cv2.resize(s,(int(floating1),int(floating2)),interpolation=cv2.INTER_CUBIC)
	floating1=float(ff.shape[1])/ratios[2]
	floating2=float(ff.shape[0])/ratios[2]
	ff1=cv2.resize(ff,(int(floating1),int(floating2)),interpolation=cv2.INTER_CUBIC)
	cv2.imwrite('mfront.jpg',f1)
	cv2.imwrite('mside.jpg',s1)
	cv2.imwrite('mfrontf.jpg',ff1)
	ratios=ratioheight('mfront.jpg','mfrontf.jpg','mside.jpg',rimg)
	for i in ratios :
		if i < 0.93 or i >1.07 :
			return resize_model('mfront.jpg','mfrontf.jpg','mside.jpg',rimg)
	return 'mfront.jpg','mside.jpg','mfrontf.jpg'
