# Description: This script creates a text file for each source document with given words of 
# windowsize and overlapsize on new lines
import string, re
import glob, os

def createsourcewindows(windowsize,overlapsize):
	#get instance id from metadata to fetch files to work on
	readf=open('/home/ubuntu/index.txt','r')
	index=readf.read()
	id = int(index) + 1
	path = "/home/ubuntu/pan-plagiarism-collection/source-docs" + str(id)
	#Read names of files
	source_filenames = glob.glob(os.path.join(path, '*'))

	for source_file in source_filenames:
		#open file for reading
		readfile = open(source_file, 'r')
		#read all lines from the file
		inputtext = ''.join(readfile.readlines())
		readfile.close()
		#convert to lowercase
		lowercase_text = inputtext.lower()
		#remove punctuations
		nopunctuation_text = re.sub('[%s]' % re.escape(string.punctuation), '', lowercase_text)
		#split all the text into words
		words = nopunctuation_text.split()
		#Get source document filename
		(filepath, filename) = os.path.split(source_file)
		#create a new file with source document filename in different folder
		writefile = open('/home/ubuntu/pan-plagiarism-collection/source-files/'+filename, 'w')

		#initialise s and w(variables used in the loop)
		s=0
		w=windowsize

		#create words of windowsize and overlapsize and add them on new lines in a file
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