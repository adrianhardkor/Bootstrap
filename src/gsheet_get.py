#!/usr/bin/python3
import sys
import string
sys.path.insert(1, './lib/shared_libs/')
import wcommon as wc
# wc.header()
import wgcp 

# GOOGLE PUBLIC CLOUD
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1lChMjk1OMyZlEmX8TqUjHOwILoBSnCUpm4evrPvLork'
SAMPLE_RANGE_NAME = 'Login_pwd'

# build class
UNIT_ASSET = wgcp.GCP(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, SCOPES, './src/runner.pickle', './src/credentials.json')
handle = UNIT_ASSET.Connect(); # connect to google

# CONVERT GSHEET AND SORT BY 'IP'
sheet = UNIT_ASSET.GET(handle)
sheet = UNIT_ASSET.CONVERT_JSON_BY_HEADER(sheet, 'Device')

for attempt in sheet.keys():
	print(sheet[attempt])
exit(0)
