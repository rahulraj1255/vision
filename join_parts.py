from outer import encContour,give_extindices
from give_extpoints import give_extpoints
import cv2
import numpy as np
from matplotlib import pyplot as plt
from indices import give_index_h,give_index_v

def index_flatside(contour1,side,frac=0) :
	if side not in ["left","right","top","bottom"]:
		print "Enter a valid side"
		exit(1)
	if side in ["left","right"] and frac!=0 :
		extpt=give_extpoints(contour1)
		range1=[extpt["top"][1],extpt["top"][1]*(1-frac)+extpt["bottom"][1]*frac]
		sorted(range1)
		contour=[]
		for a in range(0,len(contour1)) :
			if contour1[a,0,1] >range1[0] and contour1[a,0,1] <range1[1] :
				contour.append(contour1[a])
	else :
		contour=contour1
	contour=np.array(contour)
	extremeindex=give_extindices(contour)[side]
	if side == "left":
		a=contour[extremeindex,0,0]+1
	elif side =="right":
		a=contour[extremeindex,0,0]-1
	elif side =="top":
		a=contour[extremeindex,0,1]+1
	else :
		a=contour[extremeindex,0,1]-1
	iterator1=True
	iterator2=False
	t1=extremeindex
	t2=extremeindex
	if side in ["left","right"] :
		while iterator1!=iterator2 :
			iterator1=not iterator1
			if contour[t1+1,0,0] in [a,a-1,a+1] :
				if iterator1 is iterator2 :
					iterator2= not iterator1
				t1=t1+1
			if contour[t2-1,0,0] in [a,a-1,a+1] :
				if iterator1 is  iterator2 :
					iterator2=not iterator1
				t2=t2 -1
		tempindex1=give_index_h(contour1,contour[t1,0,1])
		tempindex2=give_index_h(contour1,contour[t2,0,1])
		if side =='left' and frac!=0:
			mini=tempindex1[0]
			minimum=contour1[mini,0,0]
			for indextem in tempindex1 :
				if minimum>contour1[indextem,0,0] :
					mini=indextem
					minimum=contour1[mini,0,0]
			t1=mini
			mini=tempindex2[0]
			minimum=contour1[mini,0,0]
			for indextem in tempindex2 :
				if minimum > contour1[indextem,0,0] :
					mini=indextem
					minimum=contour1[indextem,0,0]
			t2=mini
		elif side =='right' and frac!=0 :
			maxi=tempindex1[0]
			maximum=contour1[maxi,0,0]
			for indextem in tempindex1 :
				if maximum<contour1[indextem,0,0] :
					maxi=indextem
					maximum=contour1[maxi,0,0]
			t1=maxi
			maxi=tempindex2[0]
			maximum=contour1[maxi,0,0]
			for indextem in tempindex2 :
				if maximum < contour1[indextem,0,0] :
					maxi=indextem
					maximum=contour1[indextem,0,0]
			t2=maxi
		return [t1,t2] if contour1[t1,0,1] <contour1[t2,0,1] else [t2,t1]
	else :
		while iterator1!=iterator2 :
			iterator1=not iterator1
			if contour[t1+1,0,1] in [a,a-1,a+1] :
				if iterator1 is iterator2 :
					iterator2= not iterator1
				t1=t1+1
			if contour[t2-1,0,1] in [a,a-1,a+1] :
				if iterator1 is  iterator2 :
					iterator2=not iterator1
				t2=t2 -1
		return [t1,t2] if contour[t1,0,0]<contour[t2,0,0] else [t2,t1]
	
def join_parts(body_without_hands,hands) :
	body=cv2.imread(body_without_hands)
	arms1=cv2.imread(hands)

	body_prt=body.copy()
	body_prt[body.shape[0]/3:body.shape[0],:,:]=255
	cv2.imwrite('body_prt.jpg',body_prt)
	prt_cnt=encContour('body_prt.jpg')
	leftindex=index_flatside(prt_cnt,"left")
	print "bodyleft",prt_cnt[leftindex,0]
	rightindex=index_flatside(prt_cnt,"right")
	print "bodyright",prt_cnt
	blank=np.zeros(arms1.shape,dtype=np.uint8)
	blank[:,:,:]=255
	arms2=arms1.copy()
	#print arms1.shape[1]
	arms1[:,arms1.shape[1]/2:arms1.shape[1]]=blank[:,arms1.shape[1]/2:arms1.shape[1]]
	arms2[:,0 : arms1.shape[1]/2]=blank[:,0 : arms1.shape[1]/2]	
	cv2.imwrite('arms1.jpg',arms1)
	cv2.imwrite('arms2.jpg',arms2)
	armsc1=encContour('arms1.jpg')
	armsc2=encContour('arms2.jpg')
	arm1index=index_flatside(armsc1,"right")
	arm2index=index_flatside(armsc2,"left")
	print "left top",armsc1[arm1index[1],0],'\nright top',armsc2[arm2index[1],0],"\nleftbody",prt_cnt[leftindex[1],0],"\nrightbody",prt_cnt[rightindex[1],0]
	armsc1[:,0]=armsc1[:,0]-armsc1[arm1index[0],0]+prt_cnt[leftindex[0],0]
	armsc2[:,0]=armsc2[:,0]-armsc2[arm2index[0],0]+prt_cnt[rightindex[0],0]
	cv2.drawContours(blank,[armsc1,armsc2,encContour(body_without_hands)],-1,(0),1)
	plt.imshow(blank)
	plt.show()
#join_parts('body_without_hands.jpg','hands2.jpg')
