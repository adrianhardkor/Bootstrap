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

@given(u'Bootstrap Ran')
def step_impl(context):
	pass

@when(u'I try to ping NewMgmtIP from Jenkinsfile-paramter-input cidr')
def step_impl(context):
	ip = wc.env_dict['cidr'].split('/')[0] 
	context.ip = ip
	context.pingable = wc.bdd_bool_inp(wc.is_pingable(ip))
	assert True is not False

@then(u'I expect response "{expectationBoolean}"')
def step_impl(context, expectationBoolean):
	expectationBoolean = wc.bdd_bool_inp(expectationBoolean)
	wc.pairprint('expected',expectationBoolean)
	wc.pairprint('actual',context.pingable)
	assert_that(expectationBoolean, equal_to(context.pingable))
