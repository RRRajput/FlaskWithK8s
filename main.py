# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 20:58:53 2021

@author: Rehan Rajput
"""

import json
from flask import Flask, request, jsonify
from datetime import datetime
from Handler import *
from SqliteAdapter import SqliteAdapter

## defining the flask part
app = Flask(__name__)

## initializing the database adapter
adapter = SqliteAdapter('sqlite:///adex.db?check_same_thread=False')

## chain of responsbility for getting statistics from the get method
getStatKeys = ["customerID","date"]
jsonfields_getStat = JSONFieldsHandler(getStatKeys)
customerPresent_getStat = CustomerPresentHandler(adapter)
getStat = StatisticsHandler(adapter)

jsonfields_getStat.set_next(\
    customerPresent_getStat).set_next(\
    getStat)
                                              
@app.route('/user/<customer_id>', methods=['GET'])
def query_records(customer_id=None):
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
def update_record():
    record = json.loads(request.data)
    return jsonify(record)

app.run(debug=True, use_reloader=False)