#!/usr/bin/env python3a
# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# launchs - small-side, single-line steam game launcher in python
#
# github.com/ferhatgec/launchs

from os import getenv, listdir
from pathlib import Path


class launchs_info:
    def __init__(self):
        self.app_name = ''
        self.app_exec = ''
        self.category = ''


class launchs:
    def __init__(self):
        home = getenv('HOME')

        self.check(f'{home}/.steam/steam/steamapps/common/')
        self.check(f'{home}/.local/share/applications/')

        self.dir = f'{home}/.steam/steam/steamapps/common/'
        self.desktop_dir = f'{home}/.local/share/applications/'
        self.dir_games = listdir(self.dir)
        self.desktop_apps = listdir(self.desktop_dir)

        self.games = []

        self.is_start = False

        for app in self.desktop_apps:
            app = app.split('.')[0]
            for game in self.dir_games:
                if app == game:
                    self.games.append(self.parse(app))

    def check(self, file: str):
        if not Path(file).exists():
            exit(f'directory not exists: {file}')

    def parse(self, app_name: str) -> launchs_info:
        init_app = launchs_info()

        with open(f'{self.desktop_dir}{app_name}.desktop', 'r') as file:
            for line in file:
                if 'Name=' in line:
                    init_app.app_name = line.split('Name=')[1].strip()
                elif 'Exec=' in line:
                    init_app.app_exec = line.split('Exec=')[1].strip()
                elif 'Categories=' in line:
                    init_app.category = line.split('Categories=')[1].split(';')[0].strip()

        return init_app

    def select(self):
        from subprocess import run, PIPE
        i = 0

        print(end=f'\033[2K\033[1G\x1b[1;97m{self.games[0].app_name}', flush=True)

        while True:
            if self.is_start:
                print(end=f'\033[2K\033[1G{self.games[i].app_name}', flush=True)
                self.is_start = False

            data = self.getchar()

            print(end='\033[2K\033[1G', flush=True)

            if ord(data) == 65 and i > 0:
                i -= 1
                print(end=self.games[i].app_name, flush=True)
            elif ord(data) == 66 and i < len(self.games) - 1:
                i += 1
                print(end=self.games[i].app_name, flush=True)
            elif ord(data) == 13:
                run(self.games[i].app_exec.split(' '), stdout=PIPE)
                self.is_start = True
            elif ord(data) == 101:
                exit(1)

    @staticmethod
    def getchar():
        from sys import stdin
        from termios import tcgetattr, tcsetattr, TCSADRAIN
        from tty import setraw

        fd = stdin.fileno()
        old_settings = tcgetattr(fd)

        try:
            setraw(fd)
            ch = stdin.read(1)
        finally:
            tcsetattr(fd, TCSADRAIN, old_settings)

        return ch


init = launchs()
init.select()
