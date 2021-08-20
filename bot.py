import os
from shutil import copyfile
from cowin_api import beneficiaries, book, calendarByPin, confirmOTP, generateOTP, generate_captcha, publicPin
import requests
from requests import status_codes
from requests.api import head, request
import logger
import logging
import json
import time
import hashlib
import configparser


logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")


if not os.path.isfile("config.ini"):
    try:
        copyfile("default_config.ini", "config.ini")
        logger.log("Config file config.ini not found, generating a new one from default_config.ini", "warning")
    except:
        logger.log("Neither config.ini , nor default_config.ini do not exist, cannot create bot." , "CRITICAL")
        os.system.exit(1)


config = configparser.ConfigParser()
config.read("config.ini")


mobile_no = config["Info"]["mobile"]
date =config["Info"]["date"]
pincode = config["Info"]["pincode"]
dose =config["Info"]["dose"]
age_limit = config["Info"]["age_limit"]    
benefeciary_ID = config["Info"]["beneficiary_id"]
# district_id = "395"

txnId = ""
token =""

def authenticate():

    data = generateOTP(mobile_no )
    logger.log(data.text , str(data.status_code))
    if(data.status_code != 200):
        return
        
    txnId = data.json()["txnId"]
    print("Enter OTP  :" , end= " ")
    otp = input()
    otp = hashlib.sha256(otp.encode()).hexdigest()

    data = confirmOTP(txnId , otp)
    logger.log(data.text , str(data.status_code))

    if(data.status_code == 200):
        print("Authenticated !")
    else: 
        print("Error Occured. Check log file.")
        exit(1)
    

    global token
    token = data.json()["token"]

def benef():
    data = beneficiaries(token)
    # print(data.json())
    print(data.text)
    logger.log(data.text , str(data.status_code))

def findSlot():
    while(True):

        data = calendarByPin(pincode , date , token )

        if(data.status_code == 401):
            logger.log("authenticating again")
            authenticate()
            continue

        elif(data.status_code != 200):
            logger.log(data.text)
            print("Error Occured. Check log file ")
            exit(1)

        for center in data:
            slots = center['sessions'][0]['available_capacity_dose' + dose]
            vaccine = center['sessions'][0]['vaccine']
            center_name = center['name']
            if(slots > 1 and age_limit >= int(center['min_age_limit'])):
                return center


def bookSlot(center):
    center_id = center['center_id']
    session_id = center['sessions'][0]['session_id']
    slot = center['sessions'][0]['slots'][0]

    captcha = generate_captcha(token)
    
    data = book(token=token , center_id= center_id, session_id= session_id , slot=slot , benef_id=benefeciary_ID , dose=dose , captcha=captcha)
    logger.log(data.text)
    if(data.status_code == 200):
        print("Slot booked. Check log for details.")
        exit(0)
    elif(data.status_code == 409):
        print("Unlucky")
        return 
    else: 
        print("Error Occured. Check log file.")
        exit(1)


if __name__ == "__main__": 
    
    authenticate()
    while(True):
        center = findSlot()
        bookSlot(center)

    



