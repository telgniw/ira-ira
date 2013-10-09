#!/usr/bin/env python
import cv2, pickle
from game import Game
from ui import *
from lib.window import Window
from lib.util import bounding_rect, crop

class Main(object):
    def __init__(self):
        self.video_source = self.video = None
        self.color_range_bar = self.rect_points = None
        self.color_range_water = None
        self.check_points = self.start_points = None

    def _get_video_frame(self, is_crop=True):
        if self.video is None:
            return None

        cv2.namedWindow('tmp')

        ret, frame = self.video.read()
        while not ret:
            ret, frame = self.video.read()
            cv2.waitKey(100)

        cv2.destroyWindow('tmp')
        if (self.rect_points is None) or (is_crop is False):
            return frame

        rect = bounding_rect(self.rect_points)
        return crop(frame, rect)

    def export(self, filename):
        with open(filename, 'w') as fout:
            fout.write(pickle.dumps((
                self.color_range_bar,
                self.color_range_water,
                self.rect_points,
                self.check_points,
                self.start_points,
                self.video_source
            )))

    def game_start(self):
        if self._get_video_frame() is None:
            print 'no video source'
            return

        if self.color_range_bar is None:
            print 'no color-range selected'
            return

        if self.start_points is None:
            print 'no start-points selected'
            return

        game = Game()
        game.color_range_bar = self.color_range_bar
        game.color_range_water = self.color_range_water
        game.rect_points = self.rect_points
        game.check_points = self.check_points
        game.start_points = self.start_points
        game.start(self.video)

    def load(self, filename):
        with open(filename, 'r') as fin:
            (
                self.color_range_bar,
                self.color_range_water,
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
        frame = self._get_video_frame(is_crop=False)
        if frame is None:
            print 'no video source'
            return

        self.rect_points = AreaSelectionUI(frame).get_selections(4)

    def set_check_points(self, kind='both'):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        if len(self.check_points) == 0:
            self.check_points = [None, None]

        if kind == 'both' or kind == 'bar':
            print 'select for the bar'
            self.check_points[0] = PointSelectionUI(frame).get_selections()
        
        if kind == 'both' or kind == 'water':
            print 'select for the pipe'
            self.check_points[1] = PointSelectionUI(frame).get_selections()

    def checkbar(self):
        self.set_check_points(kind = 'bar')

    def checkwater(self):
        self.set_check_points(kind = 'water')

    def set_color(self, kind='both'):
        frame = self._get_video_frame()
        if frame is None:
            print 'no video source'
            return

        if kind == 'both' or kind == 'bar':
            self.color_range_bar = ColorSelectionUI(frame).get_selections()

        if kind == 'both' or kind == 'water':
            self.color_range_water = ColorSelectionUI(frame).get_selections()

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

    def tune(self):
        tune_window = Window('Tune Window')
        colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255)]

        print
        print 'press Q to cancel the whole selection process'
        print

        while True:
            frame = self._get_video_frame()

            for p in self.rect_points:
                cv2.circle(frame, p, 3, colors[0], thickness=2)
            
            for p in self.check_points[0]:
                cv2.circle(frame, p, 3, colors[1], thickness=2)

            for p in self.check_points[1]:
                cv2.circle(frame, p, 3, colors[2], thickness=2)

            for p in self.start_points:
                cv2.circle(frame, p, 3, colors[3], thickness=2)

            tune_window.draw(frame)

            key_cmp = lambda k, c: k is ord(c.upper()) or k is ord(c.lower())
            key = tune_window.wait()
            if key_cmp(key, 'q'):
                tune_window.close()
                break; 
