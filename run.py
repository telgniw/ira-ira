#!/usr/bin/env python
import cmd
from main import Main

class Cmd(cmd.Cmd):
    global main
    prompt = '/_> '

    def do_exit(self, _):
        return True

    def do_open(self, video):
        try:
            video = int(video)
        except ValueError:
            pass

        main.open_video(video)

    def do_set(self, what):
        if what == 'area':
            main.set_area()
        elif what == 'color':
            main.set_color()
        elif what == 'start':
            main.set_start()

if __name__ == '__main__':
    global main
    main = Main()

    Cmd().cmdloop()
