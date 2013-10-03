#!/usr/bin/env python
import cv, cv2, numpy
from lib.color_filter import ColorFilter
from lib.searcher import FastSearcher
from lib.util import mappings, remap
from lib.window import Window

class Game(object):
    def __init__(self):
        self.color_range = self.rect_points = self.start_point = None
    
    def start(self, video):
        window = Window('Water Ira-Ira Bou')
        mask_window = Window('Mask')

        fps = video.get(cv.CV_CAP_PROP_FPS)
        if fps > 0:
            window.fps = fps

        h = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        w = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))

        map_x, map_y = mappings((h, w), self.rect_points)
        cfilter = ColorFilter(self.color_range)
        searchers = []
        for _ in self.start_points:
            searchers.append(FastSearcher())

        colors = [(0, 255, 0), (255, 255, 0)]

        while True:
            key = window.wait()

            if key is ord('Q') or key is ord('q'):
                break

            ret, frame = video.read()
            if not ret:
                break

            img = remap(frame, map_x, map_y)
            mask = cfilter.get_mask(img)

            for i, start_point in enumerate(self.start_points):
                (x, y) = searchers[i].search(mask, start_point)
                cv2.circle(img, (x, y), 3, colors[i], thickness=2)

            mask_window.draw(mask)
            window.draw(img)

        mask_window.close()
        window.close()
