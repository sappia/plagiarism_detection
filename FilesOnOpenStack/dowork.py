# Description: Main file which fetches work from GAE and calls required methods to compute matches
import urllib2
import glob, os
from fetchS3files import getfilesfromS3
from matches_openstack import computematches
from suspiciousindex import createsuspiciousindex

#check for work on GAE
u = 'http://sa00393-cw.appspot.com/anyWork'
webpage = urllib2.urlopen(u)
work = webpage.read()
webpage.close()
print 'work fetched'

if(work != ''):
	work = work.lstrip('\n')
	worklist = work.split()
	print worklist
	user = worklist[0]
	expected_files = int(worklist[1])
	windowsize = int(worklist[2])
	overlapsize = int(worklist[3])
	work_flag = worklist[4]
	suspiciousfile = worklist[5]
	if(work_flag == '0'):
		print 'fetching files from S3'
		#fetch required files from S3
		getfilesfromS3()
		print 'files fetched from S3'
		#check if the required number of files are fetched
		filenames = glob.glob(os.path.join("/home/ubuntu/index/", '*'))
		no_of_files = len(filenames)
		if(no_of_files == expected_files):
			#set workTaken flag on GAE Datastore
			u1 = 'http://sa00393-cw.appspot.com/workTaken?user='+str(user)+'&work=1'
			webpage1 = urllib2.urlopen(u1)
			response = webpage1.read()
			webpage1.close()
			print 'work taken.now creating suspicious index'
			createsuspiciousindex(windowsize,overlapsize)
			print 'index created. now computing matches'
			#compute matches and update on GAE datastore
			matches = computematches()
			#Push results to GAE Datastore
			print 'pushing results to datastore'
			u2 = 'http://sa00393-cw.appspot.com/workDone?user='+str(user)+'&work=2'+'&matches='+str(matches)
			webpage2 = urllib2.urlopen(u2)
			response2 = webpage2.read()
			webpage2.close()
			print 'work done'