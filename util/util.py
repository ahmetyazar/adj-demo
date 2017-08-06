#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:48:37 2017

@author: yazar
"""

import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def publishBlockedCustomers(event, context):
    client = boto3.client('sns')
    
    logger.info('#################')
    logger.info(event)
    logger.info('#################')
    
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:635746843624:blockedCustomers',    
        Message='{ "partyID" : 11 }'
    )
    print("Response: {}".format(response))