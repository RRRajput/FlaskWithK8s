# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 20:06:45 2021

@author: Rehan Rajput
"""

import sqlalchemy as db
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from sqlalchemy.sql import func

from DatabaseAdapter import IDatabaseAdapter

class SqliteAdapter(IDatabaseAdapter):
    
    def __init__(self, path = 'sqlite:///adex.db'):
        self.engine = db.create_engine(path)
        self.connection = self.engine.connect()
        self.meta = db.MetaData()
        self.loadTables()
        
    def loadTables(self):
        self.customer = db.Table('customer', \
                             self.meta, \
                             db.Column('id', db.Integer(), primary_key= True, nullable=False), \
                             db.Column('name', db.String(255), nullable=False), \
                             db.Column('active', db.Boolean(), nullable=False, default=1))
        
        
        self.ip_blacklist = db.Table('ip_blacklist',\
                                self.meta, \
                                db.Column('ip', db.Integer(), primary_key=True, nullable=False))
        
        self.ua_blacklist = db.Table('ua_blacklist',\
                                self.meta, \
                                db.Column('ua', db.String(255), primary_key=True, nullable=False))
            
        self.hourly_stats = db.Table('hourly_stats',\
                                self.meta,\
                                db.Column('id', db.Integer(), primary_key=True, nullable = False),\
                                db.Column('customer_id', db.Integer(), nullable = False, unique=True),\
                                db.Column('time', db.DateTime(), nullable = False),\
                                db.Column('request_count', db.Integer(), nullable = False, default = 0),\
                                db.Column('invalid_count', db.Integer(), nullable = False, default = 0),\
                                db.UniqueConstraint('customer_id','time', name='unique_customer_time'),\
                                db.ForeignKeyConstraint(['customer_id'],['customers.id'],\
                                                        name='hourly_stats_customer_id',\
                                                        ondelete='CASCADE', onupdate='RESTRICT'))
    
    def isCustomerPresentAndActive(self, customer_id):
        query = db.select([self.customer]).\
                    where(self.customer.columns.id == customer_id)
        ResultProxy = self.connection.execute(query)
        Result = ResultProxy.fetchall()
        isPresent = len(Result) > 0
        isActive = isPresent and Result[0][-1]
        return (isPresent,isActive)
    
    def isIPBlacklisted(self, ip):
        query = db.select([self.ip_blacklist]).\
                    where(self.ip_blacklist.columns.ip == ip)
        ResultProxy = self.connection.execute(query)
        return len(ResultProxy.fetchall()) > 0
    
    def isUserAgentBlacklisted(self, userAgent):
        query = db.select([self.ua_blacklist]).\
                    where(self.ua_blacklist.columns.ua == userAgent)
        ResultProxy = self.connection.execute(query)
        return len(ResultProxy.fetchall()) > 0
    
    def insertValidHourlyStat(self, customer_id, now):
        if self.existsHourlyStat(customer_id, now):
            query = self.getUpdateQuery(customer_id, now)
            query = query.values(request_count = self.hourly_stats.columns.request_count+1)
        else:
            query = self.getInsertQuery(customer_id, now)
        self.connection.execute(query)
    
    def insertInvalidHourlyStat(self, customer_id, now):
        if self.existsHourlyStat(customer_id, now):
            query = self.getUpdateQuery(customer_id, now)
            query = query.values(invalid_count = self.hourly_stats.columns.invalid_count+1)
        else:
            query = self.getInsertQuery(customer_id, now, valid=False)
        self.connection.execute(query)
    
    def generateStatistics(self, customer_id, day):
        day_plus_one = day + timedelta(days=1)
        query = (db.select([self.hourly_stats, func.sum(self.hourly_stats.columns.request_count + self.hourly_stats.columns.invalid_count).label('Total Requests')]).\
                     where(and_(self.hourly_stats.columns.customer_id == customer_id,\
                            and_(func.date(self.hourly_stats.columns.time)>=day,
                             and_(func.date(self.hourly_stats.columns.time) < day_plus_one)))))
        ResultProxy = self.connection.execute(query)
        Results = ResultProxy.fetchall()
        return [dict(r) for r in Results]
    
    def existsHourlyStat(self, customer_id, now):
        query = db.select([self.hourly_stats]).\
                    where(\
                          and_(self.hourly_stats.columns.customer_id == customer_id,\
                          func.date(self.hourly_stats.columns.time) == now))
        ResultProxy = self.connection.execute(query)
        return len(ResultProxy.fetchall()) > 0
    
    def getUpdateQuery(self, customer_id, now):
        query = db.update(self.hourly_stats).\
                     where(and_(self.hourly_stats.columns.customer_id == customer_id, \
                           func.date(self.hourly_stats.columns.time) == now))
        return query
    
    def getInsertQuery(self, customerID, now, valid = True):
        requestCount = 1 if valid else 0
        invalidCount = 1 if not valid else 0
        query = db.insert(self.hourly_stats).values(\
                                        customer_id=customerID,\
                                        time = now,\
                                        request_count = requestCount,\
                                        invalid_count = invalidCount)
        return query