#!/usr/bin/expect
source "./lib/wc.tcl"
set_debug 1

set ts_ip [lindex $argv 0]
set ts_user "arcadmin"
set ts_pass1 "arcaccess"
set ts_pass2 "arcenable"
set ts_port [lindex $argv 1]
set ports [mrvTS_show $ts_ip $ts_user $ts_pass1 $ts_pass2 ""]
puts $ports
exit 0
