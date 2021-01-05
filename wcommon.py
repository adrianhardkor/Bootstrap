from __future__ import print_function
import datetime
import copy
import subprocess
import ipaddress
from xml.etree import ElementTree as ET
from collections import defaultdict
from time import sleep
import time
import sys
import csv
import json
import platform
import os
import re
import getpass
# import shutil
import binascii
import requests
import paramiko
from urllib3.exceptions import InsecureRequestWarning
import uuid

def import_or_install(package):
    import pip
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])     
packages = ['datetime','platform','copy','subprocess','ipaddress','xml','collections','time','sys','csv','json','os','re','getpass','shutil','binascii','requests','paramiko','urllib3','uuid']

try:
    basestring
except NameError:
    # python3
    basestring = str

global argv_dict
global wow_time
global clock_format
clock_format = '%a, %d %b %Y %H:%M:%S GMT'

def bdd_bool_inp(inp2):
	if str(inp2).lower() == 'true':
		return(True)
	elif str(inp2).lower() == 'false':
                return(False)

def now():
    # CURRENT TIME
    return(time.ctime(time.time()))

def jd(mydict):
    # json.dumps shorthand
    out = json.dumps(mydict, sort_keys=True, indent=2)
    print(out)
    pairprint('Timestamp',fullRuntime())
    print('\n')
    return(out)

def timer_index_start():
    # timer sub-commands
    global timer
    timer = time.time()
    return(timer)

# Init wow-common library timestamp (start of scripts)
wow_time = timer_index_start()

def wait_start():
    # animation scroller for waiting for things to work
    global animation
    global idx
    animation = "|/-\\"
    idx = 0


def expand(unformatted):
    # 1-3 into [1,2,3]
    result = []
    unformatted = unformatted.split('-')
    start = int(unformatted[0])
    while start <= int(unformatted[1]):
        result.append(start)
        start += 1
    pairprint(unformatted, result)
    return(result)


def wait_update():
    # animation scropper for waiting for things to work
    global animation
    global idx
#    try:
#        print(animation[idx % len(animation)], end="\r")
#    except SyntaxError:
#        print(animation[idx % len(animation)])
    idx += 1


def do_nothing():
    return()


def encode(s):
    s = str(s)
    unic = 'utf-8'
    s = bytes(s, unic)
    s = binascii.hexlify(s)
    # s = s.decode(unic)
    return(s)


def decode(s):
    unic = 'utf-8'
    un = binascii.unhexlify(s)
    un = un.decode(unic)
    return(un)


def genUUID(identifyer):
    # convert from input, so UUID always same, if same input
    myUUID = uuid.uuid3(uuid.NAMESPACE_X500, identifyer)
    # myUUID = ''
    # pairprint(identifyer, myUUID)
    return(str(myUUID))


def covertMaskToCIDR(netmask):
    # 255.255.255.0 = 24
    return(sum(bin(int(x)).count('1') for x in netmask.split('.')))


def IP_get(n):
    # GET ATTRIBUES FOR CIDR BLOCK
    # >>> from netaddr import IPAddress
    # >>> IPAddress('255.255.255.0').netmask_bits()
    # 24
    n = n.strip()
    cidr_split = mcsplit(n, '/ ')
    cidr = ipaddress.IPv4Network((cidr_split[0],cidr_split[1])).prefixlen
    try:
        addr4 = ipaddress.ip_interface(n)
    except ValueError:
        return(['', ''])
    netAddress = str(addr4.network)
    try:
        net = ipaddress.ip_network(netAddress)
        hosts = []
        for ip in net:
            hosts.append(str(ip))
        if bool([cidr_split[0]] == hosts):
            return([str(addr4.network), ''])
        elif cidr_split[1] != '31' and cidr_split[1] != '255.255.255.254':
            hosts.pop()
            hosts.pop(0)
        return([str(addr4.network), hosts])
    except Exception as err:
        return([str(addr4.network), err])


def sorted_dict(inDict):
    # sort in-dict (without .dumps)
    result = {}
    for i in sorted(inDict):
        result[i] = inDict[i]
    return(result)


def dict_move(myDict, old, new):
    # move to new mem space
    if old == new: return(myDict)
    myDict[new] = myDict[old]
    del myDict[old]
    return(myDict)

def cleanLine(line):
    # split by space and tab, and special char's
    # used as an 'awk'
    result = []
    mcs = mcsplit(line, ' \t')
    for word in mcs:
        if word != '':
            result.append(word)
    return(result)


