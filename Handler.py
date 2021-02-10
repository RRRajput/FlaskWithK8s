# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:04:38 2021

@author: Rehan Rajput
"""

from abc import ABC, abstractmethod
from DatabaseAdapter import IDatabaseAdapter
import json

class AbstractHandler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """
    def __init__(self):
        self._success_handler = None
        self._failure_handler = None
    
    def set_next(self, successHandler, failureHandler = None):
        self._success_handler = successHandler
        self._failure_handler = failureHandler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # handler_1.set_next(handler_2).set_next(handler_3)
        return successHandler

    @abstractmethod
    def handle(self):
        pass

class MalformedJSONHandler(AbstractHandler):
    
    def handle(self, inputData):
        try:
            outputData = json.loads(inputData)
            return self._success_handler.handle(outputData)
        except ValueError:
            return "Malformed JSON"

class JSONFieldsHandler(AbstractHandler):
    def __init__(self, keys):
        self.__keys = set(keys)
        super().__init__(self)
        
    def handle(self, inputData):
        if set(inputData.keys()) == self.__keys:
            return self._success_handler.handle(inputData)
        return "ERROR: Keys required: {0}\nKeys Provided: {1}".format(self.__keys,inputData.keys())

class CustomerPresentAndActiveHandler(AbstractHandler):
    def __init__(self, database):
        self.__database = database
        super().__init__(self)
        
    def handle(self, inputData):
        customerID = inputData["customerID"]
        isPresent, isActive = database.isCustomerPresentAndActive(customerID)
        if isPresent and isActive:
            return self._success_handler.handle(inputData)
        elif isPresent:
            error_message = "ERROR: Customer ID {0} not active in database".format(customerID)
            return self._failure_handler.handle(customerID, error_message)
        return "Customer ID {0} is not in database".format(customerID)

class IPBlacklistHandler(AbstractHandler):
    def __init__(self, database):
        self.__database = database
        super().__init__(self)
        
    def handle(self, inputData):
        customerID = inputData["customerID"]
        ip = inputData["remoteIP"]
        if not database.isIPBlacklisted(ip):
            return self._success_handler.handle(inputData)
        error_message = "ERROR: IP {0} is blacklisted".format(ip)
        return self._failure_handler.handle(customerID, error_message)
    
class UserAgentBlacklistHandler(AbstractHandler):
    def __init__(self, database):
        self.__database = database
        super().__init__(self)
        
    def handle(self, inputData):
        customerID = inputData["customerID"]
        userAgent = inputData["userID"]
        if not database.isUserAgentBlacklisted(userAgent):
            return self._success_handler.handle(inputData)
        error_message = "ERROR: User Agent {0} is blacklisted".format(userAgent)
        return self._failure_handler.handle(customerID, error_message)

class RequestCountHandler(AbstractHandler):
    def __init__(self, database):
        self.__database = database
        super().__init__(self)
        
    def handle(self, inputData):
        customerID = inputData["customerID"]
        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        database.insertValidHourlyStat(customerID, now)
        return self._success_handler.handle(inputData)
    
class InvalidCountHandler(AbstractHandler):
    def __init__(self, database):
        self.__database = database
        super().__init__(self)
        
    def handle(self, customerID, message):
        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        database.insertValidHourlyStat(customerID, now)
        return "{0}\nInvalid Request received by customer ID {1}".format(message, customerID)
    
class ValidRequestHandler(AbstractHandler):
    def handle(self, inputData):
        # TODO: The Stub function for all valid requests
        return "Valid Request Received"