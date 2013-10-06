#!/usr/bin/env python
import cv, cv2, numpy
from lib.color_filter import ColorFilter
from lib.searcher import CheatSearcher
from lib.util import bounding_rect, crop, play_sound
from lib.window import Window
from pump import *

class Game(object):
    def __init__(self):
        self.color_range_bar = self.rect_points = None
        self.color_range_water = None
        self.check_points = self.start_points = None
    
    def start(self, video):
        ps = PumpSpark()
        '''
        ps.pump2([
          ([(1, 254), (4, 254)], 5), 
          ([(0, 254), (2, 254)], 1), 
          ([(2, 80), (5, 80)], 10),
          ([(1, 254), (4, 254)], 5)])  
        '''
        window = Window('Water Ira-Ira Bou')
        mask_window = Window('Mask')

        fps = video.get(cv.CV_CAP_PROP_FPS)
        if fps > 0:
            window.fps = fps

        h = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        w = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))

        rect = bounding_rect(self.rect_points)
        cfilter_bar = ColorFilter(self.color_range_bar)
        cfilter_water = ColorFilter(self.color_range_water)
        searcher_bar = CheatSearcher(self.check_points[0])
        searcher_water = CheatSearcher(self.check_points[1])

        colors = [(0, 255, 0), (255, 255, 0)]
        ret, frame = video.read()
        if not ret:
            'frame is null'
        
        bar_index = 0
        water_index = 0
        start = False
        print self.color_range_bar
        while True:
            key = window.wait()

            if key is ord('Q') or key is ord('q'):
                break

            ret, frame = video.read()
            if not ret:
                break

            current_img = crop(frame, rect)

            mask_bar = cfilter_bar.get_mask(current_img)
            mask_water = cfilter_water.get_mask(current_img)

            bar_index, (x, y) = searcher_bar.search(mask_bar, bar_index)
            cv2.circle(current_img, (x, y), 3, colors[0], thickness=2)
            
            water_index, (x, y) = searcher_water.search(mask_water, water_index)
            cv2.circle(current_img, (x, y), 3, colors[0], thickness=2)

            mask_window.draw(mask_bar)
            window.draw(current_img)
            
            if bar_index != 0 and start == False:
              play_sound('sound/button-8.wav')
              start = True
              ps.turnOff(1, 4)
              ps.pump([(0, 254), (3,254)], 0.5)
              ps.turnOn([(2, 70), (5, 70)])
            
        mask_window.close()
        window.close()
        ps.turnOff()
