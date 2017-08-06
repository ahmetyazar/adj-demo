#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 15:28:00 2017

@author: yazar
"""

import sys
import logging
import rds_config
import pymysql
import datetime
import json
import requests

# rds settings
rds_host = "creditadjudication.cz3lpdttkjpo.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name,
                           connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

json.JSONEncoder.default = datetime_handler


def addBlockedCustomers(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    logger.info('#################')
    logger.info(event)
    logger.info('#################')
    
    message = event['Records'][0]['Sns']['Message']
    logger.info('From SNS: ' + message)
    message = json.loads(message)

    sql = "insert into FulfillmentDb.BlockedCustomers (partyID, effectiveDate) "
    sql += "values ({0}, NOW())".format(message['partyID'])

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)
        conn.commit()
        cur.execute("select * from FulfillmentDb.BlockedCustomers")

        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table".format(item_count))

    conn.commit()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


def checkPotentialFraud(event, context):
    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    # check if there is a fraud
    sql = "select * from FulfillmentDb.PotentialFraud where partyID = {}".format(event['partyID'])    
    
def processCreditLimit(event, context):   
    logger.info('#################')
    logger.info(event)
    logger.info('#################')


    
    

    