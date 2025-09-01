# Grading Output for Task task-9.alpha.p2.inter-as
**Device:** B-ASBR-1 (192.168.100.124)
_Generated: 2025-08-06 04:07:21.531147_

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 08:07:18.818 UTC
BGP router identifier 2.0.101.8, local AS number 200
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 27
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:1
Route Distinguisher Version: 23
<span style="background-color:red">*> 10.1.1.1/32        100.64.121.1                           0 100 1001 i</span>
<span style="background-color:red">*> 10.1.1.3/32        100.64.121.1                           0 100 1002 i</span>
*> 10.10.1.0/24       100.64.121.1                           0 100 ?
*> 10.10.3.0/24       100.64.121.1                           0 100 ?
Route Distinguisher: 100:2
Route Distinguisher Version: 6
*> 10.1.1.2/32        100.64.121.1                           0 100 4000 i
*> 10.1.1.4/32        100.64.121.1                           0 100 ?
*> 10.10.2.0/24       100.64.121.1                           0 100 ?
*> 10.10.4.0/24       100.64.121.1                           0 100 ?
Route Distinguisher: 200:1
Route Distinguisher Version: 27
<span style="background-color:red">*>i10.2.1.4/32        2.0.101.4                0    100      0 1003 i</span>
*>i10.20.1.0/24       2.0.101.4                0    100      0 ?

Processed 10 prefixes, 10 paths
RP/0/RP0/CPU0:B-ASBR-1#
```

