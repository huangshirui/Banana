#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import os
import sys
import time
import signal


class Daemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pid_file, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pid_file = pid_file

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        # First fork (detaches from parent)
        try:
            if os.fork() > 0:
                raise SystemExit(0)  # Parent exit
        except OSError as e:
            raise RuntimeError('fork #1 failed: {0} ({1}).'.format(e.errno, e.strerror))

        # decouple from parent environment
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # Second fork (relinquish session leadership)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #2 failed: {0} ({1}).'.format(e.errno, e.strerror))

        # Flush I/O buffers
        sys.stdout.flush()
        sys.stderr.flush()

        # Replace file descriptors for stdin, stdout, and stderr
        with open(self.stdin, 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        # Write the PID file
        with open(self.pid_file, 'w') as f:
            print(os.getpid(), file=f)

        # Arrange to have the PID file removed on exit/signal
        atexit.register(lambda: os.remove(self.pid_file))

        # Signal handler for termination (required)
        def sigterm_handler(signo, frame):
            raise SystemExit(1)

        signal.signal(signal.SIGTERM, sigterm_handler)

    def start(self):
        """
        Start the daemon
        """
        try:
            # Check for a pidfile to see if the daemon already runs
            if os.path.exists(self.pid_file):
                raise RuntimeError('Already running')

            # Start the daemon
            self.daemonize()
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        if os.path.exists(self.pid_file):
            with open(self.pid_file) as f:
                pid = int(f.read())
                try:
                    while True:
                        os.kill(pid, signal.SIGTERM)
                        time.sleep(0.1)
                except OSError as e:
                    err = str(e)
                    if err.find("No such process") > 0:
                        if os.path.exists(self.pid_file):
                            os.remove(self.pid_file)
                    else:
                        print(str(err))
                        raise SystemExit(1)
        else:
            print('Not running', file=sys.stderr)
            raise SystemExit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
