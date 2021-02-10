# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:17:43 2021

@author: Rehan Rajput
"""

from abc import ABC, abstractmethod

class IDatabaseAdapter(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def loadTables(self):
        pass
    
    @abstractmethod
    def isCustomerPresent(self):
        pass
    
    @abstractmethod
    def isCustomerActiveAndActive(self):
        pass
    
    @abstractmethod
    def isIPBlacklisted(self):
        pass
    
    @abstractmethod
    def isUserAgentBlacklisted(self):
        pass
    
    @abstractmethod
    def insertValidHourlyStat(self):
        pass
    
    @abstractmethod
    def insertInvalidHourlyStat(self):
        pass
    
    @abstractmethod
    def generateStatistics(self):
        pass
    
    