# Full Output for Task task-9.alpha.p1.l3vpn/
**Device:** A-PE-3 (192.168.100.103)
_Generated: 2025-08-06 03:40:19.514404_

## show run router bgp

```
show run router bgp

Wed Aug  6 07:40:16.472 UTC
router bgp 100
 bgp router-id 1.0.101.3
 address-family ipv4 unicast
  network 1.0.101.3/32 route-policy SID(3)
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
   redistribute ospf 1 match internal external
  !
  address-family ipv6 unicast
   redistribute connected
   redistribute ospfv3 1 match internal external
  !
 !
!

RP/0/RP0/CPU0:A-PE-3#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 07:40:16.722 UTC
BGP router identifier 1.0.101.3, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 42
BGP NSR Initial initsync version 8 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2 (default for vrf BLUE)
Route Distinguisher Version: 42
*>i10.1.1.2/32        1.0.101.2                0    100      0 4000 i
* i                   1.0.101.2                0    100      0 4000 i
*> 10.1.1.4/32        10.10.4.2                2         32768 ?
*>i10.10.2.0/24       1.0.101.2                0    100      0 ?
* i                   1.0.101.2                0    100      0 ?
*> 10.10.4.0/24       0.0.0.0                  0         32768 ?

Processed 4 prefixes, 6 paths
RP/0/RP0/CPU0:A-PE-3#
```

