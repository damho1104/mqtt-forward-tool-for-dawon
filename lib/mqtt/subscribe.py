#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time

import lib
import paho.mqtt.client as mqtt
from collections import OrderedDict

from lib.log import log
from lib.config.config import ConfigLoader
from lib.mqtt.mqtt import MQTT


class MQTTSub(MQTT):
    def __init__(self, device_dict: OrderedDict, config: ConfigLoader):
        super().__init__(device_dict, config)
        sub_dict: OrderedDict = device_dict.get('subscribe')

        self.is_cert_mode: bool = sub_dict.get('use_cert')
        self.ip: str = sub_dict.get('ip')
        self.port: str = sub_dict.get('port')
        self.password: str = sub_dict.get('password')
        self.client_id = f'DAWONDNS-{self.mqtt_device_name}'

        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(self.mqtt_device_name, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_unsubscribe = self.on_unsubscribe
        self.is_reconnected = False

        self.make_topic()

        lib.user_info.device_name = self.mqtt_device_name
        lib.user_info.ip = self.ip
        lib.user_info.port = self.port

    def subscribe(self):
        self.subscribe_now(self.client, self.topic)

    @staticmethod
    def on_unsubscribe(client, userdata, mid):
        log.warning(f"[{lib.user_info.device_name}] [SUB] unsubscribe: {mid}")

    @staticmethod
    def on_connect_fail(client, userdata):
        log.warning(f"[{lib.user_info.device_name}] [SUB] Connection failed")
        MQTTSub.reconnect(client)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info(f"[{lib.user_info.device_name}] [SUB] connected OK")
            if lib.mqtt_sub.is_reconnected:
                MQTTSub.subscribe_now(client, lib.mqtt_sub.topic)
        else:
            log.warning(f"[{lib.user_info.device_name}] [SUB] Bad connection Returned code={rc}")

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        log.info(f'[{lib.user_info.device_name}] [SUB] disconnected {str(rc)}')
        MQTTSub.reconnect(client)

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        log.info(f"[{lib.user_info.device_name}] [SUB] subscribed: {str(mid)} {str(granted_qos)}")

    @staticmethod
    def on_message(client, userdata, msg):
        payload_dict = json.loads(str(msg.payload.decode("utf-8")))
        log.debug(msg.topic)
        lib.mqtt_pub.publish(payload_dict, msg.topic)

    @staticmethod
    def reconnect(client):
        log.info(f'[{lib.user_info.device_name}] [SUB] wait 5 seconds and re-connect')
        time.sleep(5)
        client.reconnect()
        lib.mqtt_sub.is_reconnected = True

    @staticmethod
    def subscribe_now(client, topic: str):
        client.subscribe(topic)
