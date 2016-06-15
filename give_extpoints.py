def give_extpoints(f):
	fl=tuple(f[f[:,:,0].argmin()][0])
	fr=tuple(f[f[:,:,0].argmax()][0])
	 
	
	ft=tuple(f[f[:,:,1].argmin()][0])
	fb=tuple(f[f[:,:,1].argmax()][0])

	return {"top":ft,"left":fl,"right":fr,"bottom":fb}
def give_extpoints2(f):
	fl=tuple(f[f[:,0].argmin()])
	fr=tuple(f[f[:,0].argmax()])
	 
	
	ft=tuple(f[f[:,1].argmin()])
	fb=tuple(f[f[:,1].argmax()])

	return {"top":ft,"left":fl,"right":fr,"bottom":fb}
