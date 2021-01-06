import os
from behave import given, when, then
import sys
# context: where behave runs
sys.path.insert(1, './lib/shared_libs/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile
wc.wcheader['packages']['wc'] = wc.__file__
wc.jd(wc.wcheader)


@given(u'Bootstrap Ran')
def step_impl(context):
	assert True

@when(u'I try to ping NewMgmtIP from Jenkinsfile-paramter-input cidr')
def step_impl(context):
	wc.jd(wc.env_dict)
	context.ip = wc.env_dict['cidr'].split(' /')[0]
	context.pingable = bool(wc.is_pingable(context.ip))
	pass

@then(u'I expect response "{expectationBoolean}"')
def step_impl(context, expectationBoolean):
	expectationBoolean = wc.bdd_bool_inp(expectationBoolean)
	print('\t'.join(['',context.ip,'actual:' + str(context.pingable),'','expected:' + str(expectationBoolean)]))
	assert context.pingable == expectationBoolean
