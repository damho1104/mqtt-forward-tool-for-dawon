#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ssl
import paho.mqtt.client as mqtt
from collections import OrderedDict
from lib.config.config import ConfigLoader


class MQTT:
    def __init__(self, device_name: str, device_dict: OrderedDict):
        self.ip = ''
        self.port = -1
        self.topic_keyword = device_dict.get('topic')
        self.topic = ''
        self.client_id = f'DAWONDNS-'
        self.user = device_name
        self.password = ''
        self.dawon_device_name = device_dict.get('device_name')
        self.dawon_device_id = device_dict.get('device_id')
        self.is_cert_mode = False
        self.client: mqtt.Client = None

    def make_topic(self):
        self.topic = f'{self.topic_keyword}.v1/DAWONDNS-{self.dawon_device_name}-{self.dawon_device_id}/iot-server/notify/json'

    def connect(self):
        self.make_topic()
        if self.is_cert_mode:
            config = ConfigLoader()
            self.client.tls_set(certfile=config.get_client_cert_path(),
                                keyfile=config.get_client_cert_key_path(),
                                tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.connect(self.ip, self.port)