# -*- coding: utf-8 -*-
# WakeOnLAN-API
# Project by https://github.com/rix1337

import multiprocessing

from wol_api import run

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run.main()
