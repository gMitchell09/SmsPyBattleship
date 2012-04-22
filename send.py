#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import shelve

def Send(msg, num):
    message = {"phoneNumber": num, "message": msg}
    db = shelve.open("msgDB")
    db[str(num+len(db))] = message
