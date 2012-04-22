#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from googlevoice import *
from googlevoice.util import input
import cgi

print "Content-Type: text/html;charset=utf-8"
print

print "<html><head><title>SMS Gateway</title></head><body>"

form = cgi.FieldStorage()
if form.has_key('phoneNumber') and form['phoneNumber'].value != "":
    voice = Voice()
    voice.login("george.mitchell91@gmail.com", "skateboarders")

    phoneNumber = form["phoneNumber"].value
    message = form["message"].value
    voice.send_sms(phoneNumber, message)
    print "Message Sent :)"

print "<form method='POST' action='http://gmitchell09.alwaysdata.net/smsSend.py'>"
print "<p>Phone Number: <input type='text' name='phoneNumber'></p>"
print "<p>Message: <input type='text' name='message'></p>"
print "<input type='submit'></form>"
print "</body></html>"
