#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

__author__ = "Marius Pozniakovas, Tomas Kučejevas"
__email__ = "pozniakovui@gmail.com"
'''script used to control a funny facebook bot'''

#main libraries
from fbchat import Message, log, Client
from fbchat.models import *

#for sending mail
import smtplib, ssl

#for getting systime
import datetime
from datetime import timedelta

#schedule jobs
import schedule
import time

#for password security
import getpass

#for Exceptions
import sys

#for nophone auth
import pyotp

#for various reasons
import os

#for random photo
from random import choice

#-------------------------------------------------------




#if we are using hardcoded data
data_from_file = True


data_arr = []
#fill empty array with passwords and other sensitive data
if data_from_file:
    with open('/home/marusqq/Facebook_bot/data.bin') as file:
        for line in file:
            line = line.rstrip()
            line = line.lstrip()
            data_arr.append(line)
else:
    data_arr.append('Facebook login:')
    data_arr.append(input('Facebook login ----> '))

    data_arr.append('Facebook password:')
    psw = getpass.getpass(prompt = 'Facebook password ---> ', stream = None)
    data_arr.append(psw)

    data_arr.append('Gmail bot login:')
    data_arr.append(input('Gmail bot username ----> '))

    data_arr.append('Gmail bot password:')
    psw = getpass.getpass(prompt = 'Gmail bot password ---> ', stream = None)
    data_arr.append(psw)

    data_arr.append('TOPT auth key:')
    data_arr.append(input('TOPT auth key ----->'))

    data_arr.append('Group Thread ID:')
    data_arr.append(input('Group Thread ID ----->'))

#-------------------------------------------------------

#0. start the script
print ('Bot Started!!!!')

#1. connect to client
username = data_arr[1]
password = data_arr[3]


#overloading client function onMessage
class FacebookBot(Client):
    def on2FACode(self):
        totp = pyotp.TOTP(data_arr[9])
        code = totp.now()
        return code

#connect to fb
client = FacebookBot(username, password, max_tries = 2)



#2. read msg_no
msg_no_file = open('/home/marusqq/Facebook_bot/reminder/times.txt', 'r')
msg_no = msg_no_file.read()

if msg_no is not None:
    message_number = msg_no
else:
    message_number = 0

def schedule_rafal_reminders():
    #testing:
    #schedule.every().minute.do(sendReminder)

    timesheet = ["04:20", "11:11", "16:20"]
    print('Times when the bot will send a reminder: ')
    print (timesheet)

    #main schedule, looks stupid but looping through timesheet doesnt work :(
    schedule.every().day.at("02:20").do(sendReminder)
    schedule.every().day.at("09:11").do(sendReminder)
    schedule.every().day.at("14:20").do(sendReminder)

    return

def _get_dirlist(rootdir):

    dirlist = []

    with os.scandir(rootdir) as rit:
        for entry in rit:
            if not entry.name.startswith('.') and entry.is_dir():
                dirlist.append(entry.path)
                dirlist += _get_dirlist(entry.path)

    dirlist.sort()
    return dirlist



def sendInfo(mes, subject = None):
    '''this is used for sending a message to mail'''

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = data_arr[5]  # Enter your address
    receiver_email = data_arr[5]  # Enter receiver address
    password = data_arr[7]



    message = """\
Subject: """ + subject + """
    \n""" + mes

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def sendReminder():
    '''send a reminder to Rafal'''

    global message_number
    message_number = int(message_number)

    #get systime
    dt = datetime.datetime.now() + timedelta(hours = 2)
    date = dt.strftime('%Y-%m-%d %H:%M')

    #get a random photos
    photos = []
    with os.scandir('/home/marusqq/Facebook_bot/reminder/photos/') as root_dir:
        for entry in root_dir:
                if entry.is_file():
                    photos.append(entry.path)

    #print(photos)
    randomPhoto = choice(photos)

    print ('Sending a reminder to facebook!')
    print ('Send Date: ' + str(date))
    print ('No#: ' + str(message_number))

    #process the message
    MESSAGE = '[' + date + ']  #' + str(message_number+1) + ' PRIMINIMAS:'

    #set our group info and group thread type
    threadID = data_arr[11]
    threadTYPE = ThreadType.GROUP

    #grupei
    client.sendLocalImage(randomPhoto, message = Message(text = MESSAGE), thread_id = threadID, thread_type = threadTYPE)

    #tomui:
    #client.sendLocalImage("reminder/photo.jpg", message = Message(text = MESSAGE), thread_id = 100001826192111)

    #mariui:
    #client.sendLocalImage("reminder/photo.jpg", message = Message(text = MESSAGE), thread_id = 1100000105556453)

    #aurelijai
    #client.sendLocalImage(randomPhoto, message = Message(text = MESSAGE), thread_id = 100002227277241)

    #stickeris
    #client.send(Message(sticker=Sticker("177583982712301")), thread_id=100002227277241)

    #get one more
    message_number = message_number + 1

    print ('Waiting for the next reminder\n\n')

#3. do when SCHEDULED
    #3.1 rafal reminders
schedule_rafal_reminders()

random = []

print ('---------------------------------------------')
print ('Rafal reminders scheduled!')
print ('---------------------------------------------')

#main loop
try:
    while True:
        #check if we have any jobs to do, if none, wait for 1 second
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print('Script stopped by KeyboardInterrupt')

except:
    print ('Script has crashed :(')
    e = sys.exc_info()[0]
    print ('Exception that caused this: ' + str(e))
    msg_no_file = open('/home/marusqq/Facebook_bot/reminder/times.txt', 'w+')
    msg_no_file.write(str(message_number))
    msg_no_file.close()
    sendInfo(str(e), 'SCRIPT CRASH!')
    quit()