import click
import paramiko
from paramiko import SSHClient
import time
import re

USERNAME = 'akbansal'
PASSWORD = 'Pass@123'
bigip_server= 'jfk10-ddos-bigip01.webex.com'

try:
	ssh_client: SSHClient = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
except Exception as e1:
	print("main exception " + str(e1))


@click.group(help="To search IP information in Geolocation  DB")
def geolocdb():
	pass

@geolocdb.command(help="To search IP information Geolocation DB")
@click.argument('ip_address')
def geolocdb(ip_address):
	try:
		ssh_client.connect(bigip_server,username=USERNAME,password=PASSWORD)
		chan = ssh_client.invoke_shell()
		temp = chan.recv(1024).decode('ascii')
		chan.send("bash\n")
		time.sleep(1)
		temp = chan.recv(1024).decode('ascii')
		chan.send("geoip_lookup {}\n".format(ip_address))
		time.sleep(2)
		temp = chan.recv(5000).decode('ascii')
		print("User: Awesom-o is querying the Geolocation DB")
		print("************************************************************")
		print("Search Query:")
		data = temp.splitlines()
		for line in data:
			if re.search("Marvinh",line):
				pass
			else:
				print(line)
		ssh_client.close()

	except paramiko.ssh_exception.AuthenticationException:
		print("Authentication Failure")

	except Exception as e:
		print(e)
		print("Sorry ! Unable to connect to Geolocation DB, Please try again after some time")
	
