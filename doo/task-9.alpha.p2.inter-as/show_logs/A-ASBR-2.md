# Full Output for Task task-9.alpha.p2.inter-as
**Device:** A-ASBR-2 (192.168.100.110)
_Generated: 2025-08-06 04:07:19.151929_

## show run router bgp

```
show run router bgp

Wed Aug  6 08:07:15.278 UTC
router bgp 100
 bgp router-id 1.0.101.10
 address-family ipv4 unicast
  network 1.0.101.10/32 route-policy SID(10)
  allocate-label all
 !
 address-family vpnv4 unicast
  retain route-target all
 !
 address-family vpnv6 unicast
  retain route-target all
 !
 neighbor-group TO_P
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
   next-hop-self
   route-policy PASS in
   route-policy PASS out
  !
  address-family vpnv4 unicast
   next-hop-self
   route-policy PASS in
   route-policy PASS out
  !
  address-family vpnv6 unicast
   next-hop-self
   route-policy PASS in
   route-policy PASS out
  !
 !
 neighbor-group TO_B_ASBR
  remote-as 200
  update-source GigabitEthernet0/0/0/0
  address-family vpnv4 unicast
   route-policy PASS in
   route-policy PASS out
  !
  address-family vpnv6 unicast
   route-policy PASS in
   route-policy PASS out
  !
 !
 neighbor 1.0.101.7
  use neighbor-group TO_P
 !
 neighbor 1.0.101.8
  use neighbor-group TO_P
 !
 neighbor 100.64.122.2
  use neighbor-group TO_B_ASBR
 !
!

RP/0/RP0/CPU0:A-ASBR-2#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 08:07:15.528 UTC
BGP router identifier 1.0.101.10, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 40
BGP NSR Initial initsync version 7 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:1
Route Distinguisher Version: 35
*>i10.1.1.1/32        1.0.101.1                0    100      0 1001 i
* i                   1.0.101.1                0    100      0 1001 i
*>i10.1.1.3/32        1.0.101.4                0    100      0 1002 i
* i                   1.0.101.4                0    100      0 1002 i
*>i10.10.1.0/24       1.0.101.1                0    100      0 ?
* i                   1.0.101.1                0    100      0 ?
*>i10.10.3.0/24       1.0.101.4                0    100      0 ?
* i                   1.0.101.4                0    100      0 ?
Route Distinguisher: 100:2
Route Distinguisher Version: 6
*>i10.1.1.2/32        1.0.101.2                0    100      0 4000 i
* i                   1.0.101.2                0    100      0 4000 i
*>i10.1.1.4/32        1.0.101.3                2    100      0 ?
* i                   1.0.101.3                2    100      0 ?
*>i10.10.2.0/24       1.0.101.2                0    100      0 ?
* i                   1.0.101.2                0    100      0 ?
*>i10.10.4.0/24       1.0.101.3                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?
Route Distinguisher: 200:1
Route Distinguisher Version: 40
* i10.2.1.4/32        1.0.101.9                     100      0 200 1003 i
*>                    100.64.122.2                           0 200 1003 i
* i10.20.1.0/24       1.0.101.9                     100      0 200 ?
*>                    100.64.122.2                           0 200 ?

Processed 10 prefixes, 20 paths
RP/0/RP0/CPU0:A-ASBR-2#
```