def lfind(myList, what):
    # return list of indexes
    return([i for i, x in enumerate(myList) if x == what])
    try:
        result = myList.index(what)
    except ValueError:
        result = -1
    return(result)


def per(unit, of):
    # percentage handler
    # echo_param({'unit': unit, 'of': of})
    unit = float(unit)
    of = float(of)
    major = unit / of
    major = major * 100
    return(str(int(major)) + '%')


def cp(element):
    # deepcopy handler
    # cp = timer_index_start()
    result = copy.deepcopy(element)
    # pairprint('deepcopy', timer_index_since(cp))
    return(result)

def qcp(element):
        # quick copy for large dict - new mem spaces
        result = ''
        if type(element) is dict:
                result = {}
                for tag in element:
                        if type(element[tag]) == str:
                                result[tag] = str(element[tag])
                        elif type(element[tag]) == list:
                                result[tag] = []
                                for l in element[tag]:
                                        result[tag].append(l)
                        else:
                                print('qcp failure')
                                exit(5)
        return(result)

def str_int_split(raw):
    # ge-1/0/8 = ['ge', '-1/0/8']
    strings = []
    integers = []
    for r in list(raw):
        if r.isdigit():
            integers.append(str(r))
        else: strings.append(r)
    return(''.join(strings), ''.join(integers))


def could_be_int(element):
    # if type could be int
    if element == '':
        return(1)
    try:
        blah = float(element) + 1
        return(1)
    except Exception:
        return(0)


def grep(re, output):
    # grep regex against string
    result = []
    for line in output.split('\n'):
        if string_match(re, line): result.append(line)
    result = "\n".join(result)
    return(result)


def ls(path):
    # os.exec an ls $path
    result = sorted(exec2('ls ' + path).split('\n'))
    for popMe in lfind(result, ''): result.pop(popMe)
    return(result)


def return_code_error(message):
    # python handler for TCL thinking
    message = "\n\n%s" % message
    raise Exception(message)


def split(word):
    return [char for char in word]


def lremove(myList, element):
    return([x for x in myList if element not in x])

def fname_age(fname):
    global clock_format
    try:
        fname_epoch = os.path.getmtime(fname)
    except FileNotFoundError:
        return(['',''])
    my_epoch = current_time
    age = int(my_epoch) - int(fname_epoch)
    return([age, time_epoch_human(age)])

def fname_age_check(fname):
    age = fname_age(fname)
    try:
        if int(age[1][0]) > 0:
            pass
    except IndexError:
        pass 

def rmf(fname):
    # remove file
    try:
        return(os.remove(fname))
    except OSError as err:
        return(err)


def rmrf(dirname):
    # remove dir
    try:
        result = shutil.rmtree(dirname)
    except OSError as e:
        result = 'Warning: %s - %s' % (e.filename, e.strerror)
    return(result)

def touch(fname):
    try:
        os.utime(fname, None)
    except OSError:
        open(fname, 'a').close()

def exec2(command):
    # execute shell command, handle stdout stderr
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (stdout, stderr) = output.communicate()
    return(bytes_str(stdout).strip())

def bytes_str(data):
    try:
        # data = data.decode("utf-8")
        data = data.decode("utf-8")
    except Exception:
        pass
    return(data)

def str_insert(old,num,new):
    return(old[:num] + new + old[num:])

def post_fname(data, fname):
    # write data to fname
    f = open(fname, "a")
    for line in data.split('\n'):
        f.write(line)
    f.close()
    return(data)

def log_fname(data, fname):
    # write data to fname
    f = open(fname, "a+")
    for line in data.split('\n'):
        f.write(line + '\r\n')
    f.close()
    return(data)

def read_binary_file(fname):
    # if read_file fails as binary-file, retry as binary
    result = []
    try:
        f = open(fname, 'rb')
    except FileNotFoundError:
        return('')
    return(f.readlines())
    with open(fname, 'rb') as f:
        for line in f.readline():
            result.append(line)
    return(result)


def read_file(fname):
    # read file, if fails, try as binary
    try:
        f = open(fname, "r")
    except FileNotFoundError:
        return('')
    try:
        contents = f.read()
    except UnicodeDecodeError:
        return(read_binary_file(fname))
    except Exception:
        return('')
    contents = contents.strip('\r')
    contents = contents.strip('\n')
    return(contents)


