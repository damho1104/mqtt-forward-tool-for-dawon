#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import multiprocessing
import signal
from lib.log import log
from lib import ExceptionUtil, Console, ConfigLoader
from lib.mode.parallel import run_pub_sub


def main():
    Console.title_message(f'MQTT Forward tool v1.0.1')
    try:
        config = ConfigLoader()
        # arg_list = [
        #     (device_name, config.get_root_cert_path(), config.get_client_cert_path(), config.get_client_cert_key_path())
        #     for device_name in config.get_device_list()]
        device_cnt = len(config.get_device_list())
        Console.info_message(f'The number of devices: {device_cnt}')

        with multiprocessing.Pool(device_cnt,
                                  log.multiprocess_init,
                                  initargs=[log.get_log_file_path()]) as pool:
            for device_name, result in pool.map(run_pub_sub, config.get_device_list()):
                log.warning(f'{device_name}: {result}')
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
