#!/usr/bin/python3
import os
import sys
sys.path.insert(1, './lib/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile

import json
import behave2cucumber

raw = wc.read_file(sys.argv[1])
behave_json = json.loads(raw)
cucumber_json = behave2cucumber.convert(behave_json)
wc.rmf(sys.argv[2])
wc.post_fname(json.dumps(cucumber_json), sys.argv[2])
exit(0)
