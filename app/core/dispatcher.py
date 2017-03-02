# -*- coding: utf-8 -*-
import time

import logging


class Dispatcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Starting dispatcher ...')
        while True:
            time.sleep(0.1)
