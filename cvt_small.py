#!usr/bin/python
import sys
import cv2
import numpy as np
'''
import os
os.mkdir('new')
os.chdir('new')	
os.chdir('../')
#except :	
#	os.mkdir('new')

'''
oi=cv2.imread('shirt2.jpg')
ni=cv2.resize(oi,(int(oi.size[1]*0.3),int(oi.size[0]*0.3)),interpolation=cv2.INTER_CUBIC)
cv2.imwrite('asd'+i,ni)

