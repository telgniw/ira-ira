#!/usr/bin/env python
import cv2, numpy
from lib.window import *

class Main(object):
    def __init__(self):
        self.rect_points = self.video = None

    def open_video(self, video):
        self.video = cv2.VideoCapture(video)

    def set_area(self):
        if self.video is None:
            return

        ret, frame = self.video.read()
        if not ret:
            return

        self.rect_points = AreaSelectionUI(frame).get_selections()
        return self.rect_points

class AreaSelectionUI(MouseHandler):
    def __init__(self, frame):
        self.frame = frame

        self.click = self.window = None

    def _draw_circle(self, img, center, color):
        cv2.circle(img, center, 3, color, thickness=2)
        self.window.draw(img)

    def handle(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.click = (x, y)

            tmp = numpy.copy(self.frame)
            self._draw_circle(tmp, self.click, (255, 0, 255))

    def get_selections(self, n_selections=4):
        self.window = Window('Select Target Area')
        self.window.draw(self.frame)
        self.window.set_mouse_handler(self)

        # print instructions
        print 'click by mouse to make selection'
        print 'select in clockwise order starting from the upper-left corner'
        print 'press Y to confirm the selection on screen'
        print 'press Q to cancel the whole selection process'

        selections = []
        while len(selections) < n_selections:
            key = self.window.wait()

            if key is ord('Q') or key is ord('q'):
                selections = None
                break

            if self.click is None:
                continue

            if key is ord('Y') or key is ord('y'):
                click, self.click = self.click, None

                self._draw_circle(self.frame, click, (0, 255, 0))
                selections.append(click)

        self.window.close()
        return selections
