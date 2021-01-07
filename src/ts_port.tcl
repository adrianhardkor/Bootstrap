#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

set ts_ip [lindex $argv 0]
set ts_user "InReach"
set ts_pass1 "access"
set ts_pass2 "system"
set ts_port [lindex $argv 1]

set output [mrvTS $ts_ip $ts_user $ts_pass1 $ts_pass2 $ts_port {timeout 20}]
echo_param [list "Script Runtime" [timer_index_since SCRIPT]\ms]

