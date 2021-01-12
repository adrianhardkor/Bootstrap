#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

global argv_array
global cred
# echo_param [array get argv_array]
cred_array argv_array
puts "\n\n\n"

# if $argv_array(lx_port) == 0: foreach loop
set ports [mrvTS $argv_array(lx_ip) $cred(LX,user) $cred(LX,pass) $cred(LX,pass15) $argv_array(lx_port)]
puts $ports
exit 0

