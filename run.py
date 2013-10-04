#!/usr/bin/env python
import cmd, os
from main import Main

class Cmd(cmd.Cmd):
    global main
    prompt = '/_> '

    def do_exit(self, _):
        return True

    def do_export(self, filename):
        main.export(filename)

    def do_import(self, filename):
        main.load(filename)

    def do_open(self, video):
        try:
            video = int(video)
        except ValueError:
            video = os.path.abspath(video)

        main.open_video(video)

    def do_start(self, _):
        main.game_start()

    def do_set(self, what):
        if what == 'area':
            main.set_area()
        elif what == 'color':
            main.set_color()
        elif what == 'check':
            main.set_check_points()
        elif what == 'start':
            main.set_start_points()
        else:
            print 'invalid argument'

    def do_skip(self, n_frames):
        try:
            n_frames = int(n_frames)
            main.skip_frames(n_frames)
        except ValueError:
            print 'invalid argument'

if __name__ == '__main__':
    global main
    main = Main()

    Cmd().cmdloop()
