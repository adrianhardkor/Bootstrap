import wcommon as wc
import json,requests,ipaddress,time
class AWX():
	def __init__(self, IP, user, pword):
		self.user = user
		self.pword = pword
		self.IP = IP
		self.__name__ = 'AWX'
	def mcsplit(mystr, cc):
		# handler for multiple splits
		if type(cc) == str:
			chars1 = []
			chars1[:0] = cc
		elif type(cc) == list:
			chars1 = cc
		for c in chars1:
			mystr = mystr.replace(c, ',')
		return(mystr.split(','))
	def IP_get(n):
		# GET ATTRIBUES FOR CIDR BLOCK
		# >>> from netaddr import IPAddress
		# >>> IPAddress('255.255.255.0').netmask_bits()
		# 24
		n = n.strip()
		cidr_split = AWX.mcsplit(n, ['/',' '])
		cidr = ipaddress.IPv4Network(('0.0.0.0',cidr_split[1])).prefixlen
		try:
			addr4 = ipaddress.ip_interface(n)
		except ValueError:
			return(['', '',cidr])
		netAddress = str(addr4.network)
		try:
			net = ipaddress.ip_network(netAddress)
			hosts = []
			for ip in net:
				hosts.append(str(ip))
			if bool([cidr_split[0]] == hosts):
				return([str(addr4.network), '',cidr])
			elif cidr_split[1] != '31' and cidr_split[1] != '255.255.255.254':
				hosts.pop()
				hosts.pop(0)
			return([str(addr4.network), hosts,cidr])
		except Exception as err:
			return([str(addr4.network), err,cidr])
	def listprint(deli,lst):
		out = []
		for l in lst:
			out.append(str(l))
		print(deli.join(out))
	def list2dict(lst):
		if lst == [] or lst == [''] or lst == ['---']:
			return({})
		return({lst[i]: lst[i + 1] for i in range(0, len(lst), 2)})
	def RunPlaybook(self,playbook_name,args={}):
		# ASYNC BY DEFAULT
		playbook_start = wc.timer_index_start()
		if args != {}:
			args = json.dumps({'extra_vars':args})
		data = json.loads(wc.REST_POST('http://' + self.IP + '/api/v2/job_templates/' + playbook_name + '/launch/', user=self.user, pword=self.pword, args=args))
		status_url = data['url']
		data['status'] = 'Running'
		if 'job' not in data.keys():
			# SOMETHING WENT WRONG
			wc.jd(data)
			return('')
		job = str(data['job'])
		playbook = data['playbook']
		inventory = str(data['inventory'])
		while data['status'] not in ['successful','failed']:
			time.sleep(5)
			data = json.loads(wc.REST_GET('http://' + self.IP + status_url, user=self.user, pword=self.pword))
			print('  '.join([job,playbook,inventory,data['status'],'',str(wc.timer_index_since(playbook_start))]))
		if data['status'] == 'successful':
			endpoint = data['related']['stdout']
		else:
			endpoint = data['related']['stderr']
		return(json.loads(wc.REST_GET('http://' + self.IP + endpoint, user=self.user, pword=self.pword))['content'])
		# ['related']['stdout']
		# POST https://your.tower.server/api/v2/job_templates/<your job template id>/launch/ with any required data gathered during the previous step(s). The variables that can be passed in the request data for this action include the following.
		# extra_vars: A string that represents a JSON or YAML formatted dictionary (with escaped parentheses) which includes variables given by the user, including answers to survey questions
		# job_tags: A string that represents a comma-separated list of tags in the playbook to run
		# limit: A string that represents a comma-separated list of hosts or groups to operate on
		# inventory: A integer value for the foreign key of an inventory to use in this job run
		# credential: A integer value for the foreign key of a credential to use in this job run
	def GetInventory(self):
		_INV = {}
		data = json.loads(wc.REST_GET('http://' + self.IP + '/api/v2/inventories', user=self.user, pword=self.pword))
		for inventory in data['results']:
			# single page
			wc.pairprint(inventory['id'],inventory['name'])
			_INV[inventory['name']] = {}
			hosts = json.loads(wc.REST_GET('http://' + self.IP + inventory['related']['hosts'], user=self.user, pword=self.pword))
			for host in hosts['results']:
				print(host['name'])
				# single page
				mylist = AWX.mcsplit(host['variables'], ['\n', ': '])
				host['variables'] = AWX.list2dict(mylist)
				facts = json.loads(wc.REST_GET('http://' + self.IP + host['related']['ansible_facts'], user=self.user, pword=self.pword))
				interestingfact = {}
				interestingfact['id'] = host['related']['ansible_facts'].split('/')[4]
				if 'ansible_default_ipv4' in facts.keys():
					# has CIDR info (add cidr from device)
					cidr = str(AWX.IP_get(host['name'] + ' ' + facts['ansible_default_ipv4']['netmask'])[-1])
					interestingfact['networks'] = [ AWX.IP_get(host['name'] + '/' + cidr)[0] ]
					interestingfact['mac'] = facts['ansible_default_ipv4']['macaddress']
				if 'junos' in facts.keys():
					# JUNIPER
					interestingfact['model'] = facts['junos']['model']
					interestingfact['junos'] = {}
					for re in facts['junos']['junos_info'].keys():
						interestingfact['junos'][re] = facts['junos']['junos_info'][re]['text']
					interestingfact['dns'] = facts['ansible_dns']['search']
					interestingfact['api'] = facts['ansible_net_api']
					interestingfact['intf'] = {}
					for intf in facts['ansible_net_interfaces'].keys():
						interestingfact['intf'][intf] = '/'.join([facts['ansible_net_interfaces'][intf]['oper-status'],facts['ansible_net_interfaces'][intf]['admin-status']])
					for n in facts['ansible_network_resources']['l3_interfaces']:
						if 'ipv4' in n.keys():
							for block in n['ipv4']:
								interestingfact['networks'].append(block['address'])
				elif 'ansible_devices' in facts.keys():
					# LINUX
					interestingfact['ansible_devices'] = list(facts['ansible_devices'].keys())
					interestingfact['vendor'] = facts['ansible_devices']['sda']['host'] + ' '  + facts['ansible_devices']['sda']['vendor']
					interestingfact['hdd'] = facts['ansible_devices']['sda']['size']
				
				AWX.listprint('  ', [host['name'], host['enabled'], host['variables'], interestingfact])
				_INV[inventory['name']][interestingfact['id']] = {'Host':host['name'],
					'Enabled':host['enabled'],
					'Variables':host['variables'],
					'facts':interestingfact}
		wc.jd(_INV)
		return()
