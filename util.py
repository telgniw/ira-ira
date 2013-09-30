#!/usr/bin/env python
import cv2, numpy

def blur(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def bgr2hsv(bgr_array):
    is_image = True

    # a single bgr color tuple, like red being (0, 0, 255)
    if type(bgr_array) is not numpy.ndarray:
        is_image = False
        bgr_array = numpy.array([[bgr_array]], dtype=numpy.uint8)

    hsv_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)

    if is_image:
        return hsv_array

    return tuple(hsv_array[0][0])
