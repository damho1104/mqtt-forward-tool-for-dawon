#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import multiprocessing
import signal
from lib.log import log
from lib import ExceptionUtil, Console, ConfigLoader
from lib.mode.run_forward import run_mqtt_forward


def main():
    Console.title_message(f'MQTT Forward tool v1.0.3')
    try:
        config = ConfigLoader()
        run_mqtt_forward(config)
        return True
    except Exception as e:
        Console.error_message(str(e))
        Console.error_message(f'Please check the log(File: "{log.get_log_file_path()}").')
        for trace in ExceptionUtil.get_traceback_list():
            log.error(f'    {trace}')
        return False


if __name__ == '__main__':
    log.init()
    multiprocessing.freeze_support()
    signal.signal(signal.SIGINT, ExceptionUtil.receive_signal)
    if main():
        sys.exit(0)
    sys.exit(1)
