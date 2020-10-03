# Description: 	This is the main python script which creates source index. It is run from user-data.
# The command to run is passed while launching instances. It calls methods from b,d and e to 
# excute those scripts.

from sourcefiles import createsourcewindows
from sourceindex import createsourceindex
from createsourcefolders import createfolders
import time
import sys
import os

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

windowsize = int(sys.argv[1])
overlapsize = int(sys.argv[2])
division = int(sys.argv[3])

t0 = time.time()

print 'Moving sourcefiles into folders'

createfolders(division)

print 'creating windows of words in sourcefiles'

createsourcewindows(windowsize,overlapsize)

print 'creating index from source files'

createsourceindex()

t1 = time.time() - t0
print 'time taken : ' + str(t1)

print 'terminating instance'

readfile = open('/home/ubuntu/instance.txt','r')
details = readfile.read()
instanceid = details[20:30]

os.system("ec2-terminate-instances " + str(instanceid) + " -K /home/ubuntu/awspk.pem -C /home/ubuntu/awscert.pem")
