import sys 
import os
import time
import re
import paramiko 
from paramiko import SSHClient
import re
import os
import click


BOT_USERNAME='akbansal'
BOT_PASSWORD='Pass@123'
ENABLE_PASSWORD ='C1sc0@FW582'


try:
	ssh_client: SSHClient = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
except Exception as e1:
	print("main exception " + str(e1))

@click.group(help="Download Show Tech Detail")
def tech():
	pass

@tech.command(help="Download Show Tech Detail")
@click.argument('device')
def tech(device):
	try:
		ssh_client.connect(hostname=device, username=BOT_USERNAME, password=BOT_PASSWORD,\
			allow_agent=False, look_for_keys=False, timeout=10)
		chan = ssh_client.invoke_shell()
		temp = chan.recv(1024).decode('ascii')
		#print("Logged in")
		#print(temp)
		chan.send("enable\n")
		time.sleep(2)
		temp = chan.recv(1024).decode('ascii')
		#print(temp)
		# add enable password once you test out prod devices
		if re.search("Password:", temp):
			chan.send("%s\n" % ENABLE_PASSWORD)
		chan.send("terminal page 0\n")
		temp = chan.recv(1024).decode('ascii')
		time.sleep(1)
		chan.send("changeto system\n")
		time.sleep(1)
		temp = chan.recv(1024).decode('ascii')
		if re.search('asacl',device):
			chan.send("cluster exec show tech-support\n")
		elif re.search('asa',device):
			chan.send("show tech-support\n")
		elif re.search("fpr",device):
			chan.send("connect local-mgmt\n")
			chan.send("show tech-support chassis 1 detail\n")
		time.sleep(5)
		temp = chan.recv(100000).decode('ascii')
		print(temp)
		tech_filedir ='/logs/'
		tech_file_name ='show-tech-detail.txt'
		tech_filepath = os.path.join(tech_filedir, tech_file_name)
		if os.path.exists(tech_filepath):
			os.remove(tech_filepath)
			print("Old file removed")
		techsup_file = open(tech_filepath,'a+')
		techsup_file.write('\n' + temp + '\n')

		techsup_file.close()
		ssh_client.close()

	except paramiko.ssh_exception.AuthenticationException:
		print("Authentication Failure on device {}".format(device))
	except Exception as e:
		print("Encountered exception" +str(e))
		print("Device %s" % device)

