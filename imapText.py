import imaplib
import re

M = imaplib.IMAP4_SSL("imap.googlemail.com", port=993)
M.login("google_account@gmail.com", "password")

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

M.select()

typ, data = M.search(None, 'UnSeen')
for num in data[0].split():
    typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
    numGroups = phonePattern.search(data[0][1]).groups() 
    print "(", numGroups[0], ")", numGroups[1], "-", numGroups[2]
    typ, data = M.fetch(num, '(UID BODY[TEXT])')
    print (data[0][1].split("\r\n\r\n")[0].replace("\n", ""))

M.close()
M.logout()
