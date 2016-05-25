import cv2

def resize(image, width = 500):
    '''
    there is some issue for some images
    '''
    print(image.shape)
    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))

    resized = cv2.resize(image, dim, fx=0, fy=0)
    return resized
