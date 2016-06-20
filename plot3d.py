from outer import encContour
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from give_extpoints import give_extpoints
from give_extpoints import give_extpoints2
from give_index_ct import give_index_ct
from give_index_ct import give_index_ct2
from outer import give_extindices
from join_parts import index_flatside
# Function which takes two arguments ( names of front and side view images existing in the same directory )
'''
Usage :
	Arguments:
		front : name of front view of person
		side  : name of side view of person
		points : two points in the image to determine the portion intended to be plotted ( pass empty array to plot completely )
'''
# Function which gives y values for a distance t and modified contour f
def retval (t,f) :
	x=[]
	for i in range(0,len(f)-1):
		a=f[:,1][i]-t
		b=f[:,1][i+1]-t
		if a*b == 0 :
			if a==0:
				x.append(f[:,0][i])
			else:
				x.append(f[:,0][i+1])
		else:
			if a*b<0:
				x.append((f[:,0][i]+f[:,0][i+1])/2)
	sorted(x)
# At this stage x has the required values but there may be some repeated values
	y=[]
	for i in range(0,len(x)-1):
		if x[i] == x[i+1] :
			continue
		y.append(x[i])
	if len(x) is not 0 :
		y.append(x[-1])
	return y
def retval2 (t,f) :
	x=[]
	for i in range(0,len(f)-1):
		a=f[:,0][i]-t
		b=f[:,0][i+1]-t
		if a*b == 0 :
			if a==0:
				x.append(f[:,1][i])
			else:
				x.append(f[:,1][i+1])
		else:
			if a*b<0:
				x.append((f[:,1][i]+f[:,1][i+1])/2)
	sorted(x)
# At this stage x has the required values but there may be some repeated values
	y=[]
	for i in range(0,len(x)-1):
		if x[i] == x[i+1] :
			continue
		y.append(x[i])
	if len(x) is not 0 :
		y.append(x[-1])
	return y
def plot3dHuman (front,side,points):
	
#Extracting enclosing contours
	s=encContour(side)
	f=encContour(front)
	
# Function which gives x values for a height t and modified contour f
	
# Getting extreme points
	fl=tuple(f[f[:,:,0].argmin()][0])
	fr=tuple(f[f[:,:,0].argmax()][0])
	 
	sl=tuple(s[s[:,:,0].argmin()][0])
	sr=tuple(s[s[:,:,0].argmax()][0])

	ft=tuple(f[f[:,:,1].argmin()][0])
	fb=tuple(f[f[:,:,1].argmax()][0])

	st=tuple(s[s[:,:,1].argmin()][0])
	sb=tuple(s[s[:,:,1].argmax()][0])
	#from height import height
	#height('man_front.jpg')
	#print ft,fb
	#print st,sb
# manipulating the contour to set the lowest point to origin and the body in positive direction
	f1=f
	f1=f1[:,0]-[fr[0]-(fl[0]+fr[0])/2,fb[1]]
	if len(points) != 0 :
		points[:,1]=points[:,1]-fb[1]
		points[:,1]=-points[:,1]
	f1[:,1]=-f1[:,1]
	
	s1=s
	s1=s1[:,0]-[sl[0]+(sl[0]+sr[0])/2,sb[1]]
	s1[:,1]=-s1[:,1]
	matplotlib.rcParams['legend.fontsize']=10
	fig=plt.figure()
	ax=fig.gca(projection='3d')
	s1
	#y=np.zeros(len(f1[:,0]),dtype=np.int64)
	#ax.plot(f1[:,0],y,f1[:,1],label='front')

	#x=np.zeros(len(s1[:,0]),dtype=np.int64)
	#ax.plot(x,s1[:,0],s1[:,1],label='side')
	ax.set_aspect('equal')
	#print retval(800,f1)
#Using 30 data points per height 
	theta=np.linspace(0,2*np.pi,30)
	if len(points) != 0 :
		t= float( points[1,1]- points[0,1])/(max(max(f1[:,1]),max(s1[:,1]))*0.01)
		iterator=np.linspace(points[0,1],points[1,1],t)
	else :
		iterator=np.linspace(0,max(max(f1[:,1]),max(s1[:,1])),100)
	X=[] ;Y=[];Z=[]
