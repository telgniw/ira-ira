#!/usr/bin/env python
import cv2
from game import Game
from ui import AreaSelectionUI, ColorSelectionUI

from lib.util import mappings, remap

class Main(object):
    def __init__(self):
        self.video = None
        self.color_range = self.rect_points = self.start_points = None

    def _get_video_frame(self):
        if self.video is None:
            return None

        ret, frame = self.video.read()
        if not ret:
            return None

        return frame

    def _get_video_frame_in_area(self):
        frame = self._get_video_frame()
        if frame is None:
            return None

        if self.rect_points is None:
            return frame

        map_x, map_y = mappings(frame.shape, self.rect_points)
        return remap(frame, map_x, map_y)

    def game_start(self):
        if self._get_video_frame() is None:
            print 'no video source'
            return

        if self.color_range is None:
            print 'no color-range selected'
            return

        if self.start_points is None:
            print 'no start-points selected'
            return

        game = Game()
        game.color_range = self.color_range
        game.rect_points = self.rect_points
        game.start_points = self.start_points
        game.start(self.video)

    def open_video(self, video):
        self.video = cv2.VideoCapture(video)

    def set_area(self):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        self.rect_points = AreaSelectionUI(frame).get_selections()

    def set_color(self):
        frame = self._get_video_frame_in_area()
        if frame is None:
            print 'no video source'
            return

        self.color_range = ColorSelectionUI(frame).get_selections()

    def set_start(self):
        frame = self._get_video_frame_in_area()
        if frame is None:
            print 'no video source'
            return

        self.start_points = AreaSelectionUI(frame).get_selections(2)
        self.start_points = map(lambda p: (0, p[1]), self.start_points)

    def skip_frames(self, n_frames):
        while self._get_video_frame() is not None and n_frames > 0:
            n_frames -= 1
