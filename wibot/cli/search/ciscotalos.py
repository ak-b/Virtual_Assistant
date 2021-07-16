import os
import click
import requests

@click.group(help='Search IP Threats on Cisco Talos')
def ciscotalos():
	pass

@ciscotalos.command(help = 'Search IP Threats on Cisco Talos')
@click.argument('srcip')
def ciscotalos(srcip):
	search_url='https://talosintelligence.com/reputation_center/lookup?search={}'.format(srcip)
	response= requests.get(search_url)
	print("Request Response Code")
	print(response.status_code)
