#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ssl
import paho.mqtt.client as mqtt
from collections import OrderedDict
from lib.config.config import ConfigLoader
from lib.util.singletone import SingleTone


class MQTT(SingleTone):
    def __init__(self, device_dict: OrderedDict, config: ConfigLoader):
        super().__init__()
        self.config = config
        self.ip = ''
        self.port = -1
        self.topic_keyword = device_dict.get('topic')
        self.topic = None
        self.client_id = f'DAWONDNS-'
        self.mqtt_device_name = device_dict.get('mqtt_device_name')
        self.user = self.mqtt_device_name
        self.password = ''
        self.dawon_device_name = device_dict.get('device_name')
        self.dawon_device_id = device_dict.get('device_id')
        self.is_cert_mode = False
        self.client: mqtt.Client = None
        self.is_already_set_cert = False

    def make_topic(self):
        if self.topic is not None:
            return
        # self.topic = f'{self.topic_keyword}.v1/DAWONDNS-{self.dawon_device_name}-{self.dawon_device_id}/iot-server/notify/json'
        self.topic = f'{self.topic_keyword}/#'

    def connect(self):
        self.set_cert()
        self.client.connect(self.ip, self.port)

    def set_cert(self):
        if self.is_already_set_cert or not self.is_cert_mode:
            return
        self.client.tls_set(ca_certs=self.config.get_root_cert_path(),
                            certfile=self.config.get_client_cert_path(),
                            keyfile=self.config.get_client_cert_key_path(),
                            tls_version=ssl.PROTOCOL_TLSv1_2)
        self.is_already_set_cert = True
