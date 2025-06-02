# FRITZ!Box DynDNS Serverless API

If like me you are willing to keep a DNS record up to date when your dynamic FritzBox ip changes.
You can easily deploy this serverless application and use it.

## Requirements

1. I guess you already have an AWS account if you are willing to update route53
2. IAM user with proper credentials

## Configuration

|Parameter      |Description                                        |Required|Default Value|
|:--------------|:--------------------------------------------------|:-------|:------------|
|HostedZoneId   |Hosted zone ID of your domain                      |yes     |             |
|RsDomains      |List of domain names to update (comma separated)   |yes     |             |
|DynDnsFqdn     |Custom API domain name (same zone as RsDomains)    |yes     |             |
|DynDnsUsername |FritzBox DynDns UserName                           |yes     |             |
|DynDnsPassword |FritzBox DynDns Password                           |yes     |             |
|ApiEndpointConf|API Gateway Endpoint Config (EDGE/REGIONAL/PRIVATE)|no      |REGIONAL     |
|ApiStageName   |Name of API Stage                                  |no      |v1           |

## Deployment

Deploy template.yaml as AWS Cloudformation Stack

## Usage
* IP-V4
```
curl -u <username>:<password> https://<api-name>.execute-api.<aws-region>.amazonaws.com/v1/record
```
* IP-V6
```
curl -u <username>:<password> https://custom.domain.org/record?ipv6=<ip6addr>
```
