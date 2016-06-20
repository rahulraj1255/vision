import cv2
import numpy as np
from cont_2 import retCont
from parts import disint
from parts import retval
from outer import encContour
from parts_hum import disint_hum

def swap(x,y):
	z=[]
	z=x
	x=y
	y=z
	return x,y

def cor_hands(samp,samp_side,img,img_side):
	'''
	inputs:
		samp:sample front image
		samp_side:sample image of side view
		img: given human front image
		img_side: given human image of side view
	
	output: image of the manipulated hands 
	'''
	#taking front view and side view
	sa,sb,sc,sd,se,sf=disint(samp,samp_side)
	a,b,c,d=disint_hum(img)
	conts1,conts2,sx=retCont(se)
	conti1,conti2,ix=retCont(a)
	im=cv2.imread(img)
	ims=cv2.imread(samp)
	h,w,d=im.shape
	
	#encContour('hands.jpg')
	#cont1.shape=cont2.shape
	#cont=cont1+cont2
	sll=tuple(conts1[conts1[:,:,0].argmin()][0])
	slr=tuple(conts1[conts1[:,:,0].argmax()][0])
	slt=tuple(conts1[conts1[:,:,1].argmin()][0])
	slb=tuple(conts1[conts1[:,:,1].argmax()][0])
	srl=tuple(conts2[conts2[:,:,0].argmin()][0])
	srr=tuple(conts2[conts2[:,:,0].argmax()][0])
	srt=tuple(conts2[conts2[:,:,1].argmin()][0])
	srb=tuple(conts2[conts2[:,:,1].argmax()][0])
	ill=tuple(conti1[conti1[:,:,0].argmin()][0])
	ilr=tuple(conti1[conti1[:,:,0].argmax()][0])
	ilt=tuple(conti1[conti1[:,:,1].argmin()][0])
	ilb=tuple(conti1[conti1[:,:,1].argmax()][0])
	irl=tuple(conti2[conti2[:,:,0].argmin()][0])
	irr=tuple(conti2[conti2[:,:,0].argmax()][0])
	irt=tuple(conti2[conti2[:,:,1].argmin()][0])
	irb=tuple(conti2[conti2[:,:,1].argmax()][0])
	C=[]
	if sll[0]>srl[0]:
		conts1,conts2=swap(conts1,conts2)
		sll,srl=swap(sll,srl)
		slr,srr=swap(slr,srr)
	if ill[0]>irl[0]:
		conti1,conti2=swap(conti1,conti2)
		ill,irl=swap(ill,irl)
		ilr,irr=swap(ilr,irr)
		
	lens1=slr[0]-sll[0]
	#lens2=srr[1]-srl[1]
	leni1=ilr[0]-ill[0]
	#leni2=irr[1]-irl[1]
	ratio1=lens1/leni1
	#ratio2=lens2/leni2
	#resizing
	x=[]
	x=conts1[:,0,0]-slr[0]
	conts1[:,0,0]=x*ratio1 +slr[0]
	#x=[]
	#x=conts2[:,0,0]-srl[0]
	#conts2[:,0,0]=x*ratio2 +srl[0]
	#to get the shirt point
	'''a=0
	ran2=np.linspace(1,ilr[0],200)
	for i in ran2:
		yp=retval(i-1,conti1,1)
		y=retval(i,conti1,1)
		if len(yp)==2 and a==0:
			p_slope=y[0]-yp[0]
			a=1									#comparing slopes
			continue
		if len(yp)==2 and len(y)==2 and a==1:
			#print len(yp)
			slope=y[1]-yp[1]
			if p_slope!=0:
				ratio=slope/p_slope
			p_slope=slope
		else: 
			continue
		if ratio>1.5:
			Y.append([i,y[1]])
			Y.append([i,y[0]])
			break
	ori_len=Y[0][1]-Y[1][1]
	X=retval(i,conts1,1)
	vir_len=X[0][1]-X[1][1]
	r=ori_len/vir_len'''
	
	p=(1.718/2.618)*leni1 + ill[0]
	yi=retval(p,conti1,1)
	ori_len=yi[1]-yi[0]
	ys=retval(p,conts1,1)
	vir_len=ys[1]-ys[0]
	
	r=float(ori_len)/vir_len
	ran1=np.linspace(ill[0],p,50)
	ran2=np.linspace(p,ilr[0],50)
	py=retval(p,conts1,1)
	img_new=np.zeros((h,w,d),dtype=np.uint8)
	yi=[]
	for i in ran1:
		yi=retval(i,conti1,1)
		if len(yi)==2:
			cv2.circle(img_new,(int(i),int(yi[0]),), 2, (255,255,255), -1)
			cv2.circle(img_new,(int(i),int(yi[1])), 2, (255,255,255), -1)
			cv2.circle(img_new,(w-int(i),int(yi[0]),), 2, (255,255,255), -1)
			cv2.circle(img_new,(w-int(i),int(yi[1])), 2, (255,255,255), -1)
			#img_new[int(yi[0]),int(i)]=[255,255,255]
			#img_new[int(yi[1]),int(i)]=[255,255,255]
			#img_new[int(yi[0]),w-int(i)]=[255,255,255]
			#img_new[int(yi[1]),w-int(i)]=[255,255,255]
	
	#img_new[:,0:int(p)]=sx[:,0:int(p)]
	c=0
	for i in ran2:
		y=retval(i,conts1,1)
		ref=(y[0]+y[1])/2
		y1=y[0]-ref
		y2=y[1]-ref
		y1=y1*r+ref
		y2=y2*r+ref
		if c==0:
			ref2=(yi[0]+yi[1])/2
			d=ref2-ref
		cv2.circle(img_new,(int(i),int(y1+d)), 2, (255,255,255), -1)
		cv2.circle(img_new,(int(i),int(y2+d)), 2, (255,255,255), -1)
		cv2.circle(img_new,(w-int(i),int(y1+d)), 2, (255,255,255), -1)
		cv2.circle(img_new,(w-int(i),int(y2+d)), 2, (255,255,255), -1)
		#img_new[int(y1+d),int(i)]=[255,255,255]
		#img_new[int(y2+d),int(i)]=[255,255,255]
		#img_new[int(y1+d),w-int(i)]=[255,255,255]
		#img_new[int(y2+d),w-int(i)]=[255,255,255]
		c+=1
	
	return img_new
	
		
	
	
	#i=np.zeros((h,w,d),dtype=np.uint8)
	#cv2.drawContours(i, cont1, -1, (255,255,255), 3)
	#cv2.drawContours(i, cont2, -1, (255,255,255), 3)
	
	#cv2.imwrite('write.jpg', i)