#For every value in iterator plotting the data points considering ellipses
	for fl in iterator:
		x1=retval(fl,f1)
		y1=retval(fl,s1)
		if len(x1)%2 !=0 :
			continue
		if len(x1) == 6:
			x_a=(x1[0]+x1[1])/2
			y_a=(y1[0]+y1[1])/2
			x_a1=(x1[4]+x1[5])/2
			a=(x1[1]-x1[0])/2
			a1=(x1[5]-x1[4])/2
			b=a
			b1=a1
			for temp in (x1[0]+x1[1])/2+a*np.cos(theta) :
				X.append(temp)
			for temp in (y1[0]+y1[1])/2+b*np.sin(theta) :
				Y.append(temp)
				Z.append(fl)
			for temp in (x1[4]+x1[5])/2+a1*np.cos(theta) :
				X.append(temp)
			for temp in (y1[0]+y1[1])/2+b1*np.sin(theta) :
				Y.append(temp)
				Z.append(fl)
		
		xf=[]
		if len(x1) == 6 :
			xf=[x1[2],x1[3]]
		elif len(x1) in [2,4] :
			xf=x1
		else:
			maxdiff=0
			d=0
			index=-1
			while d<len(x1) :
				diff=x1[d+1]-x1[d]
				if diff> maxdiff :
					maxdiff = diff
					index=d
				d+=2
				xf=[x1[index],x1[index+1]]
			try :
				if x1[index-1]-x1[index-2] < 1.20*(x1[index+1]-x1[index]) and x1[index-1]-x1[index-2] > 0.80*(x1[index+1]-x1[index]) :
					xf=x1[index-2:index+2]
					x1=xf
				elif x1[index+3]-x1[index+2] < 1.20*(x1[index+1]-x1[index]) and x1[index+3]-x1[index+2] > 0.80*(x1[index+1]-x1[index]) :
					xf=x1[index:index+4]
					x1=xf
			except IndexError:
				pass
	#	print len(x1),len(y1)
		if xf == [] :
			continue
		x_a=(xf[1]+xf[0])/2
		y_a=(y1[0]+y1[1])/2
		a=(xf[1]-xf[0])/2
		b=(y1[1]-y1[0])/2
		#print y1,b
		for temp in x_a+a*np.cos(theta) :
			X.append(temp)
		for temp in y_a+b*np.sin(theta) :
			Y.append(temp)
			Z.append(fl)
		
		if(len(x1)==4):
			a=(x1[3]-x1[2])/2
			x_a=(x1[3]+x1[2])/2
			y_a=(y1[0]+y1[1])/2
			for temp in x_a+a*np.cos(theta) :
				X.append(temp)
			for temp in y_a+b*np.sin(theta) :
				Y.append(temp)
				Z.append(fl)
	fig=plt.figure()
	ax=fig.add_subplot(111,projection='3d')
	#print len(X),len(Y),len(Z)
#Using wireframe plots ( please improve this : spaces between legs is not clear, may use surface plots )
	ax.plot_wireframe(X,Y,Z,rstride=10,cstride=10)
	# Create cubic bounding box to simulate equal aspect ratio
	max_range = np.array([max(X)-min(X), max(Y)-min(Y),max(Z)-min(Z)]).max()
	Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
	Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
	Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
	for xb, yb, zb in zip(Xb, Yb, Zb):
	   ax.plot([xb], [yb], [zb], 'w')
	plt.show()

	#print "height_front :  ",ft[0]-fb[0], "|||", ft[1]-fb[1]
	#print "height_side  :  ",st[0]-sb[0] ,"|||" ,st[1]-sb[1]
	
'''
This function enables plotting 3d plots of humans with arms raised
front is the front view of person without the hands 
'''
	
def plot3dHuman2 (front,arms,side,points):
	
	#Extracting enclosing contours
	s=encContour(side)
	f=encContour(front)
	#armsc=encContour(arms)
	
	# arms has both the arms so encContour would give the bigger contour but we want both the contours. Dividing the image into two and then using encContour for both the images
	
	arms1=cv2.imread(arms)
	blank=np.zeros(arms1.shape,dtype=np.uint8)
	blank[:,:,:]=255
	arms2=cv2.imread(arms)
	#print arms1.shape[1]
	arms1[:,arms1.shape[1]/2:arms1.shape[1]]=blank[:,arms1.shape[1]/2:arms1.shape[1]]
	arms2[:,0 : arms1.shape[1]/2]=blank[:,0 : arms1.shape[1]/2]
	armsc1=encContour(arms1)
	armsc2=encContour(arms2)
	extarms1=give_extindices(armsc1)["right"]
	extarms2=give_extindices(armsc2)["left"]
	index1=index_flatside(armsc1,"right")[0]
	index2=index_flatside(armsc2,"left")[0]
# Getting extreme points
	'''
	fl=tuple(f[f[:,:,0].argmin()][0])
	fr=tuple(f[f[:,:,0].argmax()][0])
	 
	sl=tuple(s[s[:,:,0].argmin()][0])
	sr=tuple(s[s[:,:,0].argmax()][0])

	ft=tuple(f[f[:,:,1].argmin()][0])
	fb=tuple(f[f[:,:,1].argmax()][0])

	st=tuple(s[s[:,:,1].argmin()][0])
	sb=tuple(s[s[:,:,1].argmax()][0])
	'''
	extf=give_extpoints(f)
	exts=give_extpoints(s)
	f1=f.copy()
	s1=s.copy()
	f1=f1[:,0]
	s1=s1[:,0]
	bindex1=index_flatside(f,"left",0.33)
	bindex2=index_flatside(f,"right",0.33)


	matplotlib.rcParams['legend.fontsize']=10
	fig=plt.figure()
	ax=fig.gca(projection='3d')
	# Changing reference 
	f1=f1[:]-[(extf["left"][0]+extf["right"][0])/2,extf["bottom"][1]]
	f1[:,1]=-f1[:,1]
	s1=s1[:]-[(exts["left"][0]+exts["right"][0])/2,exts["bottom"][1]]
	s1[:,1]=-s1[:,1]
	armsc1[:,0,1]=-armsc1[:,0,1]
	armsc2[:,0,1]=-armsc2[:,0,1]
	if len(points) != 0 :
		#print points,fb[1]
		points[0][1]=-(points[0][1]-extf["bottom"][1])
		points[1][1]=-(points[1][1]-extf["bottom"][1])

	#print points
	
	
