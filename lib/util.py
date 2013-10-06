#!/usr/bin/env python
import cv2, numpy
import pyaudio  
import wave  

def blur(img, s=5):
    return cv2.GaussianBlur(img, (s, s), 0)

def bgr2hsv(bgr_array):
    is_image = True

    # a single bgr color tuple, like red being (0, 0, 255)
    if type(bgr_array) is not numpy.ndarray:
        is_image = False
        bgr_array = numpy.array([[bgr_array]], dtype=numpy.uint8)

    hsv_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)

    if is_image:
        return hsv_array

    return tuple(map(int, hsv_array[0][0]))

def bounding_rect(rect_points):
    return cv2.boundingRect(numpy.array([rect_points]))

def crop(img, rect):
    x, y, h, w = rect
    return img[y:y+w, x:x+h]

def play_sound(name):

    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wave.open(name,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #paly stream  
    while data != '':  
        stream.write(data)  
        data = f.readframes(chunk)  

