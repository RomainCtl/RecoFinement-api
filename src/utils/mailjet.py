# import the mailjet wrapper
from mailjet_rest import Client
import os
from flask import current_app
from settings import API_KEY,API_SECRET,MAILJET,FROM_EMAIL



def sendForget(user,url):
    data = {
    'Messages': [
        {
        "From": {
            "Email": FROM_EMAIL,
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
    result = MAILJET.send.create(data=data)
    return result.status_code

def sendReset(user,url):
    
    data = {
    'Messages': [
        {
        "From": {
            "Email": FROM_EMAIL,
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
    result = MAILJET.send.create(data=data)
    return result.status_code