def log_json(mydict, fname):
    # write dict to fname file as json.dumps
    myjson = json.dumps(mydict, sort_keys=True, indent=2)
    f = open(fname, "w")
    f.write(myjson)
    f.close()

def list_match(regex, mylist):
    # same as re.match
    r = re.compile(regex)
    return(list(filter(r.match, mylist)))


def string_match(regex, word):
    # old TCL thinking, regex against string
    if regex in word: return(True)
    else: return(False)
    return bool(re.search(regex, word))

def mcstrip(mystr, cc):
    # handler for multiple strips
    chars1 = []
    chars1[:0] = cc
    for c in chars1:
        mystr = mystr.strip(c)
    return(mystr)

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


def execPy(command):
    # exec via os.system
    out = os.system(command)
    return out

def timer_index_since(index=-1):
    # time handler
    if index == -1:
        global timer
    else:
        timer = index
    x = (time.time() - timer) * 1000
    return(float("{0:.2f}".format(x)))

def array_get(ary):
    # TCL handler for ary/dict
    return sorted(ary.items())

def lunique(list1):
    # lunique handler for list
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)


def findList(regex, mylist):
	return(lsearchAllInline(regex, mylist))

def lsearchAllInline(regex, mylist):
    return([name for name in mylist if regex in name])

def lsearchAllInline2(regex, mylist):
    # find via re
    r = re.compile(regex)
    newlist = list(filter(r.match, mylist))
    return(newlist)

def pairedList(myl):
    # ['eng1', 'WOPR', 'eng2', 'VOLTRON'] = 
    # {'eng1': 'WOPR', 'eng2': 'VOLTRON'}
    result = {}
    for i in range(0, len(myl), 2):
        index = str(myl[i])
        value = str(myl[i + 1])
        # pairprint(index, value)
        if index in result:
            # append
            if type(result[index]) is str:
                # pairprint('already', type(result[index]))
                # new
                spare = result[index]
                result[index] = []
                result[index].append(spare)
            result[index].append(value)
        else: result[index] = value
        # print('\t' + str(result))
    return(result)


def echo_param(ary):
    # print dict pretty
    return(parray_slow(ary))

def pairprint(i, v, printMe=True):
    # print (i,v) pretty
    result = "%s = '%s'" % (str(i), str(v))
    if printMe:
        print(result)
    else:
        return(result)

def parray_slow(ary):
    # print no matter what type()
    # template = "{0:20}|{1:20}"
    border = "==========================================="
    print(border)
    if type(ary) is dict:
        for i, v in array_get(ary):
            print("%s = '%s'" % (str(i).ljust(20), v))
    elif type(ary) is str:
        jd(ary)
    elif type(ary) is list:
        for i, v in pairedList(ary):
            print("%s = '%s'" % (str(i).ljust(20), v))
    print(border)
    return("")

def sendmail(destinations, subject, data, source='arc-wopr@wowinc.com'):
    if destinations == '': return()
    for dest in destinations.split(', '):
        print('\t'.join(['SENDMAIL:', subject, dest, send_email_single(dest, subject, data, source)]))
    return()


def send_email_single(dest, subject, data, source='arc-wopr@wowinc.com'):
    sendmail_location = "sendmail"
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % source)
    p.write("To: %s\n" % dest)
    p.write("Subject: %s\n" % subject)
    p.write("\n") 
    p.write(str(data))
    p.write("\n") 
    status = p.close()
    try:
        # push p to complete fast
        p.write("\n")
    except ValueError:
        do_nothing()
    if str(status) == 'None': status = 'Success'
    return(status)


# SSH
def run_commands_paramiko(commands, IP, driver, remote_conn, quiet):
    result = paramiko_send_expect(commands, IP, remote_conn, driver, quiet)
    return(result)

def device_buffering_commands(driver):
    commands = []
    if driver == "cisco_ios": commands = ['term len 0', '']
    elif driver == "cisco_nxos": commands.insert(0, 'terminal length 0')
    elif driver == "juniper_junos": commands.insert(0, 'set cli screen-length 0')
    elif driver == 'mrvTS': commands.insert(0,'no pause')
    elif driver == 'mrv_mcc':
        commands.insert(0,'term width 512')
        commands.insert(0,'term len 0')
    return(commands)

