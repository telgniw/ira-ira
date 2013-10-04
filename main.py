#!/usr/bin/env python
import cv2, pickle
from game import Game
from ui import *

from lib.util import mappings, remap

class Main(object):
    def __init__(self):
        self.video_source = self.video = None
        self.color_range = self.rect_points = None
        self.check_points = self.start_points = None

    def _get_video_frame(self):
        if self.video is None:
            return None

        ret, frame = self.video.read()
        if not ret:
            return None

        if self.rect_points is None:
            return frame

        map_x, map_y = mappings(frame.shape, self.rect_points)
        return remap(frame, map_x, map_y)

    def export(self, filename):
        with open(filename, 'w') as fout:
            fout.write(pickle.dumps((
                self.color_range,
                self.rect_points,
                self.check_points,
                self.start_points,
                self.video_source
            )))

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
        game.check_points = self.check_points
        game.start_points = self.start_points
        game.start(self.video)

    def load(self, filename):
        with open(filename, 'r') as fin:
            (
                self.color_range,
                self.rect_points,
                self.check_points,
                self.start_points,
                self.video_source
            ) = pickle.loads(''.join(fin.readlines()))

            self.open_video(self.video_source)

    def open_video(self, video):
        self.video_source = video
        self.video = cv2.VideoCapture(self.video_source)

    def set_area(self):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        self.rect_points = AreaSelectionUI(frame).get_selections(4)

    def set_check_points(self):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        self.check_points = []

        print 'select for the fist (upper) pipe'
        self.check_points.append(PointSelectionUI(frame).get_selections())

        print 'select for the second (lower) pipe'
        self.check_points.append(PointSelectionUI(frame).get_selections())

    def set_color(self):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        self.color_range = ColorSelectionUI(frame).get_selections()

    def set_start_points(self):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        self.start_points = PointSelectionUI(frame).get_selections(2)
        if self.start_points is None:
            return

        self.start_points = map(lambda p: (0, p[1]), self.start_points)

    def skip_frames(self, n_frames):
        while self._get_video_frame() is not None and n_frames > 0:
            n_frames -= 1
