#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import shelve

db = shelve.open("TwitShipDB");
db2 = shelve.open("msgDB");

db["unpairedList"] = []

db.close()
db2.close()
