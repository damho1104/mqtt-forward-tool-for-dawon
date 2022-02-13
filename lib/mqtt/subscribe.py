#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time

import lib
import paho.mqtt.client as mqtt
from collections import OrderedDict

from lib.log import log
from lib.mqtt.mqtt import MQTT
from lib.mqtt.publish import MQTTPub

mqtt_pub: MQTTPub = None


class MQTTSub(MQTT):
    def __init__(self, device_name: str, device_dict: OrderedDict):
        super().__init__(device_name, device_dict)
        sub_dict: OrderedDict = device_dict.get('subscribe')

        self.is_cert_mode: bool = sub_dict.get('use_cert')
        self.ip: str = sub_dict.get('ip')
        self.port: str = sub_dict.get('port')
        self.password: str = sub_dict.get('password')

        # self.client_id = f'DAWONDNS-[DEVICE_NAME]'
        self.client_id = f'DAWONDNS-{device_name}'

        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(device_name, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_unsubscribe = self.on_unsubscribe

        lib.user_info.device_name = device_name
        lib.user_info.ip = self.ip
        lib.user_info.port = self.port

    @staticmethod
    def on_unsubscribe(client, userdata, mid):
        log.warning(f"[{lib.user_info.device_name}] [SUB] unsubscribe: {mid}")

    @staticmethod
    def on_connect_fail(client, userdata):
        log.warning(f"[{lib.user_info.device_name}] [SUB] Connection failed")

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info(f"[{lib.user_info.device_name}] [SUB] connected OK")
        else:
            log.warning(f"[{lib.user_info.device_name}] [SUB] Bad connection Returned code={rc}")

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        log.info(f'[{lib.user_info.device_name}] [SUB] {str(rc)}')
        log.info(f'[{lib.user_info.device_name}] [SUB] wait 5 seconds and re-connect')
        time.sleep(5)
        client.connect(lib.user_info.ip, lib.user_info.port)

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        log.info(f"[{lib.user_info.device_name}] [SUB] subscribed: {str(mid)} {str(granted_qos)}")

    @staticmethod
    def on_message(client, userdata, msg):
        global mqtt_pub
        payload_dict = json.loads(str(msg.payload.decode("utf-8")))
        mqtt_pub.publish(payload_dict)

    def subscribe(self):
        self.client.subscribe(self.topic)
        self.client.loop_forever()
