#!/usr/bin/env python
import cv2, numpy
from util import blur, bgr2hsv

class ColorFilter(object):
    def __init__(self, color_range):
        self.lower_color, self.upper_color = color_range

    def get_mask(self, img):
        img = blur(img)
        hsv_img = bgr2hsv(img)

        mask = cv2.inRange(hsv_img, self.lower_color, self.upper_color)

        # blurring and thresholding twice
        for i in range(2):
            mask = blur(mask)
            _, mask = cv2.threshold(mask, 2, 255, cv2.THRESH_BINARY)

        return mask

    @staticmethod
    def get_range(colors):
        hsv_colors = map(bgr2hsv, colors)
        if len(hsv_colors) < 2:
            return (hsv_colors[0], hsv_colors[0])

        lower_color = tuple(map(int, map(min, *hsv_colors)))
        upper_color = tuple(map(int, map(max, *hsv_colors)))
        return (lower_color, upper_color)
