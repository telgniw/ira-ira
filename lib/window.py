#!/usr/bin/env python
import cv2

class Window(object):
    def __init__(self, name):
        self.name = name
        self.fps, self.size = 30.0, None

        cv2.namedWindow(self.name)

    def close(self):
        cv2.destroyWindow(self.name)

    def draw(self, img):
        if self.size:
            img = cv2.resize(img, size)
        cv2.imshow(self.name, img)

    def set_mouse_handler(self, handler):
        cv2.setMouseCallback(self.name, handler.handle)

    def wait(self, key_to_wait=None):
        key = cv2.waitKey(int(1000.0 / self.fps))
        
        if key_to_wait is None:
            return key

        return key is ord(key_to_wait)

class MouseHandler(object):
    def handle(self, event, x, y, flag, param):
        raise NotImplementedError
