# Full Output for Task task-9.alpha.p2.inter-as
**Device:** B-ASBR-1 (192.168.100.124)
_Generated: 2025-08-06 04:07:21.022964_

## show run router bgp

```
show run router bgp

Wed Aug  6 08:07:18.329 UTC
router bgp 200
 address-family vpnv4 unicast
  retain route-target all
 !
 address-family vpnv6 unicast
  retain route-target all
 !
 neighbor-group IBGP-VPN
  remote-as 200
  update-source Loopback0
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
 neighbor-group TO_A_ASBR
  remote-as 100
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
 neighbor 2.0.101.10
  use neighbor-group IBGP-VPN
 !
 neighbor 100.64.121.1
  use neighbor-group TO_A_ASBR
 !
!

RP/0/RP0/CPU0:B-ASBR-1#
```

## show bgp vpnv4 unicast

```
show bgp vpnv4 unicast

Wed Aug  6 08:07:18.603 UTC
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
*> 10.1.1.1/32        100.64.121.1                           0 100 1001 i
*> 10.1.1.3/32        100.64.121.1                           0 100 1002 i
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
*>i10.2.1.4/32        2.0.101.4                0    100      0 1003 i
*>i10.20.1.0/24       2.0.101.4                0    100      0 ?

Processed 10 prefixes, 10 paths
RP/0/RP0/CPU0:B-ASBR-1#
```

