#!/usr/bin/env python3
import os
import sys
sys.path.insert(1, './lib/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile
wc.jd(wc.wcheader)
import awx

ansible = awx.AWX('10.88.48.33', 'admin', 'password')
# ansible.GetInventory()
print(ansible.RunPlaybook('Bootstrap'))
