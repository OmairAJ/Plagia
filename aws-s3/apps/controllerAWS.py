#!/usr/bin/env python
## controllerAWS.py

import os
import sys
import time
import string
import MySQLdb
import argparse

import boto
# import boto.s3
import boto.emr
from boto.emr.bootstrap_action import BootstrapAction
from boto.emr.instance_group import InstanceGroup
# from boto.emr.connection import EmrConnection
from boto.emr.step import StreamingStep

## Command-line arguments parser
parser = argparse.ArgumentParser(description='Job controller on AWS for contextual n-grams based plagiarism detection.')
parser.add_argument('-v', action='version', version='%(prog)s 1.0')
parserResults = parser.parse_args()

def main_loop():

	print '\nController starting!\n'

	## Initialise
	jIdentifier  =  None
	jDocument    =  None
	jPath        =  None
	jWindow      =  0
	jOverlap     =  0
	jPattern     =  0
	jStatus      =  None

	JobsLimit    =  2
	jobsWaiting  =  []
	jobsCurrent  =  []
	jobsRunning  = []


	# Establish connections to services
	connEMR = boto.emr.connect_to_region('eu-west-1')
	# connEMR = EmrConnection()

	# connS3 = boto.connect_s3(calling_format = boto.s3.connection.OrdinaryCallingFormat())
	# bucket = connS3.get_bucket('plagiabucket')

	## http://ceph.com/docs/master/radosgw/s3/python/
	# Listing Owned Buckets
	# for bucket in conn.get_all_buckets():
	# 	print "{name}\t{created}".format(
	# 		name = bucket.name, 
	# 		created = bucket.creation_date
	# 		)

	#Listing a bucket's content
	# for key in bucket.list():
	# 	print "{name}\t{size}\t{modified}".format(
	# 		name = key.name,
	# 		size = key.size,
	# 		modified = key.last_modified
	# 		)

	#Creating an Object
	# key = bucket.new_key('hello.txt')
	# key.set_contents_from_string('Hello World!')

	#Generate Object Download URLs (signed and unsigned)
	# hello_key = bucket.get_key('hello.txt')
	# hello_url = hello_key.generate_url(0, query_auth=False, force_http=True)
	# print hello_url

	while True:
		## Connect to Google CloudSQL
		try:
			db = MySQLdb.connect(host='173.194.248.247', port=3306, db='plagiaDB', user='plagiaAdminDb', passwd='fty5687gjh8T776HFf87UG78567jg7sq')
		except Exception as e:
			sys.exit('Unable to connect to the database.')

		cursor = db.cursor() 
		 
		# Retrive data for emr
		cursor.execute('SELECT * FROM jobs WHERE jSetup="ee" OR jSetup="eo" OR jSetup="oe" OR jStatus!="Completed" OR jStatus!="Terminated"')
		result = cursor.fetchall()

		if result:
			for att in result:
				jID          =  int(att[0])
				jIdentifier  =  att[1]
				jPath        =  att[2]
				jDocument    =  att[3]
				jResult      =  att[4]
				jSetup       =  att[5]
				jWindow      =  int(att[6])
				jOverlap     =  int(att[7])
				jPattern     =  int(att[8])
				jStatus      =  att[9]
				jTimestamp   =  att[10]

				jobs = [jID, jIdentifier, jPath, jDocument, jResult, jSetup, jWindow, jOverlap, jPattern, jStatus, jTimestamp]
				# print jobs

				if jStatus == 'Starting':
					step = StreamingStep(
						name=jIdentifier + '_Indexing',
						mapper='sn://plagiabucket/apps/indexMap.py -j ' + jIdentifier,
						reducer='sn://plagiabucket/apps/indexReduce.py',
						input='sn://plagiabucket/' + jPath,
						output='sn://plagiabucket/output/indexes')
						
					# step_args = list()
					# step_args.append('-files')
					# step_args.append('s3://plagiabucket/apps/indexMap.py -j' + jIdentifier + ',s3://plagiabucket/apps/indexReduce.py')

					# steps = []

					# steps.append(StreamingStep(
					# 	name=jIdentifier + '_Indexing',
					# 	mapper='s3://plagiabucket/apps/indexMap.py -j ' + jIdentifier,
					# 	reducer='s3://plagiabucket/apps/indexReduce.py',
					# 	input='s3://plagiabucket/' + jPath,
					# 	output='s3://plagiabucket/output/indexes',
					# 	step_args=step_args)

					# instance_groups = []

					# instance_groups.append(InstanceGroup(
					# 	num_instances='1',
					# 	role='MASTER',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND',
					# 	name='Main node'))

					# instance_groups.append(InstanceGroup(
					# 	num_instances='2',
					# 	role='CORE',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND',
					# 	name='Worker nodes'))
					
					# instance_groups.append(InstanceGroup(
					# 	num_instances='0',
					# 	role='TASK',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND',
					# 	name='Task nodes'))

					# cluster_id = connEMR.run_jobflow(
					# 	name=jDocument + '_Indexing',
					# 	master_instance_type='m3.xlarge',
					# 	slave_instance_type='m3.xlarge',
					# 	num_instances=3,
					# 	action_on_failure='TERMINATE_JOB_FLOW',
					# 	keep_alive=True,
					# 	log_uri='s3://plagiabucket/logs/',
					# 	ami_version='3.7.0',
					# 	steps=[steps],
					# 	ec2_keyname='eu-west-ire',
					# 	visible_to_all_users=True
					# )

					bootStrap = BootstrapAction('Bootstrap', 's3://plagiabucket/apps/bootup.sh', [])

					cluster_id = connEMR.run_jobflow(
						name=jIdentifier + '_Indexing',
						# instance_groups=[instance_groups],
						master_instance_type='m3.xlarge',
						slave_instance_type='m3.xlarge',
						num_instances=3,
						action_on_failure='TERMINATE_JOB_FLOW',
						keep_alive=True,
						enable_debugging=False,
						log_uri='s3://plagiabucket/logs/',
						hadoop_version=None,
						ami_version='3.7.0',
						steps=[step],
						bootstrap_actions=[bootStrap],
						ec2_keyname='eu-west-ire',
						visible_to_all_users=True,
						job_flow_role='EMR_EC2_DefaultRole',
						service_role='EMR_DefaultRole')

					# cluster_id = client.run_job_flow(
					# 	Name=jIdentifier + '_Indexing', 
					# 	LogUri='s3://plagiabucket/logs/', 
					# 	AmiVersion='latest', 
					# 	Instances={}, 
					# 	Steps=[], 
					# 	VisibleToAllUsers=True)

					# cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Waiting', jIdentifier))
					# db.commit()
					print 'Starting cluster: ', cluster_id
					# sys.exit(0)

				elif jStatus == 'Indexed' and jIdentifier[:6]!='source':
					# step = StreamingStep(name=jIdentifier + '_Matching',
					# 	mapper='s3n://plagiabucket/apps/matchMap.py -j ' + jIdentifier,
					# 	reducer='s3n://plagiabucket/apps/matchReduce.py',
					# 	input='s3n://plagiabucket/outputs/indexes',
					# 	output='s3n://plagiabucket/output/matches')

					# instance_groups = []

					# instance_groups.append(InstanceGroup(
					# 	num_instances=1,
					# 	role='MASTER',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND',
					# 	name='Main node'))
					# instance_groups.append(InstanceGroup(
					# 	num_instances=2,
					# 	role='CORE',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND',
					# 	name='Worker nodes'))
					# instance_groups.append(InstanceGroup(
					# 	num_instances=0,
					# 	role='TASK',
					# 	type='m3.xlarge',
					# 	market='ON_DEMAND', 
					# 	name='Task nodes'))

					# cluster_id = connEMR.run_jobflow(
					# 	jIdentifier + '_Matching',
					# 	instance_groups=[],
					# 	action_on_failure='TERMINATE_JOB_FLOW',
					# 	keep_alive=True,
					# 	enable_debugging=False,
					# 	log_uri='s3://plagiabucket/logs/',
					# 	hadoop_version=None,
					# 	ami_version='3.7.0',
					# 	steps=[step],
					# 	bootstrap_actions=[],
					# 	ec2_keyname='eu-west-ire',
					# 	visible_to_all_users=True,
					# 	job_flow_role='EMR_EC2_DefaultRole',
					# 	service_role='EMR_DefaultRole')
					
					print 'Starting cluster: ', cluster_id

				# elif jIdentifier[:6]!='source':
				# 	cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Completed', jIdentifier))
				# 	db.commit()

		## 

		print '\nController is running...\n'
		time.sleep(10)


if __name__ == '__main__':
	try:
		main_loop()
	except KeyboardInterrupt:
		print >> sys.stderr, '\nController stopping!\n'
		sys.exit(0)


