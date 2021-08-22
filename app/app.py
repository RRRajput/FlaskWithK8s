# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 20:58:53 2021

@author: Rehan Rajput
"""

from flask import Flask, request
from datetime import datetime
import os
from Handler import (
    JSONFieldsHandler,
    CustomerPresentHandler,
    StatisticsHandler,
    CustomerPresentAndActiveHandler,
    IPBlacklistHandler,
    UserAgentBlacklistHandler,
    RequestCountHandler,
    InvalidCountHandler,
    ValidRequestHandler,
    MalformedJSONHandler
)
from SQLDatabase import SQLDatabase

## defining the flask part
app = Flask(__name__)

## initializing the database adapter
database_address = os.environ['DATABASE_ADDRESS']
adapter = SQLDatabase(database_address)

## chain of responsbility for getting statistics from the get method
getStatKeys = ["customerID","date"]
jsonfields_getStat = JSONFieldsHandler(getStatKeys)
customerPresent_getStat = CustomerPresentHandler(adapter)
getStat = StatisticsHandler(adapter)

jsonfields_getStat.set_next(\
    customerPresent_getStat).set_next(\
    getStat)
                                      
## chain of responsibility for get commands
malformed_request = MalformedJSONHandler()
requestKeys = ["customerID","tagID","userID","remoteIP","timestamp"]
jsonfields_request = JSONFieldsHandler(requestKeys)
customerPandA_request = CustomerPresentAndActiveHandler(adapter)
ipblacklist_request = IPBlacklistHandler(adapter)
uablacklist_request = UserAgentBlacklistHandler(adapter)
validCounter_request = RequestCountHandler(adapter)
invalidCounter_request = InvalidCountHandler(adapter)
valid_request = ValidRequestHandler()

malformed_request.set_next(jsonfields_request).\
    set_next(customerPandA_request).\
    set_next(ipblacklist_request,invalidCounter_request).\
    set_next(uablacklist_request,invalidCounter_request).\
    set_next(validCounter_request,invalidCounter_request).\
    set_next(valid_request)

@app.route('/user/<customer_id>', methods=['GET'])
def getStatistics(customer_id=None):
    if customer_id is None:
        return "No customer ID given"
    try:
        date = request.args.get('date')
        date = datetime.strptime(date, '%d-%m-%Y')
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    except:
        return "The correct format for the date is dd-mm-yyyy"
    
    inputData = {"customerID":customer_id,"date":date}
    return jsonfields_getStat.handle(inputData)


@app.route('/', methods=['POST'])
def postRequest():
    return malformed_request.handle(request.data)

if __name__=="__main__":
    app.run()
