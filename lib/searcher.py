#!/usr/bin/env python
import cv2, numpy
from util import blur

class Searcher(object):
    def search(self, img, start_point):
        raise NotImplementedError

class BFSearcher(Searcher):
    def search(self, img, start_point):
        h, w = img.shape
        img = numpy.copy(img)

        def check(y, x):
            return 0 <= x < h and 0 <= y < w and img[x][y] > 0

        res_point, queue = start_point, [start_point]
        while len(queue) > 0:
            y, x = queue.pop(0)

            if not check(y, x):
                continue

            if check(y+1, x):
                queue.append((y+1, x))
            if check(y, x-1):
                queue.append((y, x-1))
            if check(y, x+1):
                queue.append((y, x+1))
            if check(y-1, x):
                queue.append((y-1, x))

            res_point, img[x][y] = (y, x), 0

        return res_point

class MeanSearcher(Searcher):
    def search(self, img, start_point):
        h, w = img.shape
        img = numpy.copy(img) / numpy.max(img)

        grid_x, grid_y = numpy.mgrid[0:h, 0:w]

        n_non_zeros = numpy.sum(img)
        mean_x = int(numpy.sum(numpy.multiply(img, grid_x)) / n_non_zeros)
        mean_y = int(numpy.sum(numpy.multiply(img, grid_y)) / n_non_zeros)
        res_point = (mean_y, mean_x)

        a, b = numpy.array(start_point), numpy.array(res_point)
        if numpy.linalg.norm(b - a) > 50:
            return start_point

        return res_point

class FastSearcher(Searcher):
    def __init__(self, searcher=MeanSearcher()):
        self.previous_img, self.previous_point = None, None
        self.searcher = searcher

    def search(self, img, start_point):
        # set negative values to 0
        if self.previous_img is None:
            diff = img
        else:
            p_img = blur(self.previous_img)
            _, p_img = cv2.threshold(p_img, 2, 255, cv2.THRESH_BINARY)

            diff = (img - p_img).clip(min=0)
            start_point = self.previous_point

        end_point = self.searcher.search(diff, start_point)
        self.previous_img, self.previous_point = numpy.copy(img), end_point
        return end_point
