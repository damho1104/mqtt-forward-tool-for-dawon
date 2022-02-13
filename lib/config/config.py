#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
#from collections import OrderedDict
from lib.util.file import FileUtil


class ConfigLoader:
    def __init__(self):
        self.config_path = FileUtil.get_path('config.json')
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(self.config_path)
        self.config_dict = FileUtil.get_json_content_from_path(self.config_path)

    def get_client_cert_path(self) -> str:
        return self.config_dict.get('certs', {}).get('client_cert_path', '')

    def get_client_cert_key_path(self) -> str:
        return self.config_dict.get('certs', {}).get('client_cert_key_path', '')

    def get_device_list(self) -> list:
        return [key for key in self.config_dict.keys() if key != 'certs']
