#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-05 19:20:34
from flask import Flask
import logging
import os

app = Flask(__name__)
app.secret_key = "thisissecretkey"

from app.controller.main import *

