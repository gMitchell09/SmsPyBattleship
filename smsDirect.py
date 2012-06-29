#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from googlevoice import *
from googlevoice.util import input

voice = Voice()
voice.login("voice_account@gmail.com", "password")

phoneNumber = 9999999999
message = "Cron"
voice.send_sms(phoneNumber, message)
