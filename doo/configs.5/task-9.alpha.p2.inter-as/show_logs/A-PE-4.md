# Full Output for Task task-9.alpha.p2.inter-as
**Device:** A-PE-4 (192.168.100.104)
_Generated: 2025-08-06 04:06:58.727891_

## show run router bgp

```
show run router bgp

Wed Aug  6 08:06:54.863 UTC
router bgp 100
 bgp router-id 1.0.101.4
 address-family ipv4 unicast
  network 1.0.101.4/32 route-policy SID(4)
  allocate-label all
 !
 address-family vpnv4 unicast
 !
 address-family ipv6 unicast
 !
 address-family vpnv6 unicast
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
 neighbor-group SILVER_CE_IPV4
  remote-as 1002
  address-family ipv4 unicast
   route-policy PASS in
   route-policy PASS out
  !
 !
 neighbor-group SILVER_CE_IPV6
  remote-as 1002
  address-family ipv6 unicast
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
 vrf SILVER
  rd 100:1
  address-family ipv4 unicast
   redistribute connected
  !
  address-family ipv6 unicast
   redistribute connected
  !
  neighbor 10.10.3.2
   use neighbor-group SILVER_CE_IPV4
  !
  neighbor 2620:fc7:10:103::2
   use neighbor-group SILVER_CE_IPV6
  !
 !
!

RP/0/RP0/CPU0:A-PE-4#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 08:06:55.114 UTC
BGP router identifier 1.0.101.4, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 57
BGP NSR Initial initsync version 12 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:1 (default for vrf SILVER)
Route Distinguisher Version: 56
*>i10.1.1.1/32        1.0.101.1                0    100      0 1001 i
* i                   1.0.101.1                0    100      0 1001 i
*> 10.1.1.3/32        10.10.3.2                0             0 1002 i
*>i10.2.1.4/32        1.0.101.10                    100      0 200 1003 i
*>i10.10.1.0/24       1.0.101.1                0    100      0 ?
* i                   1.0.101.1                0    100      0 ?
*> 10.10.3.0/24       0.0.0.0                  0         32768 ?
*>i10.20.1.0/24       1.0.101.10                    100      0 200 ?
Route Distinguisher: 200:1
Route Distinguisher Version: 57
* i10.2.1.4/32        1.0.101.9                     100      0 200 1003 i
*>i                   1.0.101.10                    100      0 200 1003 i
* i10.20.1.0/24       1.0.101.9                     100      0 200 ?
*>i                   1.0.101.10                    100      0 200 ?

Processed 8 prefixes, 12 paths
RP/0/RP0/CPU0:A-PE-4#
```

