#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from collections import OrderedDict
import lib
from lib.log import log
from lib.config.config import ConfigLoader
from lib import Console, ExceptionUtil
from lib.mqtt.subscribe import MQTTSub
from lib.mqtt.publish import MQTTPub


def run_mqtt_forward(config: ConfigLoader):
    mqtt_info_dict: OrderedDict = config.get_info_dict()

    while True:
        try:
            lib.mqtt_pub = MQTTPub(mqtt_info_dict, config)
            lib.mqtt_sub = MQTTSub(mqtt_info_dict, config)
            lib.mqtt_sub.connect()
            lib.mqtt_sub.subscribe()
            lib.mqtt_sub.client.loop_forever()
            return True
        except Exception as e:
            Console.error_message(str(e))
            for element in ExceptionUtil.get_traceback_list():
                log.error(f'    {element}')
        finally:
            Console.warn_message('Connection failed unexpectedly.')
            Console.warn_message('wait 10 seconds and restart...')
            time.sleep(10)

