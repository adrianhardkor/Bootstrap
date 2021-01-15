#!/usr/bin/python3
import sys
sys.path.insert(1, './lib/shared_libs/')
import wcommon as wc
# wc.jd(wc.wcheader)

from bs4 import BeautifulSoup

user = wc.argv_dict['user']
data = wc.exec2('curl -s --netrc-file /opt/self.creds http://%s:8080/configure' % wc.argv_dict['server'])

result = {}
parsed = BeautifulSoup(data, features="html.parser")
for line in parsed.find_all('input'):
	line = str(line)
	flag = ''
	if '_.configID' in line:
		flag = 'xrayConnectorId'
	elif '_.alias' in line:
		flag = 'xrayUser'
	if flag != '':
		line = wc.mcsplit(line, ' ')
		out = {}
		for l in line:
			if '=' in l:
				l = l.split('=')
				# wc.pairprint(l[0], l[1])
				out[str(l[0])] = l[1].split('"')[1]
		if flag == 'xrayConnectorId':
			xrayConnectorId = out['value']
		elif flag == 'xrayUser':
			try:
				out['xrayConnectorId'] = xrayConnectorId
				result[out['value']] = out
			except Exception:
				pass	

if user + '-Xray' in result.keys():	
	print(result[user + '-Xray']['xrayConnectorId'])
else:
	print('81980372-6ec2-4708-8f2d-3536cb95fd59')
