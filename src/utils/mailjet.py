# import the mailjet wrapper
from mailjet_rest import Client
import os
from flask import current_app

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
from_email="advise.ly1@gmail.com"

def sendForget(user,url):
    data = {
    'Messages': [
        {
        "From": {
            "Email": from_email,
            "Name": "Advise Ly"
        },
        "To": [
            {
            "Email": user.email,
            "Name": user.username
            }
        ],
        "TemplateID": 1107554,
		"TemplateLanguage": True,
        "Variables":{
            "firstname":user.username,
            "resetUrl":url+"/"+user.reset_password_token,
            "subject":"[RecoFinement] Reset Your Password"
        }
        },      
    ],
    }
    result = mailjet.send.create(data=data)
    return result.status_code

def sendReset(user,url):
    
    data = {
    'Messages': [
        {
        "From": {
            "Email": from_email,
            "Name": "Advisely"
        },
        "To": [
            {
            "Email": user.email,
            "Name": user.username
            }
        ],
        "TemplateID": 1817695,
		"TemplateLanguage": True,
        "Variables":{
            "firstname":user.username,
            "resetUrl":url,
            "subject":"[RecoFinement] Successful reset password"
        }
        },      
    ],
    }
    result = mailjet.send.create(data=data)
    return result.status_code
    