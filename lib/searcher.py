#!/usr/bin/env python
import cv2, numpy
from util import blur

class Searcher(object):
    def search(self, img, start_point=None):
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

class CheatSearcher(Searcher):
    def __init__(self, check_points):
        self.check_points = check_points

    def search(self, img, start_point=None):
        end_point = start_point
        for (y, x) in self.check_points:
            if img[x][y] <= 0:
                break
            end_point = (y, x)

        return end_point

class FastSearcher(Searcher):
    N_HISTORY       = 30
    ERR_THRESHOLD   = 50

    def __init__(self, searcher=BFSearcher()):
        self.history, self.searcher = [], searcher

    def search(self, img, start_point=None):
        if len(self.history) < FastSearcher.N_HISTORY:
            diff = img
        else:
            p_img, p_point = self.history.pop(0)

            diff = (img - p_img).clip(min=0)

            if p_img[p_point[1]][p_point[0]] > 0:
                cv2.circle(diff, p_point, 3, (255, 255, 255), thickness=-1)

            start_point = p_point

        end_point = self.searcher.search(diff, start_point)

        if len(self.history) > 0:
            _, last_point = self.history[-1]
            diff_vec = numpy.array(end_point) - numpy.array(last_point)
            if numpy.linalg.norm(diff_vec) > FastSearcher.ERR_THRESHOLD:
                end_point = last_point

        self.history.append((numpy.copy(img), end_point))
        return end_point
