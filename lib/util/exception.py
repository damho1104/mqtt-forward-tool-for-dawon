#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import traceback
from lib.util.console import Console


class ExceptionUtil:
    @staticmethod
    def get_traceback_list() -> list:
        lines = traceback.format_exc().strip().split('\n')
        rl = [lines[-1]]
        lines = lines[1:-1]
        lines.reverse()
        for i in range(0, len(lines), 2):
            if i + 1 >= len(lines):
                rl.append('* \t%s' % (lines[i].strip()))
            else:
                rl.append('* \t%s at %s' % (lines[i].strip(), lines[i + 1].strip()))
        return rl

    @staticmethod
    def receive_signal(signum, frame):
        Console.warn_message("Interrupt signal received.")
        Console.warn_message("Abort.")
        sys.exit(0)

