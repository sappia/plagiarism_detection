# Description: This file has code to start required EC2 instances
# Resource used: http://www.tikirobot.net/wp/2010/01/24/signing-amazon-web-services-api-requests-in-python/
import base64, hashlib, hmac, time, urllib, urllib2
        
# Sign an AWS REST request using the method described in
# http://docs.aws.amazon.com/general/latest/gr/signature-version-2.html
#_______________________________________________________________________________
def getSignedUrl(accessKey, secretKey, params):
 
    #Step 0: add accessKey, Service, Timestamp, and Version to params
    params['AWSAccessKeyId'] = accessKey
    
    #Amazon adds hundredths of a second to the timestamp (always .000), so we do too.
    #(see http://associates-amazon.s3.amazonaws.com/signed-requests/helper/index.html)
    params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    params['Version'] = '2013-02-01'
    params['SignatureMethod'] = 'HmacSHA256'
    params['SignatureVersion'] = '2'
 	
    #Step 1a: sort params
    paramsList = params.items()
    paramsList.sort()
 
    #Step 1b-d: create canonicalizedQueryString
    # This code comes from http://blog.umlungu.co.uk/blog/2009/jul/12/pyaws-adding-request-authentication/
    # and the resulting discussion
    canonicalizedQueryString = '&'.join(['%s=%s' % (k,urllib.quote(str(v))) for (k,v) in paramsList if v])
 
    #Step 2: create string to sign
    host          = 'ec2.us-east-1.amazonaws.com'
    requestUri    = '/'
    stringToSign  = 'GET\n'
    stringToSign += host +'\n'
    stringToSign += requestUri+'\n'
    stringToSign += canonicalizedQueryString.encode('utf-8')
 
    #Step 3: create HMAC
    digest = hmac.new(secretKey, stringToSign, hashlib.sha256).digest()
 
    #Step 4: base64 the hmac
    sig = base64.b64encode(digest)
 
    #Step 5: append signature to query
    url  = 'https://' + host + requestUri + '?'
    url += canonicalizedQueryString + "&Signature=" + urllib.quote(sig)
 
    return url