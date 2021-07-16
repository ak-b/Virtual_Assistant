'''
This python script checks if a given server can communicate on a given TCP port, 
a.k.a it tells if there is an ACL open for the user inputted server and port
'''
import os
import csv
import html2text
import paramiko
from paramiko import SSHClient
import re
import requests 
from requests.auth import HTTPBasicAuth
import socket
import time

NETDB_USERNAME = 'akbansal-mech'
NETDB_PASSWORD = 'marvInaSah1ker'
BOT_USERNAME='akbansal'
BOT_PASSWORD='Pass@123'
ENABLE_PASSWORD ='C1sc0@FW582'

try:
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

except Exception as e1:
	print("main exception " + str(e1))


def isvalidIP(serverIP):
	#CHECK IF USER HAS INPUT A VALID IP ADDRESS
	regex_validIp =r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	regex_validMask = r"\b([1,9]|[12][0-9]|3[0-2])\b"

	#regex_validSub = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/\b([1,9]|[12][0-9]|3[0-2])"
	'''unit tests
	#ip_check = "2.16.152.0/24"
	#ip_check = "10.0.024"
	#ip_check = "3...3"
	#ip_check = "-1.2.3.4"
    #ip_check = "1.1.1.1."
	#ip_check = "192.168.1.256"
	#ip_check = "127.1"
	#ip_check = "165.225.112.2100"
	'''
	match_ip=[]
	match_sub=[]
	if re.search('/',ip):
		match_sub = re.compile(regex_validIp).findall(ip.split('/')[0]) and re.compile(regex_validMask).findall(ip.split('/')[1])
		#print("Checking if Valid Subnet")
		#print(match_sub)
		return True
	else:
		match_ip = re.compile(regex_validIp).findall(ip)
		#print("Checking if Valid IP")
		#print(match_ip)
		return True
	

 

def find_dc_stack(serverIP):
	'''
	This function checks netdb and returns the DC, VRF and stack
	the server is located it
	Input: Server IP
	Output: Tuple (DC,STACK,VRF)
	Netdb: 
	'''
	'''
	netdb_url_diff= 'https://dfw01-netdb.webex.com/netdb/vlans.php?fmt=&so=DCNet'
	netdb_download = requests.get(netdb_url_diff,auth=HTTPBasicAuth(NETDB_USERNAME,NETDB_PASSWORD))
	if netdb_download.status_code == 200:
		
		Extract VRF,DC,STACK information
		Search Results from netdb??
		Return a tuple
	
		#dev_diff_url='https://dfw01-netdb.webex.com/netdb/vlans.php?fmt=&re={}&so=DCNet.format(serverIP)'
		dev_diff_url= 'https://dfw01-netdb.webex.com/netdb/vlans.php?fmt=&so=DCNet'
		dev_diff_download= requests.get(dev_diff_url,auth=HTTPBasicAuth(NETDB_USERNAME,NETDB_PASSWORD))
		if dev_diff_download.status_code == 200:
			content_html = dev_diff_download.text[:]
			content_text = html2text.html2text(content_html)
			print(content_text)
			content = content_text.splitlines()

		'''
	csv_file = csv.reader(open('/Users/akbansal/snow_test/server_port_map.csv', "r"), delimiter=",")
	for row in csv_file:
		if re.search(serverIP,row[3]):
			#print (row)
			return row
			break



def find_port_status(serverIP,port):
	'''
	This function checks if the specified port is
	open for the input server on the firewall
	Input: Server IP, Port Number
	Output: Port Open(True) or Not(False)
	'''
	dc= ''
	stack= ''
	data= find_dc_stack(serverIP) 
	if data:	
		dc = data[0]
		stack = data[-1]
		print(dc)
		print(stack)
	else:
		print("Sorry Port is NOT open,Please place a request on Service Now to open ACL ")

	if stack == 'abc':
		print('Sorry! Please check your input')

	else:
		if stack.lower() == 'wxp':
			CSW = dc.lower()+'00-csw01'+ '.webex.com'
			print("You entered -> Server IP : {} Port Number : {}".format(serverIP,port))
			print("IP Location/DC: {} Stack: Data".format(dc))
			print("Checking if Route Path Exists from Core Switch -> {} ".format(CSW))
		elif stack.lower() == 'wxvc':
			CSW = dc.lower()+'-csw01'+ '.webex.com'
			print("You entered -> Server IP : {} Port Number : {}".format(serverIP,port))
			print("Location/DC: {} Stack: Voice".format(dc))
			print("Checking if Route Path Exists from Core Switch -> {} ".format(CSW))
		else:
			CSW= -1

	if CSW == -1:
		pass
	else:
		try:
			ssh_client.connect(hostname=CSW, username=BOT_USERNAME, password=BOT_PASSWORD,\
				allow_agent=False, look_for_keys=False, timeout=10)
			chan = ssh_client.invoke_shell()		
			temp = chan.recv(1024).decode('ascii')
			time.sleep(2)
			chan.send("telnet {} {}\n".format(serverIP,port))
			time.sleep(2)
			temp = chan.recv(1024).decode('ascii')
			#print(temp)

			msg = temp.splitlines()
			for line in msg:
				if re.search("Unable",line):
					print("Sorry Port is NOT open,Please place a request on Service Now to open ACL")
					return False
				else:
					return True
			if re.search('csw',CSW):
				device = CSW.replace('csw,asa')


		except paramiko.ssh_exception.AuthenticationException:
			print("Authentication Failure on device {}".format(CSW))
		except Exception as e:
			print("exception found,details: " +str(e))


if __name__ == "__main__":
	find_dc_stack('10.253.72.0')



