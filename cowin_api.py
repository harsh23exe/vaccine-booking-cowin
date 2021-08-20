from random import betavariate
import re
from PySimpleGUI.PySimpleGUI import SGrip as sg
from reportlab.graphics import renderPM
import requests
from requests.api import head
from requests.sessions import session
from svglib.svglib import svg2rlg
import logger
import json



prod_api = "https://cdn-api.co-vin.in/api"
test_api = "https://cdndemo-api.co-vin.in/api"
curr_api = prod_api
test_secret = "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi"
prod_secret = "U2FsdGVkX19mD56KTNfQsZgXJMwOG7u/6tuj0Qvil1LEjx783oxHXGUTDWYm+XMYVGXPeu+a24sl5ndEKcLTUQ=="
curr_secret = prod_secret


headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36", 
    "Accept" : "application/json, text/plain, */*",
    "Accept-Language" : "en-US,en;q=0.9" , 
    "authority": "cdn-api.co-vin.in",
    "accept-encoding": "gzip, deflate, br",
    "origin": "https://selfregistration.cowin.gov.in",
    "referer": "https://selfregistration.cowin.gov.in/",
    "scheme": "https"

    # "x-secret-key" : "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi"
}

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r



def generateOTP(mobile ):
    parameters = {
        "mobile": mobile,
        "secret": curr_secret
    }
    
    return requests.post(url =  curr_api + "/v2/auth/generateMobileOTP" , data =json.dumps(parameters), headers= headers)

def confirmOTP(txnID , otp):
    parameters = {
        "otp":otp,
        "txnId" : txnID
    }
    return requests.post(url = curr_api + "/v2/auth/validateMobileOtp", data= json.dumps(parameters) , headers = headers )

def beneficiaries(token):
    return requests.get(url=curr_api + "/v2/appointment/beneficiaries" , headers = headers , auth = BearerAuth(token))

def calendarByPin(pincode , date ,token , vaccine = None ):
    if(not(vaccine == None) ):
        parameters = {"pincode" : pincode , "date" : date , "vaccine" : vaccine}
    else :
        parameters= {"pincode" : pincode , "date" : date }
    return requests.get(url=curr_api + "/v2/appointment/sessions/calendarByPin" , headers= headers , params= parameters , auth=BearerAuth(token))

def publicPin():
    return requests.get(url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin" , headers = headers , params={"pincode" : "400064" , "date" : "01-06-2021"})


def captcha_builder(resp):
    with open('captcha.svg', 'w') as f:
        f.write(re.sub('(<path d=)(.*?)(fill=\"none\"/>)', '', resp['captcha']))

    drawing = svg2rlg('captcha.svg')
    renderPM.drawToFile(drawing, "captcha.png", fmt="PNG")

    layout = [[sg.Image('captcha.png')],
              [sg.Text("Enter Captcha Below")],
              [sg.Input()],
              [sg.Button('Submit', bind_return_key=True)]]

    window = sg.Window('Enter Captcha', layout)
    event, values = window.read()
    window.close()
    return values[1]
    

def generate_captcha(token):
    try:
        r = requests.post(url=curr_api + "/v2/auth/getRecaptcha", headers=headers ,auth = BearerAuth(token))
        if r.status_code == 200:
            return captcha_builder(r.json())
    except Exception as e:
        raise e
    print('Retrying captcha')
    return generate_captcha(token)

def book(token , center_id , session_id ,slot , benef_id , dose , captcha):
    data = {'center_id' : center_id ,
            'session_id' : session_id, 
            'slot' : slot , 
            'dose' : dose , 
            'benefeciaries' : [benef_id] ,
            'capctcha' : captcha
        }
    return requests.post(url = curr_api + "/v2/appointment/schedule" , data = json.dumps(data) , headers= headers , auth=BearerAuth(token))

        
    
