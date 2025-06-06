import os
import logging
import json
import boto3
import base64

#Set up our Session and Client
session = boto3.session.Session()
client = session.client(
    service_name='route53',
    region_name=os.getenv('AWS_REGION')
)

#Set up logging
logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

def lambda_handler(event, context):
    logger.debug("Event: %s", json.dumps(event))

    headers = event['headers']
    if not checkBasicAuth(headers, os.getenv('username'), os.getenv('password')):
        return createResponse(403, {"error": "Forbidden"})

    if not 'X-Forwarded-For' in headers:
        return createResponse(500, {"error": "Missing IP in proxy http headers"})
    
    domains = os.getenv('rsDomains')
    hostedZoneId = os.getenv('hostedZoneId')

    responseIPV4 = updateRecord(domains, headers['X-Forwarded-For'], "A", "FRITZ!Box IPv4 record", hostedZoneId)
    if responseIPV4.get('ChangeInfo') and responseIPV4['ChangeInfo']['Status'] != 'FAIL':
        logger.info("IPV4 %s: %s", headers['X-Forwarded-For'], responseIPV4['ChangeInfo']['Status'])
        
    if event.get('queryStringParameters') and event['queryStringParameters'].get('ipv6'):
        responseIPV6 = updateRecord(domains, event['queryStringParameters']['ipv6'], "AAAA", "FRITZ!Box IPv6 record", hostedZoneId)
        if responseIPV6.get('ChangeInfo') and responseIPV6['ChangeInfo']['Status'] != 'FAIL':
            logger.info("IPV6 %s: %s", event['queryStringParameters']['ipv6'], responseIPV4['ChangeInfo']['Status'])

    return createResponse(200, {"status": "OK"})

# Format API Gateway response
# @param {number} statusCode
# @param {object} body
def createResponse(statusCode, body):
    if body:
        responseBody = json.dumps(body)
    else:
        responseBody = '{}'
        
    return {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin' : '*',
            'Content-Type' : 'application/json'
        },
        'body': responseBody
    }

def checkBasicAuth(headers, username, password):
  if not 'Authorization' in headers:
    return false
  
  auth = headers['Authorization'].split()[1]
  u,p = base64.b64decode(auth.encode("utf-8")).decode("utf-8").split(':')

  return u == username and p == password

def updateRecord(domains, ip, type, comment, zoneid):
    response = client.change_resource_record_sets(
        ChangeBatch={
            'Changes': list(map(lambda domain:
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain,
                        'ResourceRecords': [
                            {
                                'Value': ip,
                            },
                        ],
                        'TTL': 60,
                        'Type': type,
                    },
                },
                domains.split(','))),
            'Comment': comment,
        },
        HostedZoneId=zoneid,
    )

    return response
