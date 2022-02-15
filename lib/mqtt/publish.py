#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import paho.mqtt.client as mqtt
import lib
from collections import OrderedDict

from lib.log import log
from lib.config.config import ConfigLoader
from lib.mqtt.mqtt import MQTT


class MQTTPub(MQTT):
    def __init__(self, device_dict: OrderedDict, config: ConfigLoader):
        super().__init__(device_dict, config)
        sub_dict: OrderedDict = device_dict.get('publish')

        self.is_cert_mode: bool = sub_dict.get('use_cert')
        self.ip: str = sub_dict.get('ip')
        self.port: str = sub_dict.get('port')
        self.user = sub_dict.get("user")
        self.password: str = sub_dict.get('password')
        self.client_id = sub_dict.get("client_id")

        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(self.user, self.password)
        self.is_connected = False

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_connect_fail = self.on_connect_fail

        lib.user_info.pub_client_id = self.client_id
        lib.user_info.ip = self.ip
        lib.user_info.port = self.port

    @staticmethod
    def on_connect_fail(client, userdata):
        log.warning(f"[{lib.user_info.pub_client_id}] Connection failed")

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info(f"[{lib.user_info.pub_client_id}] connected OK")
        else:
            if rc is None:
                rc = 'None'
            log.warning(f"[{lib.user_info.pub_client_id}] Bad connection Returned code={rc}")

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        log.info(f'[{lib.user_info.pub_client_id}] Disconnect {str(rc)}')
        log.info(f'[{lib.user_info.pub_client_id}] wait 5 seconds and re-connect')
        time.sleep(5)
        client.reconnect()

    @staticmethod
    def on_publish(client, userdata, mid):
        log.info(f"[{lib.user_info.pub_client_id}] In on_pub callback, mid = {mid}")

    def publish(self, send_dict: dict, topic):
        if not self.is_connected:
            self.connect()
            self.is_connected = True
        self.client.loop_start()
        self.client.publish(topic, json.dumps(send_dict), 1)
        self.client.loop_stop()
