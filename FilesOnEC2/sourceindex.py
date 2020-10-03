# Description: For each file created by sourcefiles.py, find hashes of each line and add it to an
# index file with its location
import csv
import hashlib
import glob, os
import boto

def createsourceindex():
	#get instance id from metadata to name the source index csvfile
	readf=open('/home/ubuntu/index.txt','r')
	index=readf.read()
	id = int(index) + 1
	#Read names of files
	source_filenames = glob.glob(os.path.join("/home/ubuntu/pan-plagiarism-collection/source-files/", '*'))

	#initialise an array for dict
	index_dict = {}

	#Create a dictionary with hashes as keys and filenames as values
	for source_file in source_filenames:
		#open file for reading
		readfile = open(source_file, 'r')
		(filepath, filename) = os.path.split(source_file)
		for line in readfile:
			line = line.rstrip()
			line = hashlib.md5(line).hexdigest()
			if line not in index_dict:
				index_dict[line] = filename

			else:
				value = index_dict.get(line)
				delim = ' '
				newvalue = value+delim+filename
				index_dict[line] = newvalue

	#create a new csv file to write the created index dictionary
	csvfilename = '/home/ubuntu/pan-plagiarism-collection/sourceindexfile' + str(id) + '.csv'
	csvfile = open(csvfilename, 'w')
	indexwriter = csv.writer(csvfile, delimiter=',')

	for key in index_dict.iterkeys():
		indexwriter.writerow([key, index_dict[key]])

	csvfile.close()
	#saving index file on S3
	indexfile = 'index/' + 'sourceindexfile' + str(id) + '.csv'
	s3 = boto.connect_s3('accesskey','secretkey')
	bucket = s3.create_bucket('cw.sa00393.com')
	key = bucket.new_key(indexfile)
	key.set_contents_from_filename(csvfilename)
	key.set_acl('public-read')