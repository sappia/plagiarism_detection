# Description: This file fetches source index and suspicious files from S3 bucket to work on
import boto

def getfilesfromS3():
	s3 = boto.connect_s3('accesskey','secretkey')
	
	mybucket = s3.get_bucket('cw.sa00393.com')
	
	for key in mybucket.list():
		res = key.get_contents_to_filename(key.name)