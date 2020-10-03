# Description: This script divides source documents into different folders based on no. of instances
import string, re
import glob, os
import time

def createfolders(division):
	t0 = time.time()
	#Read names of files
	source_filenames = glob.glob(os.path.join("/home/ubuntu/pan-plagiarism-collection/source-documents/", '*'))
	num_of_files = len(source_filenames)
	
	#Calculate number of files in each division
	if (num_of_files%division) == 0:
		each = num_of_files/division
		rem = 0
		print 'each : ' + str(each) + ' rem : ' + str(rem)
	else:
		each = num_of_files/division
		rem = num_of_files%division
		print 'each : ' + str(each) + ' rem : ' + str(rem)
	
	#intialise required counters for loop
	c = 0
	#if files are not equally divisible first folder will have "rem" files more
	files = rem
	
	#Loop to create new folder and move files into them
	for i in range(division):
		print i
		os.system("mkdir /home/ubuntu/pan-plagiarism-collection/source-docs" + str(i+1))

		files = files + each

		source_files = glob.glob(os.path.join("/home/ubuntu/pan-plagiarism-collection/source-documents/", '*'))

		for source_file in source_files:
			if(c==files):
				break
			
			else:
				command = "mv " + source_file + " /home/ubuntu/pan-plagiarism-collection/source-docs" + str(i+1) + "/"
				os.system(command)
				c = c+1

	
	print num_of_files
	
	t1 = time.time() - t0
	print 'time taken : ' + str(t1)