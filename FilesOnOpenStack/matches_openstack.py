# Description: This file computes the matches between source index and suspicious index
import csv
import glob, os
import time
import urllib2

def computematches():
	t0 = time.time()
	#initialise final matches dict
	final_matches = {}
	#read all source index filenames
	csvfilenames = glob.glob(os.path.join("/home/ubuntu/index/", '*'))
	for csvfile in csvfilenames:
		#read source index file and create a dictionary
		csvfile1 = open(csvfile, 'r')
		indexreader1 = csv.reader(csvfile1, delimiter=',')
		
		#initialise an array for dict
		index_dict = {}
		
		print 'creating dictionary 1'
		for row in indexreader1:
			index_dict[row[0]] = row[1]
			
		csvfile1.close()
		print 'dictionary 1 created and file closed'
		
		#read suspicious index file and create a dictionary
		csvfile2 = open('/home/ubuntu/pan-plagiarism-collection/suspiciousindexfile.csv', 'r')
		indexreader2 = csv.reader(csvfile2)
		
		#initialise an array for dict
		hash_dict = {}
		
		print 'creating dictionary 2'
		
		for row in indexreader2:
			hash_dict[row[0]] = ''
		
		csvfile2.close()	
		print 'dictionary 2 created and file closed'
		
		print 'Comparing dictionaries'
		#Intersection of two dictionaries
		inter = dict.fromkeys([x for x in hash_dict if x in index_dict])
		
		Matches = len(inter)
		print 'Matches : ' + str(Matches)
		
		#Create a dictionary of filenames and number of matches
		matches_dict = {}
		#Read names of files
		filenames = glob.glob(os.path.join("/home/ubuntu/pan-plagiarism-collection/source-documents/", '*'))
		for file in filenames:
			count = 0
			(filepath, filename) = os.path.split(file)
			for key1 in inter.iterkeys():
				if filename in index_dict[key1]:
					count = count + 1
			if count>0:
				matches_dict[filename] = count
		
		print matches_dict
	
		#union of dictionaries
		final_matches = dict(final_matches, **matches_dict)
	
	print final_matches
	
	FinalMatches = ''
	print 'Filenames and matches:'
	for match in final_matches.iterkeys():
		FinalMatches = FinalMatches + str(match) + ',' + str(final_matches[match]) + ','
	
	print FinalMatches
	
	Matches_to_send = FinalMatches[:-1]
	print Matches_to_send
	
	t1 = time.time() - t0
	print 'time taken : ' + str(t1)
	
	return Matches_to_send