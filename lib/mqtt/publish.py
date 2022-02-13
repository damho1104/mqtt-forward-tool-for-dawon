#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt
import lib
from collections import OrderedDict

from lib.log import log
from lib.mqtt.mqtt import MQTT


class MQTTPub(MQTT):
    def __init__(self, device_name: str, device_dict: OrderedDict):
        super().__init__(device_name, device_dict)
        sub_dict: OrderedDict = device_dict.get('publish')

        self.is_cert_mode: bool = sub_dict.get('use_cert')
        self.ip: str = sub_dict.get('ip')
        self.port: str = sub_dict.get('port')
        self.password: str = sub_dict.get('password')

        # self.client_id = f'DAWONDNS-[DEVICE_ID]'
        self.client_id = f'DAWONDNS-{self.dawon_device_id}'

        self.client = mqtt.Client(self.client_id)
        # self.client.username_pw_set([DEVICE_ID], [PASSWORD])
        self.client.username_pw_set(self.dawon_device_id, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_connect_fail = self.on_connect_fail

        lib.user_info.device_name = device_name

        self.connect()

    @staticmethod
    def on_connect_fail(client, userdata):
        log.warning(f"[{lib.user_info.device_name}] [PUB] Connection failed")

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info(f"[{lib.user_info.device_name}] [PUB] connected OK")
        else:
            log.warning(f"[{lib.user_info.device_name}] [PUB] Bad connection Returned code={rc}")

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        log.info(f'[{lib.user_info.device_name}] [PUB] Disconnect {str(rc)}')

    @staticmethod
    def on_publish(client, userdata, mid):
        log.info(f"[{lib.user_info.device_name}] [PUB] In on_pub callback, mid = {mid}")

    def publish(self, send_dict: dict):
        self.client.loop_start()
        self.client.publish(self.topic, json.dumps(send_dict), 1)
        self.client.loop_stop()
