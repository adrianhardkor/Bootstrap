#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

global argv_array
global cred
echo_param [array get argv_array]
cred_array argv_array
puts "\n\n\n"
parray_slow argv_array

set ports [mrvTS_show $argv_array(lx_ip) $cred_array(LX,user) $cred_array(LX,pass) $cred_array(LX,pass15) "portinfohere"]
puts $ports
exit 0

