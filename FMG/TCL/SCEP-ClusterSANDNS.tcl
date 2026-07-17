#!
set sysstat [exec "get system status\n" "# " 15 ]
set linelist [split $sysstat \n]
foreach line $linelist {
	if {![regexp {([^:]+):(.*)} $line dummy key value]} continue
		switch -regexp -- $key {
        	Hostname {
				set hostname [string trim $value]
}}}

#Get hostname to be used in Certificate CN

set HaCluster [exec "get system ha status\n" "# " 15]
set MemberList {}
set linelist [split $HaCluster \n]
foreach line $linelist {
	if {![regexp {(.*HA cluster index.*)} $line found]} continue
		lappend MemberList $found
}
foreach member $MemberList {
	set Serials [split $member ","]
    set CleanSerial [string map {" " ""} [lindex $Serials 1]]
	lappend SerialList "DNS:${CleanSerial},\\\n"
}
set lastelement [lindex $SerialList end]
set CleanedLast [string map {"," ""} $lastelement]
set SerialList [lreplace $SerialList end end $CleanedLast]

#Sanitize and format each SN in the cluster to have its own SAN DNS required by FGFM protocol, each DNS needs \\\n because of FMG limitation, this script allows any number of SN in certreq
set Lista [join $SerialList ""]

# \\\n is required because of FMG 70 character limitation https://community.fortinet.com/fortimanager-27/technical-tip-overcoming-fortimanager-70-character-limit-for-tcl-scripts-211132

#Fields https://community.fortinet.com/fortigate-3/technical-tip-fortigate-certificate-enrollment-using-scep-with-a-specific-source-ip-176971
set scep [exec "execute vpn certificate local generate\\\n
 rsa <LocalName> <KEYSIZE>\\\n
 $hostname <Country> <State/Province>\\\n
 <City> <Org> <OU>\\\n
 \"<ADMEMAIL>\"\\\n
 $List\\\n
 <SCEPURL>\\\n
 <SCEPPASS>\\\n
 <SRCIP>" "# " 30]
#starting space character is needed between parameters, inserting it at the start of new line for better visibility instead of trailing space after \\\n
 
puts $scep


#create SCEP request and print it for logging, each field <> is exactly as needed no field can be skipped, fill with your own info, SRCIP can be deleted if not needed
