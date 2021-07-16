import os
import click

@click.group(help='Search path between two IPs')
def route_path():
	pass

@route_path.command(help='Search path between two IPs')
def route_path():
	print("** Feature Currently Under Development **")
      