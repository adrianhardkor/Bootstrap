#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

set credentials [exec "./src/gsheet_get.py"]
puts $credentials

set ts_ip [lindex $argv 0]
set ts_user "arcadmin"
set ts_pass1 "arcaccess"
set ts_pass2 "arcenable"
set ports [mrvTS_show $ts_ip $ts_user $ts_pass1 $ts_pass2 ""]
puts $ports
exit 0

