#!/usr/bin/env python3
import os
import sys
sys.path.insert(1, './lib/shared_libs/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile
# wc.jd(wc.wcheader)
import awx

# wc.jd(wc.argv_dict)
ansible = awx.AWX(os.environ['AWX_IP'], os.environ['AWX_USER'], os.environ['AWX_PASS'])
# ansible.GetInventory()

# Run Playbook=AWX_PLAYBOOK_NAME
# Input/Overload variables == BUBBLED TO JENKINS PARAMETERS (ENV|os.environ PROVIDED VIA JENKINSFILE)
  # argv provided on orchPy paramater
  # env provided via jenkins global and non-orchPy parameters
print(ansible.RunPlaybook(wc.argv_dict['Playbook'],args=wc.env_dict))

