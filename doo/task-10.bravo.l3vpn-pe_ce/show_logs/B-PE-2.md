# Full Output for Task task-10.bravo.l3vpn-pe_ce
**Device:** B-PE-2 (192.168.100.118)
_Generated: 2025-08-06 10:50:49.619875_

## show ospf vrf YELLOW neighbor

```
show ospf vrf YELLOW neighbor

Wed Aug  6 14:50:45.764 UTC
VRF YELLOW not found in any OSPF process
RP/0/RP0/CPU0:B-PE-2#
```

## show ospf vrf YELLOW database

```
show ospf vrf YELLOW database

Wed Aug  6 14:50:45.914 UTC
VRF YELLOW not found in any OSPF process
RP/0/RP0/CPU0:B-PE-2#
```

## show route vrf YELLOW

```
show route vrf YELLOW

Wed Aug  6 14:50:46.062 UTC

Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

Gateway of last resort is not set

B    10.2.1.1/32 [200/2] via 2.0.101.1 (nexthop in vrf default), 00:12:51
B    10.2.1.2/32 [20/0] via 10.20.6.2, 00:12:09
B    10.2.1.3/32 [200/2] via 2.0.101.3 (nexthop in vrf default), 00:12:47
B    10.20.2.0/24 [200/0] via 2.0.101.3 (nexthop in vrf default), 00:13:31
B    10.20.4.0/24 [200/0] via 2.0.101.1 (nexthop in vrf default), 00:13:37
B    10.20.5.0/24 [200/0] via 2.0.101.1 (nexthop in vrf default), 00:13:37
C    10.20.6.0/24 is directly connected, 00:13:39, GigabitEthernet0/0/0/4
L    10.20.6.1/32 is directly connected, 00:13:39, GigabitEthernet0/0/0/4
RP/0/RP0/CPU0:B-PE-2#
```

## show bgp vpnv4 unicast vrf YELLOW

```
show bgp vpnv4 unicast vrf YELLOW

Wed Aug  6 14:50:46.263 UTC
BGP router identifier 2.0.101.2, local AS number 200
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 22
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 22
*>i10.2.1.1/32        2.0.101.1                2    100      0 ?
* i10.2.1.2/32        2.0.101.1                0    100      0 2000 i
*>                    10.20.6.2                0             0 2000 i
*>i10.2.1.3/32        2.0.101.3                2    100      0 ?
*>i10.20.2.0/24       2.0.101.3                0    100      0 ?
*>i10.20.4.0/24       2.0.101.1                0    100      0 ?
*>i10.20.5.0/24       2.0.101.1                0    100      0 ?
*> 10.20.6.0/24       0.0.0.0                  0         32768 ?

Processed 7 prefixes, 8 paths
RP/0/RP0/CPU0:B-PE-2#
```

## show ip bgp vrf YELLOW neighbors brief

```
show ip bgp vrf YELLOW neighbors brief

Wed Aug  6 14:50:46.486 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
10.20.6.2         0  2000                                      00:13:19 Established 
2620:fc7:20:6::2
                  0  2000                                      00:13:20 Established 
RP/0/RP0/CPU0:B-PE-2#
```

## show run router bgp

```
show run router bgp

Wed Aug  6 14:50:46.659 UTC
router bgp 200
 bgp router-id 2.0.101.2
 address-family vpnv4 unicast
 !
 address-family vpnv6 unicast
 !
 neighbor-group IBGP-VPN
  remote-as 200
  update-source Loopback0
  address-family vpnv4 unicast
  !
  address-family vpnv6 unicast
  !
 !
 neighbor 2.0.101.10
  use neighbor-group IBGP-VPN
 !
 vrf YELLOW
  rd 200:2
  address-family ipv4 unicast
   redistribute connected
  !
  address-family ipv6 unicast
   redistribute connected
  !
  neighbor 10.20.6.2
   remote-as 2000
   address-family ipv4 unicast
    route-policy PASS in
    route-policy PASS out
    as-override
   !
  !
  neighbor 2620:fc7:20:6::2
   remote-as 2000
   address-family ipv6 unicast
    route-policy PASS in
    route-policy PASS out
    as-override
   !
  !
 !
!

RP/0/RP0/CPU0:B-PE-2#
```

## show ip bgp neighbor brief

```
show ip bgp neighbor brief

Wed Aug  6 14:50:46.881 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
2.0.101.10        0   200                                         1d09h Established 
RP/0/RP0/CPU0:B-PE-2#
```

## show run router ospf

```
show run router ospf

Wed Aug  6 14:50:47.029 UTC
router ospf 1
 apply-group OSPF-GRP
 router-id 2.0.101.2
 mpls ldp auto-config
 redistribute connected
 area 0
  interface Loopback0
  !
  interface GigabitEthernet0/0/0/0
  !
  interface GigabitEthernet0/0/0/2
  !
 !
!

RP/0/RP0/CPU0:B-PE-2#
```

## show bgp neighbor 2.0.101.10 | include Address Family

```
show bgp neighbor 2.0.101.10 | include Address Family

Wed Aug  6 14:50:47.252 UTC
 For Address Family: VPNv4 Unicast
 For Address Family: VPNv6 Unicast
RP/0/RP0/CPU0:B-PE-2#
```

