'use strict';
// import { Route53Client, ChangeResourceRecordSetsCommand } from "@aws-sdk/client-route-53"; // ES Modules import
const { Route53Client, ChangeResourceRecordSetsCommand } = require("@aws-sdk/client-route-53"); // CommonJS import
const client = new Route53Client({apiVersion: '2013-04-01'});
const { hostedZoneId, rsDomains, username, password } = process.env;

/**
 * Format API Gateway response
 * @param {number} statusCode
 * @param {object} body
 */
const createResponse = (statusCode, body) => {
  return {
    statusCode: statusCode,
    headers: {
      "Access-Control-Allow-Origin" : "*"
    },
    body: body ? JSON.stringify(body) : null
  };
};

const updateRecord = (ip, type, comment, callback) => {
  const params = {
    ChangeBatch: {
      Changes: rsDomains.split(',').map((domain => {
        return {
          Action: "UPSERT",
          ResourceRecordSet: {
            Name: domain,
            ResourceRecords: [{
              Value: ip
            }],
            TTL: 60,
            Type: type
          }
        }
      })),
      Comment: comment
    },
    HostedZoneId: hostedZoneId
  };
  
  const command = new ChangeResourceRecordSetsCommand(params);
  client.send(command, (err, data) => {
    callback(err, data && data.hasOwnProperty('ChangeInfo') ? data.ChangeInfo.Status : 'FAIL');
  });
};

const checkBasicAuth = (headers) => {
  if (!headers.hasOwnProperty('Authorization')) {
    return false;
  }
  const basic = Buffer.from(headers.Authorization.split(' ')[1], 'base64').toString();
  const reqCredentials = basic.split(':');

  return !(reqCredentials[0] !== username || reqCredentials[1] !== password);
};

exports.handler = (event, context, callback) => {
  if (false === checkBasicAuth(event.headers)) {
    callback(null, createResponse(403, {"error": "Not authorized"}));
  }
  if (!event.headers.hasOwnProperty('X-Forwarded-For')) {
    callback(null, createResponse(500, {"error": "missing ip in proxy http headers"}));
  }
  updateRecord(event.headers['X-Forwarded-For'], "A", "FRITZ!Box IPv4 record", (err, success) => {
    if (err) {
      console.error(err);
    } else {
      console.log("IPV4 " + event.headers['X-Forwarded-For'] + ": " + success);
    }
  });
  if (event.queryStringParameters !== null && event.queryStringParameters.hasOwnProperty('ipv6')) {
    updateRecord(event.queryStringParameters['ipv6'], "AAAA", "FRITZ!Box IPv6 record", (err, success) => {
      if (err) {
        console.error(err);
      } else {
        console.log("IPV6 " + event.queryStringParameters['ipv6'] + ": " + success);
      }
    });
  }
  callback(null, createResponse(200, {"status": "OK"}));
};
