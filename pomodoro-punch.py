#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
Pomodoro punch
@author: Paweł Mandera (pawel.mandera@runbox.com)

Tool integrating pomodoro technique with punch.py and todo.txt.
"""
import os
import subprocess
import time
import signal
import sys
from optparse import OptionParser

pomo_duration = 25                    # duration of one pomodoro (in minutes)
break_duration = 5                    # break duration (in minutes)
punch_cmd = '~/tools/punch/Punch.py'  # punch.py shell command

version = """Pomodoro punch"""
usage = """Usage:
    pomodoro-punch pomo           -- run one pomodoro
    pomodoro-punch in <task>      -- run one pomodoro and punch in <task>"""


class Pomodoro(object):
    def __init__(self, optlist, args):
        self.task_command = args[0] if len(args) else None
        self.task_id = args[1] if self.task_command == 'in' else None
        self.punched_in = False

    def execute(self):
        """Execute pomodoro workflow."""
        # if punch command is 'in' punch in
        if self.task_command == 'in':
            self.punch_in(self.task_id)
            time.sleep(5)
            self.pomodoro()
            self.punch_out()
        elif self.task_command is 'pomo':
            self.pomodoro()
        elif self.task_command is 'help':
            print usage
        else:
            print usage
        self.finish()

    def notify(self, title, body):
        """Display notification."""
        os.system("notify-send -a pomodoro -t 5000 -u critical \
                -i media-record '%s' '%s'" % (title, body))

    def play_sound(self):
        """Play sound (as separate process)."""
        # TODO: this is not the best command
        subprocess.Popen(['ogg123', '-qy 10',
                          '/usr/share/sounds/gnome/default/alerts/sonar.ogg'])

    def pomodoro(self):
        """Run one pomodoro."""
        self.notify('Pomodoro started!',
                    'You have only %s minutes.' % pomo_duration)
        for i in range(pomo_duration):
            # 'cls' for windows 'clear' for Linux and Mac
            os.system('cls' if os.name == 'nt' else 'clear')
            print 'Minutes left:', pomo_duration - i
            time.sleep(60)
        self.notify('Pomodoro ended!',
                    'Take %s minutes break.' % break_duration)
        self.play_sound()

    def punch_in(self, task_id):
        """Punch in - start counting time."""
        # TODO: make it return task and display it
        # in notification and on terminal
        os.system("%s in %s" % (punch_cmd, task_id))
        self.punched_in = True

    def punch_out(self):
        """Punch out - stop counting time."""
        os.system("%s out" % (punch_cmd))
        self.punched_in = False

    def finish(self):
        """Finish pomodoro"""
        if self.punched_in:
            self.punch_out()


if __name__ == '__main__':
    parser = OptionParser(usage=usage, version=version)
    optlist, args = parser.parse_args()
    # TODO: check if arguments are correct
    if False:
        pass
    else:
        pomodoro = Pomodoro(optlist, args)

        def graceful_exit(signal, frame):
            """Make sure to clean in case of foreceful stop."""
            pomodoro.finish()
            sys.exit(0)
        signal.signal(signal.SIGINT, graceful_exit)
        pomodoro.execute()
