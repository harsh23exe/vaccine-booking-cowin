import requests
from requests.api import head
import logger
import json



prod_api = "https://cdn-api.co-vin.in/api"
test_api = "https://cdndemo-api.co-vin.in/api"
curr_api = prod_api


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



def generateOTP(mobile , secret):
    parameters = {
        "mobile": mobile,
        "secret": secret
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

def calendarByPin(pincode , date , vaccine = None):
    if(not(vaccine == None) ):
        parameters = {"pincode" : pincode , "date" : date , "vaccine" : vaccine}
    else :
        parameters= {"pincode" : pincode , "date" : date }
    return requests.get(url=curr_api + "/v2/appointment/sessions/calendarByPin" , headers= headers , params= parameters)

def publicPin():
    return requests.get(url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin" , headers = headers , params={"pincode" : "400064" , "date" : "01-06-2021"})



        
    
