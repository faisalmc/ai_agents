# Full Output for Task task-9.alpha.p1.l3vpn/
**Device:** A-PE-2 (192.168.100.102)
_Generated: 2025-08-06 03:40:17.832108_

## show run router bgp

```
show run router bgp

Wed Aug  6 07:40:13.725 UTC
router bgp 100
 bgp router-id 1.0.101.2
 address-family ipv4 unicast
  network 1.0.101.2/32 route-policy SID(2)
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
  !
  address-family vpnv4 unicast
   next-hop-self
  !
  address-family vpnv6 unicast
   next-hop-self
  !
 !
 neighbor-group BLUE_CE_IPV4
  remote-as 4000
  address-family ipv4 unicast
   route-policy PASS in
   route-policy PASS out
  !
 !
 neighbor-group BLUE_CE_IPV6
  remote-as 4000
  address-family ipv6 unicast
   route-policy PASS in
   route-policy PASS out
  !
 !
 neighbor 1.0.101.5
  use neighbor-group TO_P
 !
 neighbor 1.0.101.6
  use neighbor-group TO_P
 !
 vrf BLUE
  rd 100:2
  address-family ipv4 unicast
   redistribute connected
  !
  address-family ipv6 unicast
   redistribute connected
  !
  neighbor 10.10.2.2
   use neighbor-group BLUE_CE_IPV4
  !
  neighbor 2620:fc7:10:102::2
   use neighbor-group BLUE_CE_IPV6
  !
 !
!

RP/0/RP0/CPU0:A-PE-2#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 07:40:13.924 UTC
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
*> 10.1.1.2/32        10.10.2.2                0             0 4000 i
*>i10.1.1.4/32        1.0.101.3                2    100      0 ?
* i                   1.0.101.3                2    100      0 ?
*> 10.10.2.0/24       0.0.0.0                  0         32768 ?
*>i10.10.4.0/24       1.0.101.3                0    100      0 ?
* i                   1.0.101.3                0    100      0 ?

Processed 4 prefixes, 6 paths
RP/0/RP0/CPU0:A-PE-2#
```

