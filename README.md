# A Plagiarism Detection System on Hybrid Cloud

## Overview
This is a model for a plagiarism detection system functionally distributed over a combination of public and private clouds termed as hybrid cloud. The user-interface of the system is developed using Platform as a Service (PaaS) - Google App Engine (GAE). Google Datastore acts as the backend. The logic of plagiarism detection is distributed over a private Infrastructure as a Service (IaaS), OpenStack and a public IaaS, Amazon Elastic Compute Cloud (EC2) with usage of Amazon Simple Storage Service (S3) as intermediate storage. The dataset used for this project is a subset of files from PAN 2011 corpus which provides source and suspicious text documents for plagiarism detection research purposes.

This approach used the infrastructure of Amazon EC2 to produce the source document index and the infrastructure of Openstack to match a suspicious document against the source index produced to detect any text similarity in the suspicious document. Text similarity is matched by checking for words of provided windowsize and overlapsize on new lines. A web interface is developed using Python and jinja2 in Google App Engine to take user input for windowsize, overlapsize and number of instances to do the plagiarism detection.

## Contents
This project consists of 3 folders:
* __FilesOnEC2__ contains the python scripts and bash scripts that went into AWS EC2 AMI
  * __createindex.py__ This is the main script which creates source documents index
  * __createsourcefolders.py__ This script divides source documents into different folders based on no. of instances
  * __runthisfile.sh__ This script gets ami launch index id and instance number from metadata and saves in text files for other python scripts to use
  * __sourcefiles.py__ This script creates a text file for each source document with given words of windowsize and overlapsize on new lines
  * __sourceindex.py__ For each file created by sourcefiles.py, find hashes of each line and add it to an index file with its location
* __FilesOnGAE__ contains the files deployed on GAE to build the web app for the plagiarism detection system
  * __app.yaml__ required to tell version of code, location of index.py, static files and libraries to be used etc.
  * __boto__ library files required to connect to S3
  * __index.py__ Main file which has handlers for all htm pages
  * __runec2instance.py__ This file has code to start required EC2 instances
  * __static__ the css file used to design all pages
  * __templates__ all html pages used in this application
* __FilesOnOpenstack__ contains the python scripts and bash scripts that went into Openstack image
  * __dowork.py__ This is the main script which fetches work from GAE and calls required methods to compute matches
  * __every-300-seconds.sh__ This script runs in background continuously. It runs dowork.py every 300 seconds
  * __fetchS3files.py__ This script fetches source index and suspicious files from S3 bucket to work on
  * __matches_openstack.py__ This script computes the matches between source index and suspicious index
  * __suspiciousindex.py__ This script creates an index of the suspicious file to match it with source indexes

