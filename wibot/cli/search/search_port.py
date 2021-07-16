import click
import os
import csv
import paramiko
from paramiko import SSHClient
import re
import requests 
from requests.auth import HTTPBasicAuth
import socket
import time

@click.group()
def server_port():
	pass

@server_port.command(help = 'Check if server can communicate on given port')
@click.argument('serverip')
@click.argument('portno')
def server_port(serverip,portno):
	print("Please wait scanning the network for port status")
	print("You entered -> Server IP : {} Port Number : {}".format(serverip,portno))
	subnet_format = serverip.split('.')
	subnet = subnet_format[0]+'.'+subnet_format[1]+'.'+subnet_format[2]+'.0'
	csv_file = csv.reader(open('/app/files/server_port_map.csv', "r"), delimiter=",")
	for row in csv_file:
		if re.search(subnet,row[3]):
			data = row
			break

	if data:	
		dc = data[0]
		stack = data[-1]
	else:
		print("Sorry Port is NOT open,Please place a request on Service Now to open ACL ")
	if stack == 'abc':
		print('Sorry! Please check your input')

	else:
		if stack.lower() == 'wxp':
			CSW = dc.lower()+'00-csw01'+ '.webex.com'
			print("IP Location/DC: {} Stack: Data".format(dc))
			print("Checking if Route Path Exists from Core Switch -> {} ".format(CSW))
		elif stack.lower() == 'wxvc':
			CSW = dc.lower()+'-csw01'+ '.webex.com'
			print("Location/DC: {} Stack: Voice".format(dc))
			print("Checking if Route Path Exists from Core Switch -> {} ".format(CSW))
		else:
			CSW= -1
	if CSW == -1:
		pass
	else:

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

		try:
			ssh_client.connect(hostname=CSW, username=BOT_USERNAME, password=BOT_PASSWORD,\
				allow_agent=False, look_for_keys=False, timeout=10)
			chan = ssh_client.invoke_shell()		
			temp = chan.recv(1024).decode('ascii')
			time.sleep(1)
			chan.send("telnet {} {}\n".format(serverip,portno))
			time.sleep(2)
			temp = chan.recv(1024).decode('ascii')
			msg = temp.splitlines()
			for line in msg:
				if re.search("Unable",line):
					#print("Sorry Port is NOT open,Please place a request on Service Now to open ACL")
					status = False
				else:
					status = True


		except paramiko.ssh_exception.AuthenticationException:
			print("Authentication Failure on device {}".format(CSW))
		except Exception as e:
			print("exception found,details: " +str(e))

	if status == 'True':
		print("Search Results:")
		print('Port is Open on the Firewall {} '.format(device))
	else:
		print("Search Results:")
		print("Sorry Port is NOT open,Please place a request on Service Now to open ACL")

		