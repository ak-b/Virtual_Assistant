import os
import click
import re
import paramiko
from paramiko import SSHClient

feed_server = '10.252.131.11'
username = 'akbansal'
password = 'Newmuffintop123@'

@click.group(help='Search Feedserver for Allow/Deny IP list')
def feed():
	pass

@feed.command(help = "Search Feedserver for Allow/Deny IP list")
def feed():
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(feed_server, username=username, password=password)
		sftp = ssh.open_sftp()
		dirname = '/var/www/html/iad02-ddos-ipifs'
		filename = 'F5-BL_WL-feed.txt'
		f = sftp.open(dirname + '/' + filename, 'r')
		print("Contents of the Feed File on the Feedserver")
		try:
			for line in f:
				print(line.strip('\n'))
		finally:
			f.close()
		ssh.close()

	except paramiko.ssh_exception.AuthenticationException:
		print("Authentication Failure")
	except Exception as e:
		print("Sorry! I am unable to connect to FeedServer,please try after sometime")
