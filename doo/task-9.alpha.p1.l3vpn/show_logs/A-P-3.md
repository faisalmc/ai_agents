# Full Output for Task task-9.alpha.p1.l3vpn/
**Device:** A-P-3 (192.168.100.107)
_Generated: 2025-08-06 03:40:24.749380_

## show run router bgp

```
show run router bgp

Wed Aug  6 07:40:21.074 UTC
router bgp 100
 bgp router-id 1.0.101.7
 ibgp policy out enforce-modifications
 address-family ipv4 unicast
  network 1.0.101.7/32 route-policy SID(7)
  allocate-label all
 !
 address-family vpnv4 unicast
 !
 address-family ipv6 unicast
 !
 address-family vpnv6 unicast
 !
 neighbor-group RR
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
   next-hop-self
  !
  address-family vpnv4 unicast
  !
  address-family vpnv6 unicast
  !
 !
 neighbor-group RR_CLIENT
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
   next-hop-self
   route-reflector-client
  !
  address-family vpnv4 unicast
   route-reflector-client
  !
  address-family vpnv6 unicast
   route-reflector-client
  !
 !
 neighbor 1.0.101.4
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.9
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.10
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.11
  use neighbor-group RR
 !
 neighbor 1.0.101.12
  use neighbor-group RR
 !
!

RP/0/RP0/CPU0:A-P-3#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 07:40:21.324 UTC
BGP router identifier 1.0.101.7, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 22
BGP NSR Initial initsync version 5 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2
Route Distinguisher Version: 22
*>i10.1.1.2/32        1.0.101.2                0    100      0 4000 i
* i                   1.0.101.2                0    100      0 4000 i
*>i10.1.1.4/32        1.0.101.3                2    100      0 ?
* i                   1.0.101.3                2    100      0 ?
*>i10.10.2.0/24       1.0.101.2                0    100      0 ?
* i                   1.0.101.2                0    100      0 ?
*>i10.10.4.0/24       1.0.101.3                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?

Processed 4 prefixes, 8 paths
RP/0/RP0/CPU0:A-P-3#
```

