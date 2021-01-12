#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

global argv_array
global cred
# echo_param [array get argv_array]
cred_array argv_array

# if $argv_array(lx_port) == 0: foreach loop
# set ports [mrvTS_show $argv_array(lx_ip) $cred(LX,user) $cred(LX,pass) $cred(LX,pass15) "portinfohere"]
# puts $ports
# exit 0

set PORTLIST [mrvTS_getports $argv_array(lx_ip) $cred(LX,user) $cred(LX,pass) $cred(LX,pass15) $argv_array(lx_port)]

# GET STATE
foreach P $PORTLIST {
  set ports [mrvTS $argv_array(lx_ip) $cred(LX,user) $cred(LX,pass) $cred(LX,pass15) $P {tryMeCreds $argv_array}]
  # puts $ports
  puts [join [list $argv_array(lx_ip) $P [grep BAREMETAL $ports]] "    "]
}

exit 0