#Matching the topmost shoulder point ( bringing the arms to the main body )
	armsc1[:,0]=armsc1[:,0]-armsc1[index1,0]+f1[bindex1[0]]
	armsc2[:,0]=armsc2[:,0]-armsc2[index2,0]+f1[bindex2[0]]
	armsVrange=[min(f1[bindex1[1]][1],f1[bindex2[1]][1]),max(f1[bindex1[0]][1],f1[bindex2[0]][1])]
	armsc1=armsc1[:,0]
	armsc2=armsc2[:,0]
	extarms1=give_extpoints2(armsc1)
	extarms2=give_extpoints2(armsc2)
	temp=retval((f1[bindex1[0],1]+f1[bindex1[1],1])/2,s1)
	yl,yr=[0,0]
	if len(temp)==2:
		yl=(temp[0]+temp[1])/2
	temp=retval((f1[bindex2[0],1]+f1[bindex2[1],1])/2,s1)
	if len(temp)==2 :
		yr=(temp[0]+temp[1])/2
	X=[] ;Y=[];Z=[]
	armsplotting = False
	clickrange=[points[0][1],points[0][0]]
	clickrange=sorted(clickrange,reverse=False)
	for p in clickrange :
		if p <armsVrange[1] and p > armsVrange[0] :
			print " Don't click on arms "
			exit(1)
	if clickrange[0]<armsVrange[0] and clickrange[1] > armsVrange[1] :
		armsplotting=True
	
	if armsplotting :
#Plotting arms
		theta=np.linspace(0,2*np.pi,15)
		iterator=np.linspace(extarms1["right"][0],extarms1["left"][0],50)

	
		for i in iterator :
			x1=retval2(i,armsc1)
			#print x1
			if len(x1)!=2 :
				continue
			
			x_a=(x1[0]+x1[1])/2
			radius = (abs(x1[1]-x1[0]))/2
			for th in theta :
				X.append(i)
				Y.append(yl+radius*np.cos(th))
				Z.append(x_a+radius*np.sin(th))
		iterator=np.linspace(extarms2["right"][0],extarms2["left"][0],50)
		for i in iterator :
			x1=retval2(i,armsc2)
			if len(x1)!=2 :
				#print x1
				continue
		
			x_a=(x1[0]+x1[1])/2
			radius = abs(x1[1]-x1[0])/2
			for th in theta :
				X.append(i)
				Y.append(yr+radius*np.cos(th))
				Z.append(x_a+radius*np.sin(th))

	
	points=np.array(points)
	theta=np.linspace(0,2*np.pi,30)
	if len(points) != 0 :
		t= float( points[1,1]- points[0,1])/(max(max(f1[:,1]),max(s1[:,1]))*0.01)
		iterator=np.linspace(points[0,1],points[1,1],abs(t))

	else :
		iterator=np.linspace(0,max(max(f1[:,1]),max(s1[:,1])),100)
#For every value in iterator plotting the data points considering ellipses
	for fl in iterator:
		x1=retval(fl,f1)
		y1=retval(fl,s1)
		if len(y1) !=2 :
			continue
		if len(x1)%2 !=0 or len(x1) >5 or len(x1) == 0:
			continue
		
		x_a=(x1[0]+x1[1])/2
		y_a=(y1[0]+y1[1])/2
		a=(x1[1]-x1[0])/2
		b=(y1[1]-y1[0])/2

		for temp in x_a+a*np.cos(theta) :
			X.append(temp)
		for temp in y_a+b*np.sin(theta) :
			Y.append(temp)
			Z.append(fl)
		if len(x1) ==4 :
			
			x_a=(x1[2]+x1[3])/2
			y_a=(y1[0]+y1[1])/2
			a=(x1[2]-x1[3])/2
			b=(y1[1]-y1[0])/2
			#print y1,b
			for temp in x_a+a*np.cos(theta) :
				X.append(temp)
			for temp in y_a+b*np.sin(theta) :
				Y.append(temp)
				Z.append(fl)
	fig=plt.figure()
	ax=fig.add_subplot(111,projection='3d')
#Using wireframe plots ( please improve this : spaces between legs is not clear, may use surface plots )
	ax.plot_wireframe(X,Y,Z,rstride=10,cstride=10)
	# Create cubic bounding box to simulate equal aspect ratio
	max_range = np.array([max(X)-min(X), max(Y)-min(Y),max(Z)-min(Z)]).max()
	Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
	Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
	Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
	for xb, yb, zb in zip(Xb, Yb, Zb):
	   ax.plot([xb], [yb], [zb], 'w')
	plt.show()
# manipulating the contour to set the lowest point to origin and the body in positive direction
