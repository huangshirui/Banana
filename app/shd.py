#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from core.dispatcher import Dispatcher
from utils.daemon import Daemon
from utils.log import configure_logging


class SmartHomeDaemon(Daemon):
    def run(self):
        Dispatcher().run()


if __name__ == "__main__":
    configure_logging()
    daemon = SmartHomeDaemon('/tmp/shd.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
            raise SystemExit(1)
    else:
        print('Usage: {} [start|stop|restart]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)
