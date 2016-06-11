import cv2
from give_extpoints import give_extpoints
from give_index_ct import give_index_ct
from outer import encContour
'''
Input arguments :
	mimg : name of model image present in the current directory
	rimg : name of real image present in the current directory
	args : it is an array containing names of images to be scaled according to the scaling constant calculated with the above two images
Output :
	Gives the scaling constant if required 
'''
def ret_hscale(rimg,mimg,args):
# getting the enclosing contours of real image and model image
	realc=encContour(rimg)
	modelc=encContour(mimg)
	extreal=give_extpoints(realc)
	extmodel=give_extpoints(modelc)
	midreal=int( 0.25*extreal["bottom"][1]+0.75*extreal["top"][1])
	midmodel=int( 0.25*extmodel["bottom"][1]+0.75*extmodel["top"][1])

	realindex=give_index_ct(realc,midreal+extreal["top"][1])
	modelindex=give_index_ct(modelc,midmodel+extmodel["top"][1])

	min=realc[realindex[0],0,0]
	# for real
	
	leftreal=realindex[0]
	k=0
	for i in realindex :
		k+=1

	for i in range(1,len(realindex)):
		if min> realc[realindex[i],0,0] :
			
			leftreal=realindex[i]
			min=realc[realindex[i],0,0]
	min=modelc[modelindex[0],0,0]
	# for model
	
	leftmodel=modelindex[0]
	k=0
	for i in modelindex :
		k+=1
	for i in range(1,len(modelindex)) :
		if min>modelc[modelindex[i],0,0] :
			leftmodel=modelindex[i]
			
			min=modelc[modelindex[i],0,0]
#figuring out the direction on which to move to reach the shoulder
	directionreal='+' if realc[leftreal+1,0,1]+realc[leftreal+2,0,1]+realc[leftreal+3,0,1]<realc[leftreal,0,1]+realc[leftreal-1,0,1]+realc[leftreal-2,0,1] else '-'
	directionmodel='+' if modelc[leftmodel+1,0,1]+modelc[leftmodel+2,0,1]+modelc[leftmodel+3,0,1]<modelc[leftmodel,0,1]+modelc[leftmodel-1,0,1]+modelc[leftmodel-2,0,1] else '-'
# Getting the shoulder point for real image
	i=leftreal
	avr,avm=[0,0]
	a=realc[i,0]
	while(1) :
		
		if directionreal=='+' :
			b=realc[i+1,0]
			c=realc[i+2,0]
			d=realc[i+3,0]
			e=realc[i+4,0]
			f=realc[i+5,0]						
			avr=[float(b[0]+c[0]+d[0]+e[0]+f[0])/5,float(b[1]+c[1]+d[1]+e[1]+f[1])/5]
			i+=5
		else:
			b=realc[i-1,0]
			c=realc[i-2,0]
			d=realc[i-3,0]
			e=realc[i-4,0]
			f=realc[i-5,0]						
			avr=[float(b[0]+c[0]+d[0]+e[0]+f[0])/5,float(b[1]+c[1]+d[1]+e[1]+f[1])/5]
			i-=5
		
		if avr[0]!=a[0] and abs(float(avr[1]-a[1])/(avr[0]-a[0]))<1 :
			realshoulder=a
			break
		a=avr
# Getting the shoulder point for model image
	i=leftmodel
	a=modelc[i,0]
	while(1) :
		if directionreal=='+' :
			b=modelc[i+1,0]
			c=modelc[i+2,0]
			d=modelc[i+3,0]
			e=modelc[i+4,0]
			f=modelc[i+5,0]						
			avm=[float(b[0]+c[0]+d[0]+e[0]+f[0])/5,float(b[1]+c[1]+d[1]+e[1]+f[1])/5]
			i+=5
		else:
			b=modelc[i-1,0]
			c=modelc[i-2,0]
			d=modelc[i-3,0]
			e=modelc[i-4,0]
			f=modelc[i-5,0]						
			avm=[float(b[0]+c[0]+d[0]+e[0]+f[0])/5,float(b[1]+c[1]+d[1]+e[1]+f[1])/5]
			i-=5
		if avm[0]!=a[0] and abs(float(avm[1]-a[1])/(avm[0]-a[0]))<1 :
			modelshoulder=a
			break
		a=avm
#	print realshoulder,modelshoulder
	
#Calculating the width of model shoulder and real shoulder
	a=give_index_ct(realc,realshoulder[1])
	print "realshoulder",realc[a[0],0],realc[a[1],0]
	
	b=give_index_ct(modelc,modelshoulder[1])
	print "modelshoulder",modelc[b[0],0],modelc[b[1],0]
	if len(a)%2!=0 or len(b)%2!=0 :
		print "some error message" 
		exit(1)
	scaling=float(realc[a[1],0,0]-realc[a[0],0,0])/(modelc[b[1],0,0]-modelc[b[0],0,0])
	print scaling
	for i in args :
		x=cv2.imread(i)
	#	print x.shape,int(x.shape[1]*scaling)
		x1=cv2.resize(x,(int(float(x.shape[1])*scaling),x.shape[0]),interpolation=cv2.INTER_CUBIC)
		cv2.imwrite('scaled_'+i,x1)
	return scaling