def device_prompt(tn, driver):
    runtime_device_prompt = timer_index_start()
    # capture prompt instead of setting prompt
    str2 = ''
    while str2 == '':
        tn.send("\n")
        time.sleep(.4)
        str2 = bytes_str(tn.recv(65535))
        str2 = str2.split('\r\n')[-1]
        # print(" - Waiting.. '%s'" % str2)
    global prompt
    prompt = str2
    print("DEVICE PROMPT = \'%s\' Took %s" % (str2, timer_index_since(runtime_device_prompt)))
    return(str2)

def get_prompt():
    global errorPrompt
    default = "hf3023f23jfg02gn30n23ggm}{}:<>"
    global prompt
    prompt = {}
    errorPrompt = {}
    prompt['cisco_ios'] = "([a-zA-Z0-9\-\.\(\)\_]*[>#])"
    errorPrompt['cisco_ios'] = "(nable to get configuratio)"
    prompt['cisco_nxos'] = "([a-zA-Z0-9\-\.\(\)\_]*[># ])"
    errorPrompt['cisco_nxos'] = default
    prompt['juniper_junos'] = "([@]+[a-zA-Z0-9\.\-\_]+[>#%]+[ ])"
    errorPrompt['juniper_junos'] = default
    # prompt['f5'] = "([\[]+[a-zA-Z0-9\:\;\.\-\_]+[@]+[a-zA-Z0-9\(\)\/\~\_\-\:\;\ ]+[\]])|([a-zA-Z0-9\:\;\.\-\_]+[@]+[a-zA-Z0-9\/\~\_\-\(\)\:\;\ \(\)\]]+[#])|\(tmos\)\# "
    errorPrompt['f5'] = default

    prompt['mrvTS'] = "([a-zA-Z0-9\-\_]+[0-9\:\ ]+[>])"
    errorPrompt['mrvTS'] = "(Syntax Error)"
    prompt['mrv_mcc'] = "([a-zA-Z0-9\-\.\(\)\_]+[#]+[\ ])"
    errorPrompt['mrv_mcc'] = errorPrompt['cisco_ios']
    return()

