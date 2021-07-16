# -*- coding: utf-8 -*-

"""Console script for wibot."""
import click
import sys
from wibot.cli.search.search_ipi import iprep as iprep
from wibot.cli.search.search_port import server_port as server_port
from wibot.cli.search.acl106search import acl106 as acl106
from wibot.cli.search.aclsearch import acl as acl
from wibot.cli.search.feedsrvr import feed as feed
from wibot.cli.search.abusedbsearch import abusedb as abusedb
from wibot.cli.search.geolocation import geolocdb as geolocdb
from wibot.cli.search.route_path import route_path as route_path
from wibot.cli.search.show_tech import tech as tech


@click.group(name='search')
def search(args=None):
	"""
	For detailed usage instructions 
	Please refer: https://wiki.cisco.com/display/AS13445/Awesom-o%27s+Usage+Guide
	"""
	pass



search.add_command(server_port)
search.add_command(geolocdb)
search.add_command(abusedb)
search.add_command(iprep)
search.add_command(acl)
search.add_command(acl106)
search.add_command(feed)
search.add_command(route_path)
search.add_command(tech)

if __name__ == "__main__":
    sys.exit()  # pragma: no cover
