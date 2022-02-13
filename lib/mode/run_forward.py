#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
import lib
from lib.config.config import ConfigLoader
from lib.mqtt.subscribe import MQTTSub
from lib.mqtt.publish import MQTTPub


def run_mqtt_forward(config: ConfigLoader):
    mqtt_info_dict: OrderedDict = config.get_info_dict()

    lib.mqtt_pub = MQTTPub(mqtt_info_dict, config)
    lib.mqtt_sub = MQTTSub(mqtt_info_dict, config)
    lib.mqtt_sub.connect()
    lib.mqtt_sub.subscribe()
    lib.mqtt_sub.client.loop_forever()
    return True

