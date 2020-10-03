# Description: This file creates an index of the suspicious file to match it with source indexes
import string, re
import glob, os
import csv
import hashlib
import time

def createsuspiciousindex(windowsize,overlapsize):
	t0 = time.time()
	#Read names of files
	file = glob.glob(os.path.join("/home/ubuntu/suspicion/", '*'))
	
	for suspicious_file in file:
		#open file for reading
		readfile = open(suspicious_file, 'r')
		#read all lines from the file
		inputtext = ''.join(readfile.readlines())
		#convert to lowercase
		lowercase_text = inputtext.lower()
		#remove punctuations
		nopunctuation_text = re.sub('[%s]' % re.escape(string.punctuation), '', lowercase_text)
		#split all the text into words
		words = nopunctuation_text.split()
		#Get source document filename
		(filepath, filename) = os.path.split(suspicious_file)
		#create a new file with source document filename in different folder
		writefile = open('/home/ubuntu/pan-plagiarism-collection/suspicious-files/'+filename, 'w')
		
		#initialise windowsize,overlapsize,s and w(variables used in the loop) 
		s=0
		w=windowsize
		
		#create 8 words window and add them on new lines in a file 
		while True:
			sentence = words[s]
			for i in range(s+1,w):
				sentence = sentence + ' ' + words[i]
			writefile.write(sentence)
			writefile.write('\n')
		
			s=s+(windowsize-overlapsize)
			if ((w+(windowsize-overlapsize))<len(words)):
				w=w+(windowsize-overlapsize)
			else:
				sentence = words[s]
				for j in range(s+1,len(words)):
					sentence = sentence + ' ' + words[j]
				writefile.write(sentence)
				break
		
		writefile.close()
	
	#Read names of files
	h_filename = glob.glob(os.path.join("/home/ubuntu/pan-plagiarism-collection/suspicious-files/", '*'))
	
	#initialise an array for dict
	index_dict = {}
	
	print 'creating dictionary'
	
	#Create a dictionary with hashes as keys and filenames as values
	for h_file in h_filename:
		#open file for reading
		h_readfile = open(h_file, 'r')
		(filepath, filename) = os.path.split(h_file)
	
		for line in h_readfile:
			line = line.rstrip()
			line = hashlib.md5(line).hexdigest()
			if line not in index_dict:
				index_dict[line] = ''
	
	print 'dictionary created'
	
	#create a new csv file to write the created index dictionary
	csvfile = open('/home/ubuntu/pan-plagiarism-collection/suspiciousindexfile.csv', 'w')
	indexwriter = csv.writer(csvfile)
	
	print 'writing csv file'
	for key in index_dict.iterkeys():
		indexwriter.writerow([key])
		
	csvfile.close()
	
	t1 = time.time() - t0
	print 'time taken : ' + str(t1)
		