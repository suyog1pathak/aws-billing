# AWS daily billing notification lambda <img src="https://symbols.getvecta.com/stencil_9/36_lambda-function.4e903ac0e3.svg" width="30px">
![](https://www.python.org/static/community_logos/python-logo.png)


* This code fetches billing details of account from cost explorer service and sends slack notification using slack webhook.
* Additionally it can also post the same JSON payload on any API gateway where data can be ingested in the data source with data pipelines.

* Can be used either as standalone code or as lambda.

**IAM Permissions required**
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsageWithResources",
                "ce:GetCostAndUsage",
                "ce:ListCostCategoryDefinitions"
            ],
            "Resource": "*"
        }
    ]
}
```

* If deploying as lambda in VPC, VPC basic execution role is required too. 

* For changing log level, please check ```libs/poster.py```

**Vars:**

var          | type |details
------------- |---- |-------------
region|""| it should be ```us-east-1``` 
accountName|""| Name of account (Will be used in notification body creation)
org|""|
parentOrg|""|
billingCenter|""|
apiurl|""| api url for posting json payload.
slackWebhook|""|webhook address of slack.

* Example slack message
```
================================================================================
                    2021-06-30      test-account
================================================================================
Service_name                                     Amount             Unit
-----------------------------------------------  -----------------  -----------
AWS CloudTrail                                   0.003613           USD
AWS Cost Explorer                                0.01               USD
AWS Key Management Service                       0.0333723336       USD
AWS Lambda                                       0.0000125354       USD
AWS Secrets Manager                              0.000005           USD
Amazon API Gateway                               0.00001752         USD
Amazon EC2 Container Registry (ECR)              0.0006626832       USD
EC2 - Other                                      1.4313347361       USD
Amazon Elastic Compute Cloud - Compute           1.6207067788       USD
Amazon Elastic Container Service for Kubernetes  2.4                USD
Amazon Elastic Load Balancing                    0.5400732275       USD
Amazon Relational Database Service               0.4464267747       USD
Amazon Route 53                                  0.0002272          USD
Amazon Simple Notification Service               0.000001           USD
Amazon Simple Queue Service                      0.0000008          USD
Amazon Simple Storage Service                    0.0187483489       USD
AmazonCloudWatch                                 0.0047783316       USD
-----------                                      -----------        -----------
TOTAL                                            6.509980269799999  USD
```