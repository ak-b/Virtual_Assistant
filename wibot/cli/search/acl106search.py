import click
import requests
import json
import os
import re
import string

@click.group(help='Search IP blocks at Edge PE/CRT')
def acl106():
        pass

@acl106.command(help = 'Search IP blocks at Edge PE/CRT')
@click.argument('dstip')
@click.argument('port')
def acl106(dstip,port):
	print("Please wait .. Awesom-o is querying the Configuration DB for all Edge devices")
	print("...")
	search_url='http://10.241.90.66/acl106query/search?srcip=0.0.0.0/0&dstip={}&dstport={}'.format(dstip,port) 
	response= requests.get(search_url)
	#print("Request Response Code")
	#print(response.status_code)
	result = response.content 
	parsed = json.loads(result)
	#print(parsed)
	block_list = []
	allow_list = []
	for entry in parsed:
		for key,value in entry.items():
			
			if  key == 'srcip' and re.search('any',value) and key == 'dstip' and re.search('any',value):
				pass
			elif  key == 'rawrule' and re.search('deny',value):
				block_list.append(value)
			elif key == 'rawrule' and re.search('permit',value) and not re.search('bgp',value) and not re.search('gre',value) and not re.search('ahp',value) and not re.search('esp',value) :
				allow_list.append(value)
			else:
				pass

	if block_list and allow_list:
		print("Edge/ACL106 Blocks")
		print("******************")
		block = [ print(letter) for letter in block_list ]
		print("\n")
		print("Edge/ACL106 Permits")
		print("*******************")
		allow = [ print(letter) for letter in allow_list ]
		

	elif block_list:
		print("Edge/ACL106 Blocks")
		print("******************")
		block = [ print(letter) for letter in block_list ]	
	elif allow_list:
		print("Edge/ACL106 Permits")
		print("*******************")
		allow = [ print(letter) for letter in block_list ]
		

	else:
		print("No Permit/Blocks found for the input IP/Subnet")
		print("Please file a SNOW ticket at https://ciscowebex.servicenowservices.com/nav_to.do?uri=%2Fcom.glideapp.servicecatalog_category_view.do%3Fv%3D1%26sysparm_parent%3De4f58830dba9d890b5cef9551d9619c8%26sysparm_ck%3Daa829a3b1b2fa8106deba82eac4bcbb2f7c8639e49afd6e02918e387e53baf0f954fb375%26sysparm_catalog%3De0d08b13c3330100c8b837659bba8fb4%26sysparm_catalog_view%3Dcatalog_Service_Catalog%26sysparm_cartless%3Dtrue")
		print("We thankyou for your patience, your request will be assigned and serviced via WCI interface")


