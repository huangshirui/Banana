# -*- coding: utf-8 -*-
import pyrebase

from conf.firebase import config as firebase_config


class Firebase:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(firebase_config)
