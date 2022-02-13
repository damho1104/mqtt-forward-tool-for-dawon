#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing
from collections import OrderedDict
from lib.util.console import Console
from lib.config.config import ConfigLoader
from lib.mqtt import subscribe
from lib.mqtt.publish import MQTTPub

execute_counter = multiprocessing.Value('i', 0)


def run_pub_sub(arg_packed):

    global execute_counter
    device_name = arg_packed

    with execute_counter.get_lock():
        Console.check_message(f'Device: {device_name}')

    config = ConfigLoader()
    device_dict: OrderedDict = config.config_dict.get(device_name)

    subscribe.mqtt_pub = MQTTPub(device_name, device_dict)
    mqtt_sub = subscribe.MQTTSub(device_name, device_dict)
    mqtt_sub.connect()
    mqtt_sub.subscribe()

    return device_name, True

