# Full Output for Task task-10.bravo.l3vpn-pe_ce
**Device:** B-PE-1 (192.168.100.117)
_Generated: 2025-08-06 10:50:45.855362_

## show ospf vrf YELLOW neighbor

```
show ospf vrf YELLOW neighbor

Wed Aug  6 14:50:42.838 UTC

* Indicates MADJ interface
# Indicates Neighbor awaiting BFD session up

Neighbors for OSPF 100, VRF YELLOW

Neighbor ID     Pri   State           Dead Time   Address         Interface
10.2.1.1        1     FULL/DR         00:00:32    10.20.4.2       GigabitEthernet0/0/0/3
    Neighbor is up for 00:13:21

Total neighbor count: 1
RP/0/RP0/CPU0:B-PE-1#
```

## show ospf vrf YELLOW database

```
show ospf vrf YELLOW database

Wed Aug  6 14:50:43.053 UTC


            OSPF Router with ID (2.0.101.1) (Process ID 100, VRF YELLOW)

		Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
2.0.101.1       2.0.101.1       767         0x80000002 0x0056c0 1
10.2.1.1        10.2.1.1        755         0x80000004 0x00dbd0 2

		Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.20.4.2       10.2.1.1        768         0x80000001 0x002869

		Summary Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.2.1.3        2.0.101.1       763         0x80000001 0x0074cd
10.20.2.0       2.0.101.1       807         0x80000001 0x00a48e

		Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
10.2.1.2        2.0.101.1       725         0x80000001 0x0064bd 3489661128
10.20.4.0       2.0.101.1       820         0x80000001 0x006aab 0
10.20.5.0       2.0.101.1       820         0x80000001 0x005fb5 0
10.20.6.0       2.0.101.1       813         0x80000001 0x0068a4 3489661128
RP/0/RP0/CPU0:B-PE-1#
```

## show route vrf YELLOW

```
show route vrf YELLOW

Wed Aug  6 14:50:43.246 UTC

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

O    10.2.1.1/32 [110/2] via 10.20.4.2, 00:12:47, GigabitEthernet0/0/0/3
B    10.2.1.2/32 [20/0] via 10.20.5.2, 00:12:05
B    10.2.1.3/32 [200/2] via 2.0.101.3 (nexthop in vrf default), 00:12:44
B    10.20.2.0/24 [200/0] via 2.0.101.3 (nexthop in vrf default), 00:13:27
C    10.20.4.0/24 is directly connected, 00:13:41, GigabitEthernet0/0/0/3
L    10.20.4.1/32 is directly connected, 00:13:41, GigabitEthernet0/0/0/3
C    10.20.5.0/24 is directly connected, 00:13:41, GigabitEthernet0/0/0/4
L    10.20.5.1/32 is directly connected, 00:13:41, GigabitEthernet0/0/0/4
B    10.20.6.0/24 [200/0] via 2.0.101.2 (nexthop in vrf default), 00:13:33
RP/0/RP0/CPU0:B-PE-1#
```

## show bgp vpnv4 unicast vrf YELLOW

```
show bgp vpnv4 unicast vrf YELLOW

Wed Aug  6 14:50:43.482 UTC
BGP router identifier 2.0.101.1, local AS number 200
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 20
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 20
*> 10.2.1.1/32        10.20.4.2                2         32768 ?
*> 10.2.1.2/32        10.20.5.2                0             0 2000 i
*>i10.2.1.3/32        2.0.101.3                2    100      0 ?
*>i10.20.2.0/24       2.0.101.3                0    100      0 ?
*> 10.20.4.0/24       0.0.0.0                  0         32768 ?
*> 10.20.5.0/24       0.0.0.0                  0         32768 ?
*>i10.20.6.0/24       2.0.101.2                0    100      0 ?

Processed 7 prefixes, 7 paths
RP/0/RP0/CPU0:B-PE-1#
```

## show run router bgp

```
show run router bgp

Wed Aug  6 14:50:43.703 UTC
router bgp 200
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
   redistribute ospf 100
  !
  address-family ipv6 unicast
   redistribute connected
   redistribute ospfv3 200
  !
  neighbor 10.20.5.2
   remote-as 2000
   address-family ipv4 unicast
    route-policy PASS in
    route-policy PASS out
    as-override
   !
  !
  neighbor 2620:fc7:20:5::2
   remote-as 2000
   address-family ipv6 unicast
    route-policy PASS in
    route-policy PASS out
    as-override
   !
  !
 !
!

RP/0/RP0/CPU0:B-PE-1#
```

## show ip bgp neighbor brief

```
show ip bgp neighbor brief

Wed Aug  6 14:50:43.962 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
2.0.101.10        0   200                                         1d09h Established 
RP/0/RP0/CPU0:B-PE-1#
```

## show run router ospf

```
show run router ospf

Wed Aug  6 14:50:44.146 UTC
router ospf 1
 apply-group OSPF-GRP
 router-id 2.0.101.1
 mpls ldp auto-config
 redistribute connected
 area 0
  interface Loopback0
  !
  interface GigabitEthernet0/0/0/0
  !
  interface GigabitEthernet0/0/0/1
  !
  interface GigabitEthernet0/0/0/2
  !
 !
!
router ospf 100
 vrf YELLOW
  router-id 2.0.101.1
  redistribute connected
  redistribute bgp 200 route-policy PASS
  address-family ipv4 unicast
  area 0
   interface GigabitEthernet0/0/0/3
   !
  !
 !
!

RP/0/RP0/CPU0:B-PE-1#
```

## show bgp neighbor 2.0.101.10 | include Address Family

```
show bgp neighbor 2.0.101.10 | include Address Family

Wed Aug  6 14:50:44.419 UTC
 For Address Family: VPNv4 Unicast
 For Address Family: VPNv6 Unicast
RP/0/RP0/CPU0:B-PE-1#
```

