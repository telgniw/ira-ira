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

def mappings(img, rect_points):
    h, w, _ = img.shape
    ul, ur, br, bl = rect_points

    grid_x, grid_y = numpy.mgrid[0:h, 0:w].astype(numpy.float32)
    grid_xr, grid_yr = numpy.flipud(grid_x), numpy.fliplr(grid_y)

    mx = ((ul[1] * grid_yr + ur[1] * grid_y) * grid_xr + \
        (bl[1] * grid_yr + br[1] * grid_y) * grid_x) / (h * w)
    my = ((ul[0] * grid_yr + ur[0] * grid_y) * grid_xr + \
        (bl[0] * grid_yr + br[0] * grid_y) * grid_x) / (h * w)

    return mx, my

def remap(img, mx, my=None):
    return cv2.remap(img, mx, my, cv2.INTER_LINEAR)
