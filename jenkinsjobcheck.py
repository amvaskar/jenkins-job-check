#   execute program with follow command line
##   	python job.py -j <jobname> -i <ip_address> -port 8080 -username <user_name> -password <passwd>



import os, sys, json, codecs, urllib2 ,base64,time
import subprocess
import argparse
import requests
import json
import jenkinsapi
from getpass import getpass
from jenkinsapi.jenkins import Jenkins

'''
totalBuildCount = 0

for job in J.keys():
    builds = J[job].get_build_dict()
    print job + " build count: " + str(len(builds))
    totalBuildCount += len(builds)

print "Total build count: " + str(totalBuildCount)
'''

list_job_success = []
list_job_failure = []
list_job_abort = []
list_job_others = []


def job(jobname, port, ip, build_number, username, password):
	try:
		user_name= username
		passwd= password        
		job_name= jobname
		request = urllib2.Request("http://%s:%s/jenkins/job/%s/lastBuild/api/json?pretty=true" % (ip,port,job_name))
		#print (request)
		
		
		base64string = base64.encodestring('%s:%s' % (user_name, passwd)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)   
		result = urllib2.urlopen(request)
		json_result = result.read()

		lastBuild_number = json.loads(json_result)['number']
		lastBuild_number +=1
		#print "last build number =",lastBuild_number-1

	except:
		print "\ncheck your command-line options, arguments and sub-commands -h -help for information\n"

	try:
		if build_number >= lastBuild_number or build_number == 0:
			print "Number to check History, number should be less than jenkin job last build number or zero."

	except:
		pass
	for i in range(lastBuild_number-build_number,lastBuild_number):
		#print i

		firstpart = "http://%s:%s/jenkins/job/" %(ip, port)
		job_number = str(i)
		secondpart = "/api/json?pretty=true"
		final_url = (firstpart + '%s' + "/" + job_number + secondpart) %(job_name)
		print final_url
		request = urllib2.Request(final_url)
		base64string = base64.encodestring('%s:%s' % (user_name, passwd)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)   
		result = urllib2.urlopen(request)
		json_result_2 = result.read()
		#print(result.read())
		job_response_parser(json_result_2)

	print ('\nThe Final Job Status :\n')
	
	print 'Success = ', len(list_job_success)
	print 'Failure = ', len(list_job_failure)
	print 'Aborted = ', len(list_job_abort)
	print 'Others = ', len(list_job_others)
	
	
def job_response_parser(json_result):

	#print json_result
	jobStatus= json.loads(json_result)
	#print jobStatus

	result_value = jobStatus['result']
	#print result_value

	if result_value == 'SUCCESS':
		list_job_success.append(result_value)

	elif result_value == 'FAILURE':
		list_job_failure.append(result_value)

	elif result_value == 'ABORTED':
		list_job_abort.append(result_value)

	elif result_value != 'SUCCESS' and result_value != 'FAILURE' and result_value != 'ABORTED':
		list_job_others.append(result_value)

	else: 
		print ("Error on json file from jenkins!!")


if __name__ == '__main__':


	try:
		parser = argparse.ArgumentParser(
		description='Passing variables to the program for jenkins Job Status',
		formatter_class=argparse.RawDescriptionHelpFormatter)
		parser._action_groups.pop()
		required = parser.add_argument_group('Required arguments')
		optional = parser.add_argument_group('Optional arguments')

		required.add_argument('-j', '--job', type=str, nargs='+',
						help='job name to check for the job status')

		required.add_argument('-i', '--ip', type=str,
						help='use ip address and port number for jenkins')

		required.add_argument('-username', type=str,
						help='username for jenkins')

		required.add_argument('-password', type=str,
						help='password or token for jenkins')

		optional.add_argument('-history', type=int,
						help='This will print lasted jenkins job status', default='1')

		optional.add_argument('-port', type=str,
						 help='port number for jenkins', default='8080')

		args = parser.parse_args()


		if args.job and args.port and args.ip and args.history and args.username and args.password:

			jobname = args.job[0]
			port =  args.port
			ip = args.ip
			build_number = args.history
			username = args.username
			password = args.password


			job(jobname,port,ip,build_number, username, password)

		else:
			print "Use all arguments. use -h, -help for information."
	except:
		pass

		print "Either one of : \n -username -password -jobname -ip_address -port for jenkins not found"



	







