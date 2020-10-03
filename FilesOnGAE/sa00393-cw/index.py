# Description: Has all handlers for the web apcliation deployed on Google App Engine
import os
import webapp2
import jinja2
from runec2instance import getSignedUrl
import base64,urllib2
from google.appengine.ext import db
import boto

#Model for Plagiarism details
class Plagiarism(db.Model):
	username = db.StringProperty()
	instances = db.IntegerProperty()
	windowsize = db.IntegerProperty()
	overlapsize = db.IntegerProperty()
	work = db.IntegerProperty()
	userfile = db.StringProperty()
	matches = db.StringProperty()
	

template_dir = os.path.join(os.path.dirname(__file__), 'templates') 
jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def doRender(handler, tname, values={}):
	temp = os.path.join(os.path.dirname(__file__), 'templates/'+tname) 
	if not os.path.isfile(temp):
		doRender(handler, 'index.htm') 
		return

	# Make a copy of the dictionary and add the path 
	newval = dict(values)
	newval['path'] = handler.request.path
	
	template = jinja_environment.get_template(tname)
	handler.response.out.write(template.render(newval)) 
	return True

class PlagiarismHandler(webapp2.RequestHandler): 
	def get(self):
		doRender(self, 'plagiarism.htm')
		
class workinprogressHandler(webapp2.RequestHandler): 		
	def post(self):
		uname = self.request.get('username')
		i = self.request.get('instances')
		w = self.request.get('windowsize')
		o = self.request.get('overlapsize')
		file = self.request.get('suspiciousfile')
		filename = self.request.POST['suspiciousfile'].filename
		newwork = 0
		newmatches = ''

		if uname == '' or i == '' or w == '' or o == '' or file == '' or filename == '': 
			doRender(
				self,
				'plagiarism.htm',
				{'note': 'Please specify values in all fields!'})		
		else:
			# Create Plagiarism object and show the details to the user
			plagiarismdetails = Plagiarism(username=uname, instances=int(i), windowsize=int(w), overlapsize=int(o), work=int(newwork), userfile=filename, matches=newmatches);
			plagiarismdetails.put();
			
			# Create EC2 instances by calling getSignedUrl method from runec2instance
			data1 = '#!/bin/sh' + '\n'
			data2 = 'sh /home/ubuntu/runthisfile.sh' + '\n'
			data3 = 'python /home/ubuntu/createindex.py'
			data4 = ' ' + w + ' ' + o + ' ' + i
			data = data1 + data2 + data3 + data4
			userdata = base64.b64encode(data)
			# Add your access key and secret key in below lines
			accesskey = 'accesskey'
			secretKey = 'secretkey'
			params = dict(
        		Action='RunInstances', 
        		ImageId='AMI-ID',
        		MaxCount=i, 
        		MinCount='1',
        		KeyName='keyname',
        		SecurityGroup='SSH',
        		UserData=userdata)
			url = getSignedUrl(accesskey, secretKey, params)
			response = urllib2.urlopen(url).read()
			
			#saving index file on S3
			suspiciousdoc = 'suspicion/' + filename
			s3 = boto.connect_s3(accesskey,secretKey)
			bucket = s3.create_bucket('cw.sa00393.com')
			key = bucket.new_key(suspiciousdoc)
			key.set_contents_from_string(file)
			key.set_acl('public-read')
			
			#Render next page to user
			doRender(self,'workinprogress.htm', {'data': uname })
					
#This handler was implemented after submission of report					
class ResultHandler(webapp2.RequestHandler):
	def get(self):
		uname = self.request.get('uname')
		result = db.GqlQuery('SELECT * FROM Plagiarism WHERE username = :1',uname)
		if result:
			for r in result:
				if(r.work == 0):
					doRender(self, 'results.htm', {'note': 'Index being created. Please refresh this page in few minutes to view results'})
				elif(r.work == 1):
					doRender(self, 'results.htm', {'note': 'Matches being found. Please refresh this page in few minutes to view results'})
				elif(r.work == 2):
					if(r.matches != ''):
						matches_list = r.matches.split(",")
						count = len(matches_list)
						chd='&chd=t:'
						chl='&chl='
						chdl='&chdl='
						for i in range(count):
							if(i==0):
								chdl=chdl+matches_list[i]+'|'
							elif(i%2 == 0):
								chdl=chdl+matches_list[i]+'|'
							else:
								chd=chd+matches_list[i]+','
								chl=chl+matches_list[i]+'|'
						matches_to_send = chd[:-1]+chl[:-1]+chdl[:-1]
						doRender(self, 'results.htm', {'result': matches_to_send})
					else:
						doRender(self, 'results.htm', {'note': 'No plagiarism found'})


class anyWorkHandler(webapp2.RequestHandler): 
	def get(self):
		work_arrived = 0
		que = db.Query(Plagiarism)
		que = que.filter('work =',work_arrived)
		result = que.fetch(limit=1)
		
		if len(result) > 0 : 
			doRender(self,'anyWork.htm',{'work' : result} )

class workTakenHandler(webapp2.RequestHandler):
	def get(self):
		uname = self.request.get('user')
		work_taken = self.request.get('work')
		if(work_taken=='1'):
			 result = db.GqlQuery('SELECT * FROM Plagiarism WHERE username = :1',uname)
			 if result:
			 	for r in result:
			 		r.work = int(work_taken)
			 		db.put(r)
		doRender(self,'workTaken.htm',{'work' : work_taken + uname} )
		
class workDoneHandler(webapp2.RequestHandler):
	def get(self):
		uname = self.request.get('user')
		work_done = self.request.get('work')
		matches_sent = self.request.get('matches')
		if(work_done=='2'):
			 result = db.GqlQuery('SELECT * FROM Plagiarism WHERE username = :1',uname)
			 if result:
			 	for r in result:
			 		r.work = int(work_done)
			 		r.matches = matches_sent
			 		db.put(r)
		doRender(self,'workDone.htm',{'work' : work_done + uname + matches_sent} )

			
class MainPage(webapp2.RequestHandler):
	def get(self):
		path = self.request.path 
		doRender(self, path)

app = webapp2.WSGIApplication([
	('/plagiarism', PlagiarismHandler),
	('/workinprogress',workinprogressHandler),
	('/results', ResultHandler),
	('/anyWork', anyWorkHandler),
	('/workTaken',workTakenHandler),
	('/workDone', workDoneHandler),
	('/.*', MainPage)], debug=True)