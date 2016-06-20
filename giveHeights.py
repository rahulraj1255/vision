from give_extpoints import give_extpoints
import cv2
from outer import encContour
def giveHeights(ref,height,args):
	rext=give_extpoints(encContour(ref))
	scaling=float(rext["bottom"][1]-rext["top"][1])/height
	for i in args :
		print i
		xext=give_extpoints(encContour(i))
		print "Height of "+i+" is :",float(xext["bottom"][1]-xext["top"][1])/scaling
