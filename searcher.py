#!/usr/bin/env python
import cv2, numpy

class Searcher(object):
    def search(self, img, start_point):
        raise NotImplementedError

class BFSearcher(Searcher):
    def search(self, img, start_point):
        h, w, d = img.shape

        if d is 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = numpy.copy(img)
        res = numpy.zeros((h, w, 3), dtype=numpy.uint8)

        def check(y, x):
            return 0 <= x < h and 0 <= y < w and img[x][y] > 0

        queue = [start_point]
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

            img[x][y], res[x][y] = 0, (204, 204, 255)

        return res, (y, x)
