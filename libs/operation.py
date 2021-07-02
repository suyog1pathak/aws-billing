from datetime import date
from datetime import timedelta 
import requests as requests
from tabulate import tabulate
import json
from .poster import poster

class operation:

  def __init__(self):
    
    """ costy = list of lits || [service_name, billingCost, unit]
        This list will be returned and passed to the tabulate lib for table creation """
    self.costy = []

    self.hs = {"Content-Type": "application/json"}
    self.accountData = {}

    """ Gathering date inputs """
    today = date.today()
    yesterday = today - timedelta(days = 1)
    self.end = today.strftime('%Y-%m-%d')
    self.start = yesterday.strftime('%Y-%m-%d')
    self.totalBill = " "
      
  def getDates(self):
    """ Returning start and end dates
        [0] Billing day
        [1] Current day                """
    poster.debug("Start and end date considered - {} - {}".format(self.start, self.end))  
    return ([self.start, self.end])

  def costByService(self, connection, region):
    response = connection.get_cost_and_usage(
      TimePeriod={ 
        'Start': self.start, 
        'End': self.end                
        }, 
        Granularity='DAILY', 
        Metrics=[ 'UnblendedCost'],
        GroupBy = [
            {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
            }
        ]
    )  
    for res in response['ResultsByTime']:
      for cost_data in res["Groups"]:
        """ cost_data == {'Keys': ['AWS Key Management Service'], 'Metrics': {'UnblendedCost': {'Amount': '0', 'Unit': 'USD'}}} """
        poster.debug("Cost Data fetched from aws - {}".format(cost_data))

        service_name = cost_data.get("Keys")[0]
        x = cost_data.get("Metrics")
        billingCost = x.get("UnblendedCost").get("Amount")
        unit = x.get("UnblendedCost").get("Unit")
        dummy_list = [service_name, billingCost, unit]

        poster.debug("Dummy List created - {}".format(dummy_list))

        self.costy.append(dummy_list)                
    return (self.costy)
  
  def totalCost(self):
    all_service_cost = [x[1] for x in self.costy]
    # Removing 'u'
    encoded = map(float, all_service_cost)
    addition = sum(list(encoded))
    self.totalBill = addition
    poster.debug("Total Bill - {}".format(self.totalBill))
    return(addition)

  def createBody(self, unit, accountName):
    serviceCostList = self.costy
    footer_1 = ['-----------', '-----------', '-----------']
    footer_2 = ['  TOTAL   ', self.totalBill, unit]
    serviceCostList.append(footer_1)
    serviceCostList.append(footer_2)

    messageHeader = """
================================================================================
                    {}      {}
================================================================================""".format(self.start, accountName)
 
    tableData = tabulate(self.costy, headers=["Service_name", "Amount", "Unit"])

    messageBody = "```" + messageHeader + "\n" + tableData + "```"

    return messageBody


  def slack_notification(self, msg, slack_url):
    D = { 
        "text": msg,
        "icon_url": 'https://blocksedit.com/img/aws-app-icon.png'
        }
    try:    
      response = requests.post(slack_url, data=json.dumps(D), headers=self.hs)
      poster.debug("Response on slack webhook - {}".format(response))
      return response
    except Exception as e:
      poster.error("Got error while posting over slack {}".format(e))
      raise e 

  def fetchAccountData(self, connection, dlist):
    poster.debug("fetching account data")
    self.accountData["account_number"] = connection.get_caller_identity().get('Account')
    self.accountData["organization"] = dlist[0]
    self.accountData["ParentOrg"] = dlist[1]
    self.accountData["BillingCenter"] = dlist[2]
      

  def createJsonBody(self, service_provider, account_name):
    bdetails = []
    
    for detail in self.costy[:-2]:
        dict = {"service_name": detail[0], "cost": detail[1]}
        bdetails.append(dict)

    structure = {
        "service_provider": service_provider,
        "account_id": self.accountData["account_number"],
        "account_name": account_name,
        "billing_date": self.start,
        "organization": self.accountData["organization"],
        "parent_org": self.accountData["ParentOrg"],
        "billing_center": self.accountData["BillingCenter"],
        "billing_details": bdetails
    }
    poster.debug("json body - {}".format(structure))
    return json.dumps(structure, indent=4)

  def post_api(self, url, body):
    poster.debug("Posting json body on api gateway - {}".format(body))
    res = requests.post(url, data = body)
    return res
