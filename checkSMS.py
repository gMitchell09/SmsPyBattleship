#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from googlevoice import Voice, util
from time import sleep
import sys
import BeautifulSoup
import shelve
import imaplib
import re
from twitShip import *
import logging

logging.basicConfig(filename='checkSMS.log',level=logging.WARNING)

voice = Voice()
M = imaplib.IMAP4_SSL("imap.googlemail.com", port=993)

def initVoice():
    logging.debug("Init Voice")
    try:
        voice.login()
    except:
        logging.warning("Error logging into voice")
        sys.exit()
    logging.debug("Logged In")

def initIMAP():
    logging.debug("Logging in to IMAP")
    try:
        M.login("smsgameapi@gmail.com", "password")
    except:
        logging.warning("ERROR LOGGING IN TO IMAP")
        sys.exit()
        
    logging.debug("Login Successful :)")

initVoice()
initIMAP()

M.select()

phonePattern = re.compile(r'''
                # don't match beginning of string, number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
               # end of string
    ''', re.VERBOSE)

looping = 1
smsErrors = 0
imapErrors = 0

while(looping):
    try:
        M.select()
        ptyp, data = M.search(None, 'UnSeen')
        for num in data[0].split():
            typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
            numGroups = phonePattern.search(data[0][1]).groups() 
            phoneNumber = int(numGroups[0] + numGroups[1] + numGroups[2])
            typ, data = M.fetch(num, '(UID BODY[TEXT])')
            dataMsg = (data[0][1].split("\r\n\r\n")[0].replace("\n", ""))
            logging.debug(str(phoneNumber) +  ' - ' + dataMsg)
            twitShipMain(phoneNumber, dataMsg)
    except:
        #For some reason we cannot select the mailbox... so let's try reconnecting?
        logging.warning("Error retrieving IMAP")
        imapErrors += 1
        if(imapErrors >= 5):
            logging.warning("Restarting IMAP")
            M.close()
            M.logout()
            initIMAP()
    
        

    msgFile = shelve.open("msgDB")
    if(msgFile):
        for msg in msgFile:
            try:
                #logging.debug(str((msgFile[msg])['phoneNumber']) + " - " + msgFile[msg])
                voice.send_sms((msgFile[msg])['phoneNumber'], (msgFile[msg])['message'])
                del msgFile[msg]
            except:
                logging.warning("Error sending sms")
                smsErrors += 1
                if(smsErrors >= 5):
                    voice.logout()
                    initVoice()

    logging.debug("Sleeping")
    sleep(5)

M.close()
M.logout()
