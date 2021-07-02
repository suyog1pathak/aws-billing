#!/usr/bin/env python

import sys, os
from libs.connection import AWSConnection
from libs.operation import operation
from libs.poster import poster

#--------------------------------#
region = ''
currencyUnit = "USD"
accountName = os.environ.get('account_name', 'test-account')
org = os.environ.get('org', 'org1')
parentOrg = os.environ.get('parentorg', 'awesome-company')
billingCenter = os.environ.get('billingcenter', 'awesome-company')
serviceProvider = "aws"
apiurl = os.environ.get('apiurl', 'https://something.something.com')
slackWebhook = os.environ.get('slack_webhook', '')
#--------------------------------#

def start_ex(event = " ", context = " "):

  """ Creating AWS boto3 connection with CostExplorer service from custom class """
  ConnectionAWS = AWSConnection()
  ConnectionAWS.initConnection('ce', region)
  CostExplorerClient = ConnectionAWS.getConnection('ce')

  """ operation is custom class with all defined methods required """
  Operation = operation()

  """ getDates() - Returning start and end dates
          [0] Billing day
          [1] Current day                """
  billingDate = Operation.getDates()

  CostByService = Operation.costByService(CostExplorerClient, region)
  totalCost = Operation.totalCost()

  """ Create body for slack notification """
  messageBody = Operation.createBody(currencyUnit, accountName)

  slackResponse = Operation.slack_notification(messageBody, slackWebhook)
  poster.info(slackResponse)

  ConnectionAWS.initConnection('sts', region)
  sts_connection = ConnectionAWS.getConnection('sts')
  Operation.fetchAccountData(sts_connection,[org, parentOrg, billingCenter])
  """ Creating JsonBody to post on API gateway  """
  jsonBody = Operation.createJsonBody(serviceProvider, accountName)
  return str(Operation.post_api(apiurl, jsonBody))

if __name__ == "__main__":
    start_ex()