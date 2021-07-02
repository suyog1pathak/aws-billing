import boto3
from .poster import poster

class AWSConnection:

  def __init__(self):
    self.connection = {}

  def initConnection(self, resource, region):
    if resource not in self.connection:
        try:
            self.connection[resource] = boto3.client(resource, region_name=region)
        except Exception as e:
            poster.error("Something went wrong while creating connection with {}".format(resource))
            poster.error(e)

  def getConnection(self, resource):
    poster.debug("Returning connection for {}".format(resource))
    return self.connection[resource]
