import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException

# these are just simple python formatted files with variables in them
# the WLC IP and credentials are in here
from credentials import *

# first we want to grab all the APs that the WLC knows about

# this loads the devices we're working with from a simple CSV file
# I often alter this file depending on what I'm working on
switches = csv.DictReader(open("switches.csv"))

for row in switches:	
	# this initializes the device object
	# it pulls the username/password/secret variables from a local file called 'credentials.py'
	# the IP is pulled from the 'switches.csv' file
	cisco_switch = {
		    'device_type': 'cisco_ios',
		    'ip': row['IP'],
		    'username': username,
		    'password': password,
		    'port' : 22,          # optional, defaults to 22
		    'secret': secret,     # optional, defaults to ''
		    'verbose': False,       # optional, defaults to False
		}
		
	try: # if the switch is reponsive we do our thing, otherwise we hit the exeption below
		# this actually logs into the device
		net_connect = ConnectHandler(**cisco_switch)
		# we gather a list of APs learned via CDP
		cdp_neighbor = net_connect.send_command('sh cdp neigh | i SEP').split("\n")

		for cdp_neighbor_entry in cdp_neighbor:
			if len(cdp_neighbor_entry) <= 0:
				continue
			else:
				hostname = str(cdp_neighbor_entry.split()[0])
				interface = cdp_neighbor_entry.split()[1] + " " + cdp_neighbor_entry.split()[2]
				output = row['Switch'] + "," + hostname + "," + interface
				print output
		net_connect.disconnect()
	except (NetMikoTimeoutException, NetMikoAuthenticationException):
		pass
