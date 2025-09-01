# Grading Output for Task task-9.alpha.p2.inter-as
**Device:** A-PE-1 (192.168.100.101)
_Generated: 2025-08-06 04:06:57.344454_

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 08:06:52.920 UTC
BGP router identifier 1.0.101.1, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 45
BGP NSR Initial initsync version 16 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:1 (default for vrf SILVER)
Route Distinguisher Version: 45
*> 10.1.1.1/32        10.10.1.2                0             0 1001 i
*>i10.1.1.3/32        1.0.101.4                0    100      0 1002 i
* i                   1.0.101.4                0    100      0 1002 i
<span style="background-color:red">*>i10.2.1.4/32        1.0.101.9                     100      0 200 1003 i</span>
*> 10.10.1.0/24       0.0.0.0                  0         32768 ?
*>i10.10.3.0/24       1.0.101.4                0    100      0 ?
* i                   1.0.101.4                0    100      0 ?
*>i10.20.1.0/24       1.0.101.9                     100      0 200 ?
Route Distinguisher: 200:1
Route Distinguisher Version: 44
*>i10.2.1.4/32        1.0.101.9                     100      0 200 1003 i
* i                   1.0.101.9                     100      0 200 1003 i
*>i10.20.1.0/24       1.0.101.9                     100      0 200 ?
* i                   1.0.101.9                     100      0 200 ?

Processed 8 prefixes, 12 paths
RP/0/RP0/CPU0:A-PE-1#
```

