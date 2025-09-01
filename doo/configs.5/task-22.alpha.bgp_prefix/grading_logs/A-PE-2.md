# Grading Output for Task task-22.alpha.bgp_prefix
**Device:** A-PE-2 (192.168.100.102)
_Generated: 2025-08-07 04:52:46.096371_

## show bgp vrf BLUE ipv4 unicast

```
show bgp vrf BLUE ipv4 unicast

Thu Aug  7 08:52:40.892 UTC
BGP VRF BLUE, state: Active
BGP Route Distinguisher: 100:2
VRF ID: 0x60000001
BGP router identifier 1.0.101.2, local AS number 100
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000001   RD version: 37
BGP table nexthop route policy: 
BGP main routing table version 37
BGP NSR Initial initsync version 5 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2 (default for vrf BLUE)
Route Distinguisher Version: 37
*> 10.1.1.2/32        10.10.2.2                0             0 4000 i
*>i10.1.1.4/32        1.0.101.3                2    100      0 ?
* i                   1.0.101.3                2    100      0 ?
*> 10.10.2.0/24       0.0.0.0                  0         32768 ?
*>i10.10.4.0/24       1.0.101.3                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?

Processed 4 prefixes, 6 paths
RP/0/RP0/CPU0:A-PE-2#
```

## show bgp vrf BLUE ipv6 unicast

```
show bgp vrf BLUE ipv6 unicast

Thu Aug  7 08:52:41.090 UTC
BGP VRF BLUE, state: Active
BGP Route Distinguisher: 100:2
VRF ID: 0x60000001
BGP router identifier 1.0.101.2, local AS number 100
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0800001   RD version: 33
BGP table nexthop route policy: 
BGP main routing table version 33
BGP NSR Initial initsync version 5 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2 (default for vrf BLUE)
Route Distinguisher Version: 33
*> 2620:fc7:10:102::/64
                      ::                       0         32768 ?
*>i2620:fc7:10:104::/64
                      1.0.101.3                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?
*> 2620:fc7:1011::2/128
                      2620:fc7:10:102::2
                                               0             0 4000 i
*>i2620:fc7:1011::4/128
                      1.0.101.3                1    100      0 ?
* i                   1.0.101.3                1    100      0 ?

Processed 4 prefixes, 6 paths
RP/0/RP0/CPU0:A-PE-2#
```

