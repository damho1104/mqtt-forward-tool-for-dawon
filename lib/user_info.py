#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib import SingleTone


class UserInfo(SingleTone):
    def __init__(self):
        super().__init__()
        self.sub_client_id = ''
        self.pub_client_id = ''
        self.ip = ''
        self.port = ''
