import os
import sys
# context: where behave runs
sys.path.insert(1, './lib/shared_libs/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile
wc.wcheader['packages']['wc'] = wc.__file__
# wc.jd(wc.wcheader)
# wc.jd(wc.env_dict)

from behave import given, when, then
from hamcrest import assert_that, equal_to, is_not

print(wc.exec2('cat ./features/*.feature'))


# LOOPBACK FOR INVENTORY REACHABILITY

@given(u'Test Setup')
def step_impl(context):
	# Reserve Topology
		# velocity (REST)
		# get devices availble in ARC
		# velocity returns availbe devices
		# configure port speed
		# velocity reserves topology (and configures Lepton wire1)
			# Wire Once -- LEPTON
	# Router Config - Zone Change?
		# ansible
		# run playbooks on Available devices
			# changes cmts/modem zone
			# modem reboots - PDU_REST
			# inventory sync (zone change = asset-mgmt change)
	# Traffic
		# run the build-script: iTest or STC-Python script or LabServer-REST
	# GL/Twillio setup
		# build calls to execute - python/REST
	pass

@when(u'I try to run "{traffic_load}"')
def step_impl(context):
	traffic_load = traffic_load.split(' ')[1]; # 60MB/10MB
	# configure $traffic_load on Spirent
	# send traffic _____ seconds?

	# BASELINE
	# verify no frame loss -- ON SPIRENT?  ON ANSIBLE-ROUTER? on ANSIBLE_CMTS? ON MODEM-SELENIUM?
	# repeat for 5 times (loop)
	
	# TEST_START
	# 1) START TRAFFIC - STC
	# 2) WAIT 30 SECONDS
	# 3) PERFORM ANY MIGRATION FUNCTION -- MIGRATION TESTING ONLY
	# 3) REALTIME DURING TRAFFIC STATS FROM ROUTER, CMTS, MODEM? via ANSIBLE?
		# VARIABLE context.DEVICE_TRAFFIC
	# 4) WAIT 30 SECONDS
	# 5) STOP TRAFFIC - ON STC
	# 6) CALUCLATE PACKETLOSS/THROUGHPUT (loss time / pps) - STC
		# VARIABLE context.STC_TRAFFIC
	assert True is not False

@then(u'I expect "{percentNum}" percent provisioned bandwidth'}
def step_impl(context, percentNum):
	if context.STC_TRAFFIC >= percentNum and context.DEVICE_TRAFFIC >= percentNum:
		assert True
	else:
		# failed feature
		assert False
