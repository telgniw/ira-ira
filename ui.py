#!/usr/bin/env python
import cv2, numpy
from lib.color_filter import ColorFilter
from lib.window import *

class MouseSelectionUI(MouseHandler):
    def _draw_circle(self, img, center, color):
        cv2.circle(img, center, 3, color, thickness=2)
        self.window.draw(img)

    def get_selections(self):
        raise NotImplementedError

class AreaSelectionUI(MouseSelectionUI):
    def __init__(self, frame):
        self.frame = frame
        self.click = self.window = None

    def handle(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.click = (x, y)

            tmp = numpy.copy(self.frame)
            self._draw_circle(tmp, self.click, (255, 0, 255))

    def get_selections(self, n_selections=4):
        self.window = Window('Select Points')
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

        # print result and return
        print 'points selected:', selections
        return selections

class ColorSelectionUI(MouseSelectionUI):
    def __init__(self, frame):
        self.original_frame, self.frame = numpy.copy(frame), frame
        self.click = self.preview_window = self.window = None

    def _draw_preview(self, selections):
        color_range = ColorFilter.get_range(selections)
        mask = ColorFilter(color_range).get_mask(self.original_frame)
        self.preview_window.draw(mask)

    def _get_color(self, point):
        return tuple(map(int,
            self.original_frame[point[1]][point[0]]
        ))

    def handle(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.click = (x, y)

            tmp = numpy.copy(self.frame)
            self._draw_circle(tmp, self.click, (255, 0, 255))

            color = self._get_color(self.click)
            self._draw_preview(self.selections + [color])

    def get_selections(self):
        self.window = Window('Select Points')
        self.window.draw(self.frame)
        self.window.set_mouse_handler(self)

        self.preview_window = Window('Preview')
        self.preview_window.draw(
            numpy.zeros(self.frame.shape, dtype=numpy.uint8)
        )

        # print instructions
        print 'click by mouse to make selection'
        print 'press Y to confirm the selection on screen'
        print 'press S to complete the selection process'
        print 'press Q to cancel the whole selection process'

        self.selections = []
        while True:
            key = self.window.wait()

            if key is ord('S') or key is ord('s'):
                break

            if key is ord('Q') or key is ord('q'):
                self.selections = None
                break

            if self.click is None:
                continue

            if key is ord('Y') or key is ord('y'):
                click, self.click = self.click, None

                self._draw_circle(self.frame, click, (0, 255, 0))
                color = self._get_color(click)
                self.selections.append(color)

        self.preview_window.close()
        self.window.close()

        if self.selections is None or len(self.selections) <= 0:
            return None

        color_range = ColorFilter.get_range(self.selections)
        print 'hsv color range:', color_range
        return color_range
