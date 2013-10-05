#!/usr/bin/env python
import cv, cv2, numpy
from lib.color_filter import ColorFilter
from lib.searcher import CheatSearcher
from lib.util import bounding_rect, crop
from lib.window import Window
from pump import *

class Game(object):
    def __init__(self):
        self.color_range = self.rect_points = None
        self.check_points = self.start_points = None
    
    def start(self, video):
        ps = PumpSpark()
        ps.turnOn([(1, 254), (4,254)])
        
        window = Window('Water Ira-Ira Bou')
        mask_window = Window('Mask')

        fps = video.get(cv.CV_CAP_PROP_FPS)
        if fps > 0:
            window.fps = fps

        h = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        w = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))

        rect = bounding_rect(self.rect_points)
        cfilter = ColorFilter(self.color_range)
        searcher = CheatSearcher(self.check_points[0])

        colors = [(0, 255, 0), (255, 255, 0)]
        index = 0
        start = False
        while True:
            key = window.wait()

            if key is ord('Q') or key is ord('q'):
                break

            ret, frame = video.read()
            if not ret:
                break

            img = crop(frame, rect)
            mask = cfilter.get_mask(img)

            index, (x, y) = searcher.search(mask, index)
            cv2.circle(img, (x, y), 3, colors[0], thickness=2)
            cv2.circle(img, (x, y), 10, colors[1], thickness=1)

            mask_window.draw(mask)
            window.draw(img)

            if index != 0 and start == False:
              start = True
              ps.turnOff(1, 4)
              ps.pump([(0, 254), (3,254)], 0.5)
              ps.turnOn([(2, 70), (5, 70)])

        mask_window.close()
        window.close()
        ps.turnOff()
