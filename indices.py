def give_index_h(contour,height):
	x=[]
	for i in range(0,len(contour)-2):
		if i%2==0:
			continue
		a=contour[i,0,1]-height
		b=contour[i+2,0,1]-height
		if a == 0:
			x.append(i)
		elif a*b<0:
			#print i,contour[i],'\n',i+2,contour[i+2]
			x.append(i+1)
	return x
def give_index_v(contour,dist):
	x=[]
	for i in range(0,len(contour)-2):
		if i%2==0:
			continue
		a=contour[i,0,0]-dist
		b=contour[i+2,0,0]-dist
		if a == 0:
			x.append(i)
		elif a*b<0:
			#print i,contour[i],'\n',i+2,contour[i+2]
			x.append(i+1)
	return x
def give_index_h1(contour,height):
	x=[]
	for i in range(0,len(contour)-2):
		if i%2==0:
			continue
		a=contour[i,1]-height
		b=contour[i+2,1]-height
		if a == 0:
			x.append(i)
		elif a*b<0:
			#print i,contour[i],'\n',i+2,contour[i+2]
			x.append(i+1)
	return x
def give_index_v1(contour,dist):
	x=[]
	for i in range(0,len(contour)-2):
		if i%2==0:
			continue
		a=contour[i,0]-dist
		b=contour[i+2,0]-dist
		if a == 0:
			x.append(i)
		elif a*b<0:
			#print i,contour[i],'\n',i+2,contour[i+2]
			x.append(i+1)
	return x
