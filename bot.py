# from os import stat
from cowin_api import beneficiaries, calendarByPin, confirmOTP, generateOTP, publicPin
import requests
from requests import status_codes
from requests.api import head, request
import logger
import logging
import json
import time
import hashlib


logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")


mobile_no = "7506149022"
pincode = "400064"
token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJjNDkyNWVmNi04ODgxLTQ4OWEtYWQ1ZS1hMzI3YzZiNzQwMDgiLCJ1c2VyX2lkIjoiYzQ5MjVlZjYtODg4MS00ODlhLWFkNWUtYTMyN2M2Yjc0MDA4IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo3NTA2MTQ5MDIyLCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjM0MzMyNzE3ODE5OTEwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwic291cmNlIjoiY293aW4iLCJ1YSI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85MS4wLjQ0NzIuNzcgU2FmYXJpLzUzNy4zNiIsImRhdGVfbW9kaWZpZWQiOiIyMDIxLTA2LTA2VDExOjQ5OjA4LjAyMVoiLCJpYXQiOjE2MjI5ODAxNDgsImV4cCI6MTYyMjk4MTA0OH0.ZsnNhYECqDGup6XvfSyC4_oHozLwybrAQdtuDxY_DYU"
txnId = ""
district_id = "395"
age_limit = 18
benefeciary_ID = ""
prod_api = "https://cdn-api.co-vin.in/api"
test_api = "https://cdndemo-api.co-vin.in/api"
curr_api = test_api 
test_secret = "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi"
prod_secret = "U2FsdGVkX19mD56KTNfQsZgXJMwOG7u/6tuj0Qvil1LEjx783oxHXGUTDWYm+XMYVGXPeu+a24sl5ndEKcLTUQ=="
curr_secret = prod_secret


def authenticate():

    data = generateOTP(mobile_no , curr_secret)
    logger.log(data.text , str(data.status_code))
    if(data.status_code != 200):
        return
        
    txnId = data.json()["txnId"]
    print("Enter OTP  :" , end= " ")
    otp = input()
    otp = hashlib.sha256(otp.encode()).hexdigest()

    data = confirmOTP(txnId , otp)
    logger.log(data.text , str(data.status_code))

    while(data.status_code != 200) :
        print(data.status_code)
        time.sleep(30)
        data = confirmOTP(txnId , otp)
        logger.log(data.text , str(data.status_code))

    global token
    token = data.json()["token"]

def benef():
    data = beneficiaries(token)
    # print(data.json())
    print(data.text)
    logger.log(data.text , str(data.status_code))


# authenticate()
benef()


# data = confirmOTP(txnID="dd470ce3-9f26-46be-9bb8-05b5d7114049" , otp = hashlib.sha256('800580'.encode()).hexdigest())
# print(data.text)
# logger.log(data.text , str(data.status_code))

