
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 21:13:12 2021

@author: Rehan Rajput
"""

import sqlalchemy as db
from datetime import datetime, timedelta
from sqlalchemy.sql import func 
engine = db.create_engine('sqlite:///adex.db')
connection = engine.connect()
meta = db.MetaData()

customer = db.Table('customer', \
                     meta, \
                     db.Column('id', db.Integer(), primary_key= True, nullable=False), \
                     db.Column('name', db.String(255), nullable=False), \
                     db.Column('active', db.Boolean(), nullable=False, default=1))


ip_blacklist = db.Table('ip_blacklist',\
                        meta, \
                        db.Column('ip', db.Integer(), primary_key=True, nullable=False))

ua_blacklist = db.Table('ua_blacklist',\
                        meta, \
                        db.Column('ua', db.String(255), primary_key=True, nullable=False))
    
hourly_stats = db.Table('hourly_stats',\
                        meta,\
                        db.Column('id', db.Integer(), primary_key=True, nullable = False),\
                        db.Column('customer_id', db.Integer(), nullable = False, unique=True),\
                        db.Column('time', db.DateTime(), nullable = False),\
                        db.Column('request_count', db.Integer(), nullable = False, default = 0),\
                        db.Column('invalid_count', db.Integer(), nullable = False, default = 0),\
                        db.UniqueConstraint('customer_id','time', name='unique_customer_time'),\
                        db.ForeignKeyConstraint(['customer_id'],['customers.id'],\
                                                name='hourly_stats_customer_id',\
                                                ondelete='CASCADE', onupdate='RESTRICT'))

##### check if customer present
query = db.select([customer]).where(customer.columns.id == 1)
ResultProxy = connection.execute(query)
Results = ResultProxy.fetchall()
print(Results)

##### check if blacklist IP present
query = db.select([ip_blacklist]).where(ip_blacklist.columns.ip == 0)
ResultProxy = connection.execute(query)
Results = ResultProxy.fetchall()
print(Results)

##### check if blacklist ua agent present
query = db.select([ua_blacklist]).where(ua_blacklist.columns.ua == "A6-Indexer")
ResultProxy = connection.execute(query)
Results = ResultProxy.fetchall()

## check if record exists:
time_now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
query = db.select([hourly_stats]).where(\
                                hourly_stats.columns.customer_id==3 and\
                                hourly_stats.columns.time==time_now)
ResultProxy = connection.execute(query)
Results = ResultProxy.fetchall()
print(Results)

#### Insert record
query = (db.insert(hourly_stats).values(\
                                        customer_id=3,\
                                        time = datetime.utcnow().replace(minute=0, second=0, microsecond=0))
          )
ResultProxy = connection.execute(query)

#### update Record
time_now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
query = (db.update(hourly_stats).\
             where(hourly_stats.columns.customer_id == 3 and hourly_stats.columns.time == time_now).\
                 values(request_count = hourly_stats.columns.request_count+1))
ResultProxy = connection.execute(query)

#### select for data
time_now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
time_tomorrow = time_now + timedelta(days=1)
query = (db.select([hourly_stats, func.sum(hourly_stats.columns.request_count + hourly_stats.columns.invalid_count).label('Total Requests')]).\
             where(hourly_stats.columns.customer_id == 3 and\
                   (hourly_stats.columns.time>=time_now and hourly_stats.columns.time < time_tomorrow)))
ResultProxy = connection.execute(query)
Results = ResultProxy.fetchall()
print(Results)


query = db.update(hourly_stats).\
             where(hourly_stats.columns.customer_id == 3 and hourly_stats.columns.time == time_now)
