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

def view_dot(stdscr, xs, dot, scale):
    width = 5 * scale
    height = 5 * scale
    for y in range(0, int(height)):
        for x in range(0, int(width)):
            xn = floor((x + 0.5) / scale)
            yn = floor((y + 0.5) / scale)
            ch = dot[yn][xn]
            stdscr.addch(y, xs + x, ch)

def view_num(stdscr, xs, num, scale):
    view_dot(stdscr, xs, NUM_DOT[num], scale)

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
            view_num(stdscr, 0, hour // 10, scale)
            view_num(stdscr, num_width, hour % 10, scale)
            view_dot(stdscr, num_width * 2, COLON_DOT, scale)
            view_num(stdscr, num_width * 3, minutes // 10, scale)
            view_num(stdscr, num_width * 4, minutes % 10, scale)
            view_dot(stdscr, num_width * 5, COLON_DOT, scale)
            view_num(stdscr, num_width * 6, second // 10, scale)
            view_num(stdscr, num_width * 7, second % 10, scale)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch == ord('q'):
                break
            elif ch == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                num_width = width // 8
                scale = num_width / 6
                stdscr.clear()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    curses.wrapper(main)
