# Grading Output for Task task-9.alpha.p1.l3vpn/
**Device:** A-PE-2 (192.168.100.102)
_Generated: 2025-08-06 03:40:18.239483_

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 07:40:14.120 UTC
BGP router identifier 1.0.101.2, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 35
BGP NSR Initial initsync version 5 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2 (default for vrf BLUE)
Route Distinguisher Version: 35
<span style="background-color:red">*> 10.1.1.2/32        10.10.2.2                0             0 4000 i</span>
<span style="background-color:red">*>i10.1.1.4/32        1.0.101.3</span>                2    100      0 ?
* i                   1.0.101.3                2    100      0 ?
*> 10.10.2.0/24       0.0.0.0                  0         32768 ?
<span style="background-color:red">*>i10.10.4.0/24       1.0.101.3</span>                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?

Processed 4 prefixes, 6 paths
RP/0/RP0/CPU0:A-PE-2#
```

