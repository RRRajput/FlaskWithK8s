# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 21:13:12 2021

@author: Rehan Rajput
"""

import sqlalchemy as db

engine = db.create_engine('sqlite:///adex.db')
connection = engine.connect()
meta = db.MetaData()

customers = db.Table('customers', \
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

# CREATE TABLE `hourly_stats` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `customer_id` int(11) unsigned NOT NULL,
#   `time` timestamp NOT NULL,
#   `request_count` bigint(20) unsigned NOT NULL DEFAULT '0',
#   `invalid_count` bigint(20) unsigned NOT NULL DEFAULT '0',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `unique_customer_time` (`customer_id`,`time`),
#   KEY `customer_idx` (`customer_id`),
#   CONSTRAINT `hourly_stats_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
# );
    
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
