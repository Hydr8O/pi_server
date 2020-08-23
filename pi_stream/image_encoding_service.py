import cv2
import numpy as np

def image_to_bytes(image, format):
    '''Encodes image into bytes'''
    _, image= cv2.imencode(format, image)
    return image.tostring()

def image_from_bytes(image):
    '''Decodes image from bytes'''
    image = cv2.imdecode(np.frombuffer(image, np.uint8), 1)
    return image
