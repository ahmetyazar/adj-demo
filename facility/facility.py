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


def createFacility(event, context):
    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    partyID = event['partyID']
    scoreType = 'Credit'  # check credit score for eligibility
    minCreditScore = 500

    # check if the party's credit score is above the threshold
    # assuming only one response
    scoreEndPoint = 'https://7i33pxvp51.execute-api.us-east-1.amazonaws.com/dev/party/{0}/score?scoreType={1}'
    response = requests.get(scoreEndPoint.format(partyID, scoreType))
    response = response.json()

    response = json.loads(response)
    score = response[0]['score']
    if score < minCreditScore:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': {'Message': 'Insufficient credit score',
                     'PartyID': partyID,
                     'Score': score
                     }
        }

    # Credit score is above the threshold
    # Let's create the facility
    sql = "insert into FacilityDb.Facility (facilityType, status, startDate)"
    sql += " values ('{0}', 1, '{1}')".format(event['facilityType'], event['startDate'])

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)

        # insert a record into FacilityParty table
        sql = "insert into FacilityDb.FacilityParty (facilityID, partyID, relationshipType, effectiveDate, expiryDate) values (LAST_INSERT_ID(),{0},'{1}','{2}',NULL)"
        sql = sql.format(partyID, event['relationshipType'], event['startDate'])
        logger.info(sql)
        cur.execute(sql)

        conn.commit()
        cur.execute("select * from FacilityDb.Facility")

        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table".format(item_count))

        cur.execute("select * from FacilityDb.FacilityParty")

        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table".format(item_count))
    
    conn.commit()

    """
    Sample JSON to post to the API
    {"facilityType" : "Line", 
     "startDate" : "2017-07-17 22:52:21",
     "partyID" : 1,
     "relationshipType" : "Owner"
    }
    """

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }
    

def getFacility(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    sql = 'select * from FacilityDb.FacilityParty'

    if ('query' in event):
        if ('partyID' in event['query']) & ('facilityID' in event['query']):
            sql += " where partyID={0} and facilityID={1}".format(event['query']['partyID'], event['query']['facilityID'])
        elif ('partyID' in event['query']):
            sql += " where partyID="+event['query']['partyID']
        elif ('facilityID' in event['query']):
            sql += " where facilityID="+event['query']['facilityID']

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)

    data = cur.fetchall()
    conn.commit()
    return json.dumps(data, default=datetime_handler)
    

def updateCreditLimit(event, context):
    """
    This function updates credit limit.
    """

    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    with conn.cursor() as cur:
        expiryDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # expiry the old limit
        sql = "update FacilityDb.Measure set expiryDate='{0}' where facilityID={1} and measureName='CreditLimit'".format(expiryDateTime, event['facilityID'])
        logger.info(sql)
        cur.execute(sql)

        # insert the new limit
        sql = 'insert into FacilityDb.Measure (measureName, measureType, facilityID, ' + \
              'value, effectiveDate, expiryDate) values (' + \
              "'CreditLimit','Limit',{0}, {1}, '{2}', NULL)".format(event['facilityID'], event['newCreditLimit'], expiryDateTime)

        logger.info(sql)
        cur.execute(sql)

        conn.commit()
        cur.execute("select * from FacilityDb.Measure where facilityID = {0}"
                    .format(event['facilityID']))

        for row in cur:
            logger.info(row)

    """
    Sample JSON to post to the API
    {"facilityID" : 1, 
     "newCreditLimit" : 40000
    }
    """
    conn.commit()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }
    
    

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
    
    sql = "insert into FacilityDb.BlockedCustomers (partyID, effectiveDate) "
    sql += "values ({0}, NOW())".format(message['partyID'])

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)
        conn.commit()
        cur.execute("select * from FacilityDb.BlockedCustomers")

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

    

    