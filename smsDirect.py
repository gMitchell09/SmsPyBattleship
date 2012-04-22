#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from googlevoice import *
from googlevoice.util import input

voice = Voice()
voice.login("george.mitchell91@gmail.com", "skateboarders")

phoneNumber = 2568569199
message = "Cron"
voice.send_sms(phoneNumber, message)
