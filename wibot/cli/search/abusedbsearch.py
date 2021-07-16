import click
import requests
import json
import os
import re
import string



@click.group(help='Search Abuse DB')
def abusedb():
	pass

@abusedb.command(help = 'Search Abuse DB')
@click.argument('srcip')
def abusedb(srcip):
	abusedb_url = "https://www.abuseipdb.com/check/{}".format(srcip)
	payload={}
	headers = {
	  'Cookie': '__cfduid=de32f8acb2c786a2922d29d0fb8baa00a1615786307; XSRF-TOKEN=eyJpdiI6Ik5nZjZKNkMyK2h6R2hGMk9tVnY5ZlE9PSIsInZhbHVlIjoiK3NcLzg0Q3VHZHJJbTRXYUY2em9sZkt4VHBoNDhrbjFSbFZLRTFyYVdmeFZVSnphYjliTXlERUluYlJjcXY5eU0iLCJtYWMiOiIyYTA0M2FiODIwNmMwYTJkYzhkODUwOTdjMDRhNjQ0ZjYwZWFiZjBmMjk0NGJkMzYxMTczMmFlNTM3NzNjZTcwIn0%3D; abuseipdb_session=eyJpdiI6Im50cXg3Q1dnRCtXRWxHS0s1YU9cLytRPT0iLCJ2YWx1ZSI6Ikc1Rk9hQm5XZjZsXC9FZit6WUppQkR3UEd1RklQMDFCZnZEdm5WMzN3ZlwvMnpnaGE2ZTJyYjdSODlSWVBRODNJMSIsIm1hYyI6ImVjMGYzYjdkOTBhMDJhZmU3NTQ1NGE0N2E3NGUwMWQ0NDMyYWIxOGUwYWUzM2ZiYWM5OGZmNDU1MmNlNDgzYmUifQ%3D%3D'
	}
	response = requests.request("GET", abusedb_url, headers=headers, data=payload)
	unfiltered = response.text
	if response.status_code == 200:	
		if re.search("not",unfiltered):
			print("Input IP not found in Abuse DB , IP is safe to use")
		else:
			print("Malicious IP detected!")
	else:
		print("Sorry! Unable to connect to Abuse DB , please try again later")
