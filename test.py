#from resize_model import resize_model
from resize_model import resize_model
from ret_hscale import ret_hscale
'''
 This is the test file of ret_hscale
 assuming that the real image is girl_front.jpg (as the hands down image of man.jpg was not available :P ) and model image is mfront.jpg 
'''
resize_model('man_front.jpg','man_frontf.jpg','man_side.jpg','girl_front.jpg')

ret_hscale('girl_front.jpg','mfront.jpg',('mfront.jpg','mfrontf.jpg'))
