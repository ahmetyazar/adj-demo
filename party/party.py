import sys
import logging
import rds_config
import pymysql
import datetime
import json

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

def getAllCustomers(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute("select * from PartyDb.Party where partyType='Customer'")
    
    data = cur.fetchall()
    conn.commit()
    return data


def getAllParties(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    logger.info('#################')
    logger.info(event)
    logger.info('#################')
    
    sql = 'select * from PartyDb.Party'

    if ('query' in event):
      if ('partyType' in event['query']):
        sql += " where partyType='"+event['query']['partyType']+"'"

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)

    data = cur.fetchall()
    conn.commit()
    return data


def createParty(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    columns = ['partyType', 'legalName', 'corporateAddress',
               'branchOfAccount', 'SICCode', 'financingType']
    sql = 'insert into PartyDb.Party (partyType, legalName, '
    sql += 'corporateAddress, branchOfAccount, SICCode, financingType) values ('
    sql += "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(event[columns[0]],
     event[columns[1]], event[columns[2]], event[columns[3]], event[columns[4]],
          event[columns[5]])

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)
        conn.commit()
        cur.execute("select * from PartyDb.Party")

        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table".format(item_count))

    """
    Sample JSON to post to the API
    {"partyType" : "Customer", 
     "legalName" : "Company ABCDEF",
     "corporateAddress" : "6 Shepherd Ave. West, Toronto, ON L5L7K9",
     "branchOfAccount" : "Toronto",
     "SICCode" : "Tech", 
     "financingType" : "Line"
    }
    """
    conn.commit()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


def getParty(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    sql = 'select * from PartyDb.Party'

    if ('params' in event):
        if ('partyID' in event['params']):
            sql += " where partyID="+event['params']['partyID']

    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)

    data = cur.fetchall()
    conn.commit()
    return data


def getPartyScore(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    logger.info('#################')
    logger.info(event)
    logger.info('#################')

    sql = 'select * from PartyDb.Score'

    if ('params' in event):
        if ('partyID' in event['params']):
            sql += " where partyID="+event['params']['partyID']
            if ('query' in event):
              if ('scoreType' in event['query']):
                sql += " and scoreType='"+event['query']['scoreType']+"'"


    logger.info(sql)
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute(sql)
    data = cur.fetchall()
    conn.commit()
    return json.dumps(data, default=datetime_handler)

