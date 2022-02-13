#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
from lib.config.config import ConfigLoader
from lib.mqtt import subscribe
from lib.mqtt.publish import MQTTPub


def run_mqtt_forward(config: ConfigLoader):
    mqtt_info_dict: OrderedDict = config.get_info_dict()

    subscribe.mqtt_pub = MQTTPub(mqtt_info_dict, config)
    mqtt_sub = subscribe.MQTTSub(mqtt_info_dict, config)
    mqtt_sub.connect()
    mqtt_sub.subscribe()

    return True

