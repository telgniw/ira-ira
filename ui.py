#!/usr/bin/env python
import cv2, numpy
from lib.color_filter import ColorFilter
from lib.window import *

class MouseSelectionUI(MouseHandler):
    def __init__(self, frame):
        self.frame = numpy.copy(frame)
        self.click = None

    def _on_mouse(self, click):
        raise NotImplementedError

    def _pre_selections(self):
        raise NotImplementedError

    def _print_instructions(self):
        raise NotImplementedError

    def _post_selections(self, selections):
        raise NotImplementedError

    def _process(self, click):
        raise NotImplementedError

    def get_selections(self, n_selections=None):
        self._pre_selections()

        print
        print 'click by mouse to make selection'
        print 'press Y to confirm the selection on screen'
        print 'press S to complete the selection process'
        print 'press Q to cancel the whole selection process'
        print

        self._print_instructions()
        print

        key_cmp = lambda k, c: k is ord(c.upper()) or k is ord(c.lower())
        selections = []
        while n_selections is None or len(selections) < n_selections:
            key = self.window.wait()

            if key_cmp(key, 's'):
                break
            if key_cmp(key, 'q'):
                selections = []
                break

            if self.click is None:
                continue
            if key_cmp(key, 'y'):
                click, self.click = self.click, None
                selections.append(click)

                self._process(click)

        if len(selections) == 0:
            selections = None

        return self._post_selections(selections)

    def handle(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click = (x, y)
            self._on_mouse(self.click)

class PointSelectionUI(MouseSelectionUI):
    def _on_mouse(self, click):
        tmp = numpy.copy(self.frame)
        cv2.circle(tmp, click, 3, (255, 0, 255), thickness=2)
        self.window.draw(tmp)

    def _pre_selections(self):
        self.window = Window('Select Points')
        self.window.draw(self.frame)
        self.window.set_mouse_handler(self)

    def _print_instructions(self):
        pass

    def _post_selections(self, selections):
        self.window.close()

        print 'points selected:', selections
        return selections

    def _process(self, click):
        cv2.circle(self.frame, click, 3, (0, 255, 0), thickness=2)
        self.window.draw(self.frame)

class AreaSelectionUI(PointSelectionUI):
    def _print_instructions(self):
        print 'select in clock-wise order starting from the upper-left corner'

class ColorSelectionUI(MouseSelectionUI):
    def _get_color_range(self, selections):
        colors = [
            tuple(map(int, self.original_frame[x][y]))
            for (y, x) in selections
        ]
        return ColorFilter.get_range(colors)

    def _on_mouse(self, click):
        tmp = numpy.copy(self.frame)
        cv2.circle(tmp, click, 3, (255, 0, 255), thickness=2)
        self.window.draw(tmp)

        color_range = self._get_color_range(self.current_selections + [click])
        mask = ColorFilter(color_range).get_mask(self.original_frame)
        self.preview_window.draw(mask)

    def _pre_selections(self):
        self.window = Window('Select Points')
        self.window.draw(self.frame)
        self.window.set_mouse_handler(self)

        self.preview_window = Window('Preview')
        self.preview_window.draw(
            numpy.zeros(self.frame.shape, dtype=numpy.uint8)
        )

        self.original_frame = numpy.copy(self.frame)
        self.current_selections = []

    def _print_instructions(self):
        pass

    def _post_selections(self, selections):
        self.window.close()
        self.preview_window.close()

        color_range = self._get_color_range(selections)
        print 'hsv color range:', color_range
        return color_range

    def _process(self, click):
        self.current_selections.append(click)

        cv2.circle(self.frame, click, 3, (0, 255, 0), thickness=2)
        self.window.draw(self.frame)
