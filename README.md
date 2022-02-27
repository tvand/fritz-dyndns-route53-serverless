# FRITZ!Box DynDNS Serverless API

If like me you are willing to keep DNS record up to date when your dynamic FritzBox ip change.
You can easily deploy this serverless application and using it.

But it can also be also a great example of Serverless application on AWS.

## Requirements

1. I guess you already have an AWS account if you are willing to update route53
2. IAM user with proper credentials

## Configuration

|Parameter      |Description                                        |Required|Default Value|
|:--------------|:--------------------------------------------------|:-------|:------------|
|HostedZoneId   |Hosted zone ID of your domain                      |yes     |             |
|RsDomains      |List of domain names to update (comma separated)   |yes     |             |
|DynDnsUsername |FritzBox DynDns UserName                           |yes     |             |
|DynDnsPassword |FritzBox DynDns Password                           |yes     |             |
|ApiEndpointConf|API Gateway Endpoint Config (EDGE/REGIONAL/PRIVATE)|no      |REGOINAL     |
|ApiStageName   |Name of API Stage                                  |no      |v1           |

## Deployment

Deploy template.yaml as AWS Cloudformation Stack

## Usage
```
curl -u <username>:<password> https://<api-name>.execute-api.<aws-region>.amazonaws.com/v1/record
```
