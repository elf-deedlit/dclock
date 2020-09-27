#!/usr/bin/env python3
# vim: set ts=4 sw=4 et smartindent ignorecase fileencoding=utf8:
import curses
import time
from math import floor
from datetime import datetime

NUM_DOT = (
    ('***** ',
     '*   * ',
     '*   * ',
     '*   * ',
     '***** ',),
    ('  *   ',
     '  *   ',
     '  *   ',
     '  *   ',
     '  *   ',),
    ('***** ',
     '    * ',
     '***** ',
     '*     ',
     '***** ',),
    ('***** ',
     '    * ',
     '***** ',
     '    * ',
     '***** ',),
    ('*   * ',
     '*   * ',
     '***** ',
     '    * ',
     '    * ',),
    ('***** ',
     '*     ',
     '***** ',
     '    * ',
     '***** ',),
    ('***** ',
     '*     ',
     '***** ',
     '*   * ',
     '***** ',),
    ('***** ',
     '*   * ',
     '*   * ',
     '    * ',
     '    * ',),
    ('***** ',
     '*   * ',
     '***** ',
     '*   * ',
     '***** ',),
    ('***** ',
     '*   * ',
     '***** ',
     '    * ',
     '***** ',),
)

COLON_DOT = (
    ('      ',
     '  *   ',
     '      ',
     '  *   ',
     '      ',)
)

def P(stdscr, msg):
    stdscr.addstr(0, 0, msg)
    stdscr.refresh()
    stdscr.getkey()

def view_dot(stdscr, xs, max_height, dot, scale):
    width = 5 * scale
    height = 5 * scale
    ys = floor((max_height - height) / 2 + 0.5)
    for y in range(0, int(height)):
        for x in range(0, int(width)):
            xn = floor((x + 0.5) / scale)
            yn = floor((y + 0.5) / scale)
            ch = dot[yn][xn]
            stdscr.addch(ys + y, xs + x, ch)

def view_num(stdscr, xs, max_height, num, scale):
    view_dot(stdscr, xs, max_height, NUM_DOT[num], scale)

def view_normal(stdscr, max_width, max_height, now):
    xs = floor((max_width - 8) / 2 + 0.5)
    ys = floor((max_height - 5) / 2 + 0.5)
    msg = now.strftime('%H:%M:%S')
    stdscr.addstr(ys, xs, msg)

def main(stdscr):
    stdscr.nodelay(True)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    num_width = width // 8
    scale = num_width / 6
    try:
        while True:
            now = datetime.now()
            hour = now.hour
            minutes = now.minute
            second = now.second
            if scale < 1.0:
                view_normal(stdscr, width, height, now)
            else:
                view_num(stdscr, 0, height, hour // 10, scale)
                view_num(stdscr, num_width, height, hour % 10, scale)
                view_dot(stdscr, num_width * 2, height, COLON_DOT, scale)
                view_num(stdscr, num_width * 3, height, minutes // 10, scale)
                view_num(stdscr, num_width * 4, height, minutes % 10, scale)
                view_dot(stdscr, num_width * 5, height, COLON_DOT, scale)
                view_num(stdscr, num_width * 6, height, second // 10, scale)
                view_num(stdscr, num_width * 7, height, second % 10, scale)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch == ord('q'):
                break
            elif ch == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                num_width = width // 8
                scale = num_width / 6
                stdscr.clear()
            wait_time = 1.0 - datetime.now().microsecond / 1000000.0
            time.sleep(wait_time)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    curses.wrapper(main)
