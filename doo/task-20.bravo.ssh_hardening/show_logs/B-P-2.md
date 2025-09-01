# Full Output for Task task-20.bravo.ssh_hardening
**Device:** B-P-2 (192.168.100.123)
_Generated: 2025-08-07 04:30:52.981679_

## show run control-plane

```
show run control-plane

Thu Aug  7 08:30:49.035 UTC
control-plane
 management-plane
  inband
   interface all
    allow SSH peer
     address ipv4 2.0.101.0/24
     address ipv4 192.168.0.0/16
     address ipv6 2001:db8:abcd::/48
    !
    allow HTTP peer
     address ipv4 127.0.0.1
    !
    allow SNMP peer
     address ipv4 2.0.101.0/24
     address ipv4 192.168.0.0/16
     address ipv6 2001:db8:abcd::/48
    !
    allow TFTP peer
     address ipv4 127.0.0.1
     address ipv6 ::1
    !
    allow Telnet peer
     address ipv4 127.0.0.1
     address ipv6 ::1
    !
   !
  !
 !
!

RP/0/RP0/CPU0:B-P-2#
```

