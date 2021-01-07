#!/usr/bin/expect
source "./lib/shared_libs/wc.tcl"
set_debug 1

proc cred_array {varName} {
  upvar 1 $varName argv_array_inside
  global cred
  array unset cred
  foreach type $argv_array_inside(User_Pass_Json) {
    set type [split $type ",/"]
    switch -- [llength $type] {
      3 {
        set cred([lindex $type 0],user) [lindex $type 1]
        set cred([lindex $type 0],pass) [lindex $type 2]
      }
      4 {
        set cred([lindex $type 0],user) [lindex $type 1]
        set cred([lindex $type 0],pass) [lindex $type 2]
        set cred([lindex $type 0],pass15) [lindex $type 3]
      }
    }
  }
}

global argv_array
global cred
cred_array argv_array
echo_param [array get argv_array]
echo_param [array get cred]
exit 0

set ts_ip [lindex $argv 0]
set ts_user "arcadmin"
set ts_pass1 "arcaccess"
set ts_pass2 "arcenable"
set ports [mrvTS_show $argv_array("lx_ip") $ts_user $ts_pass1 $ts_pass2 ""]
puts $ports
exit 0