def mgmt_login_paramiko(ip, username, driver, quiet, password='', ping=True):
    global login_diff
    login_time = timer_index_start()
    global wow_time
    if ping:
        ping_result = is_pingable(ip)
        print('PING %s:  %r @ %s' % (ip, ping_result, timer_index_since(WOW_time)))
        if ping_result == False:
            return_code_error("\n\nUnexpected error:\nPing:%s" % ping_result)
    global paramiko_buffer
    global sleep_interval
    global prompt
    global passwords
    global result
    result = []
    paramiko_buffer = 65535
    # driver-less
    commands = device_buffering_commands(driver)

    if password == '':
        # global via dict/json
        password = passwords[ip]

    port = 22
    sleep_interval = .6
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if not quiet: echo_param({'IP': ip, 'port': port, 'username': username, 'pre-commands': commands})
    try:
        remote_conn_pre.connect(ip, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
    except Exception:
        return_code_error("\n\nUnexpected error, user %s: %s" % (username, sys.exc_info()[0]))
    print('Connection Built.. DONE:%s @ %s' % (timer_index_since(login_time), timer_index_since(wow_time)))

    remote_conn = remote_conn_pre.invoke_shell()
    output = remote_conn.recv(paramiko_buffer)
    result.append(bytes_str(output))

    # pre-commands
    paramiko_send_expect(commands, ip, remote_conn, driver, quiet)

    if not quiet: print(result)
    login_diff = timer_index_since(login_time)
    return(remote_conn)

def prompt_check(output, remote_conn, IP, prompt_status, quiet):
    # paramiko_ready(remote_conn, prompt_status, quiet)
    last_line = output.split('\n')
    print("prompt_check '%s'" % last_line)
    if string_match("assword", last_line[-1]):
        global passwords
        password = passwords[IP]
        remote_conn.send(password)
        time.sleep(0.03)
        remote_conn.send('\n')
        print('PASSWORD FOUND: %s' % last_line[-1])

def paramiko_ready(remote_conn, command, quiet, check):
    time.sleep(.4)
    while remote_conn.recv_ready() is False:
        # Not Ready
        time.sleep(0)
    if not quiet: print("\n\nReady/Sending:  '%s' = %r" % (command, remote_conn.recv_ready()))

def paramiko_send_expect(commands, IP, remote_conn, driver, quiet):
    global runcommands_diff
    diff = timer_index_start()
    s = '\n'
    global sleep_interval
    global result
    global prompt
    global paramiko_buffer
    thisPrompt = '.*%s$' % prompt[driver]
    regexPrompt = re.compile(thisPrompt)
    for command in commands:
        timer_index_start()
        output = ''
        check = 0
        if string_match('enable', command) and string_match('cisco_ios', driver): check = 1

        remote_conn.send(command + '\n')
        time.sleep(.6)
        paramiko_ready(remote_conn, command, quiet, check)

        prompt_status = regexPrompt.search(output)
        while prompt_status is None:
            if check: prompt_check(output, remote_conn, IP, prompt_status, quiet)
            buff = bytes_str(remote_conn.recv(paramiko_buffer))
            output += buff
            time.sleep(0.2)
            prompt_status = regexPrompt.search(output)
        result.append(output)
        if not quiet: print(output)
        print("DONE: '%s', took '%s'" % (command, timer_index_since()))
    runcommands_diff = timer_index_since(diff)
    return(s.join(result))

def humanSize(fileSize):
    fileSize = float(fileSize)
    divider = 1000.0
    for count in ['Bytes', 'KB', 'MB', 'GB']:
        if fileSize >= divider:
            # print("%3.1f%s" % (fileSize, count))
            fileSize = fileSize / divider
        else:
            return("%3.1f%s" % (fileSize, count))
    return("%3.1f%s" % (fileSize, 'TB'))

def IP_DNS(ID):
    # check if IP valid or dns-name
    if IP_get(ID + '/24')[0] != '':
        return('IP')
    else: return('DNS')

def is_pingable(IP):
    global matcher
    if IP == '': return(False)
    timer_index_start()
    global wcheader
    if 'darwin' in wcheader['platform']['os'].lower():
        ping_cmd = 'ping -c 2 '
    elif 'win' in wcheader['platform']['os'].lower():
        ping_cmd = 'ping -n 2 -w 3 '
    else:
        ping_cmd = 'ping -c 2 -W 3 '
    possible_zero_loss = [" 100.0% packet los", " 100% packet los", "100% loss"]
    output = exec2(ping_cmd + IP)
    result = True
    for zero in possible_zero_loss:
        if zero in str(output):
            result = False
    return(result)

def PARA_CMD_LIST(commands, ip, driver, username, password='', quiet=False,ping=True):
    global passwords
    global wow_time
    global login_diff
    global runcommands_diff
    global errorPrompt
    global prompt
    get_prompt(); # regex list 'global prompt'
    spawnID = mgmt_login_paramiko(ip, username, driver, quiet, password=password, ping=ping)
    if spawnID == -1:
        return('')
    timer_index_start()
    output = run_commands_paramiko(commands, ip, driver, spawnID, quiet)
    # command_time = timer_index_since()

    discontime = timer_index_start()
    # spawnID.disconnect(); # kills process, doesnt kill session
    spawnID.send('exit' + '\n'); # kills session
    disconnect_time = timer_index_since(discontime)

    # if not quiet:
    print("\n\n PARA_CMD_LIST Summary at %s" % timer_index_since(wow_time))
    print(" - Login Took: %s" % login_diff)
    print(" - Output Took: %s" % runcommands_diff)
    print(" - Exit Took: %s" % disconnect_time)
    sumIs = login_diff + runcommands_diff + disconnect_time
    print(" TOTAL Took: %s @ %s" % (float("{0:.2f}".format(sumIs)), timer_index_since(wow_time)))

    if string_match(errorPrompt[driver], output): return_code_error('Unknown Error on Switch: %s' % output)

    return output

def grep_until(begin, ending, data):
    # 'show run', 'end', list(output) 
    flag = 0
    result = []
    for each in data:
        if string_match(begin, each): flag = 1
        if string_match(ending, each): flag = 0
        if flag: result.append(each)
        # pairprint(each, flag)
    return(result)

def REST_GET(url, headers={"Content-Type": "application/json", "Accept": "application/json"}, user='', pword=''):
    # RETURNS JSON
    data = {}
    response = requests.get(url, auth=(user, pword), headers=headers, verify=False)
    if response.status_code != 200:
        data['url'] = url
        data['user'] = user
        data['response.status_code'] = str(response.status_code)
        data['Headers'] = {}
        for h in response.headers:
            data['Headers'][h] = response.headers[h]
        data['response.request.body'] = str(response.request.body)
        data['Response'] = str(response)
    else: data = response.json()
    return(json.dumps(data))

def REST_DELETE(url, headers={"Content-Type": "application/json", "Accept": "application/json"}, user='', pword=''):
    # RETURNS JSON
    data = {}
    response = requests.delete(url, auth=(user, pword), headers=headers)
    if response.status_code != 200:
        data['url'] = url
        data['user'] = user
        data['response.status_code'] = str(response.status_code)
        data['Headers'] = {}
        for h in response.headers:
            data['Headers'][h] = response.headers[h]
        data['response.request.body'] = str(response.request.body)
        data['Response'] = str(response)
    else: data = response.json()
    return(json.dumps(data))

def REST_POST(url, headers={"Content-Type": "application/json", "Accept": "application/json"}, user='', pword='', args={}):
    # RETURNS JSON
    dd = {}
    response = requests.post(url, auth=(user, pword), headers=headers, data=args)
    if response.status_code != 201:
        dd['url'] = url
        dd['user'] = user
        dd['response.status_code'] = str(response.status_code)
        dd['Headers'] = {}
        for h in response.headers:
            dd['Headers'][h] = response.headers[h]
        dd['response.request.body'] = str(response.request.body)
        dd['Response'] = str(response)
    else: dd = response.json()
    return(json.dumps(dd))

def time_epoch_human(myTime):
    # epoch = [10, 6, 3, 2]
    day = myTime // (24 * 3600)
    myTime = myTime % (24 * 3600)
    hour = myTime // 3600
    myTime %= 3600
    minutes = myTime // 60
    myTime %= 60
    seconds = myTime
    return([day, hour, minutes, seconds])

def roundMe(numm):
    return(float("{0:.2f}".format(numm)))

def fullRuntime():
    global wow_time
    timer = timer_index_since(wow_time)
    # sec = str(float("{0:.2f}".format(timer / 1000)))
    # return(sec + 'sec')
    return(str(timer) + 'ms')

# INIT
def PyVersion():
    # win/linux
    return('.'.join([str(sys.version_info[0]), str(sys.version_info[1]), str(sys.version_info[2])]))

def platform2():
    plat = {}
    plat['os'] = platform.platform()
    plat['processor'] = platform.processor()
    plat['machine'] = platform.machine()
    return(plat)

def what_server():
    if platform2()['os'].startswith('Windows'):
        return(exec2('hostname'))
    else:
        return(str(os.uname()[1]))

def whoami():
    if platform2()['os'].startswith('Windows'):
        return(exec2('whoami'))
    else:
        return(getpass.getuser())

def what_path():
    if platform2()['os'].startswith('Windows'):
        return(exec2('echo %cd%'))
    else:
        return(os.getcwd())

def add_pkgs():
    output = {}
    try:
        from pip._internal.operations import freeze
    except Exception:
        try:
                from pip.operations import freeze
        except Exception:
                return(output)
    for pkg in freeze.freeze():
        pkg = pkg.split('==')
        if pkg[0] in packages:
            output[pkg[0]] = pkg[-1]
    return(output)

def load_argv():
    global argv_dict
    argv_dict = dict()
    for user_input in sys.argv[1:]:
        if "=" not in user_input: continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1].split(',')
        if len(varvalue) == 1: varvalue = varvalue[0]
        argv_dict[varname] = varvalue
        # pairprint(varname, varvalue)

def jenkins_header():
	global argv_dict
	global wcheader
	for inp in argv_dict.keys():
		if inp.startswith('jenkins_'):
			if 'jenkins' not in wcheader.keys():
				wcheader['jenkins'] = {}
			wcheader['jenkins'][inp] = argv_dict[inp]
		else:
			wcheader[inp] = argv_dict[inp]

wait_start()
global current_time
current_time = time.time()

def header():
    global wcheader
    # current_time = time.localtime()
    return(echo_param(wcheader))

global wcheader
wcheader = {'Runtime': time.strftime(clock_format, time.localtime()), 'hostname': what_server(), 'whoami': whoami()}
wcheader['paths'] = {'pyVer': PyVersion(), 'pwd': what_path(), 'pyExec': sys.executable, 'runfile': sys.argv[0]}
wcheader['packages'] = add_pkgs() 
wcheader['platform'] = platform2()
load_argv()
wcheader['InitializingTime'] = fullRuntime()

