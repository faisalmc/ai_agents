# Full Output for Task task-14.bravo.multicast_vpn/
**Device:** B-P-2 (192.168.100.123)
_Generated: 2025-07-14 08:59:41.657338_

## show ip pim neighbor

```
show ip pim neighbor

Mon Jul 14 12:59:39.152 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.8.1                      GigabitEthernet0/0/0/0 2d01h     00:01:36 1           B
2.2.8.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:28 1           (DR) B E
2.2.4.1                      GigabitEthernet0/0/0/2 2d01h     00:01:43 1           B
2.2.4.2*                     GigabitEthernet0/0/0/2 2d01h     00:01:14 1           (DR) B E
RP/0/RP0/CPU0:B-P-2#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Mon Jul 14 12:59:39.285 UTC
No neighbors found for VRF YELLOW.
RP/0/RP0/CPU0:B-P-2#
```

## show run ipv4 access-list

```
show run ipv4 access-list

Mon Jul 14 12:59:39.410 UTC
ipv4 access-list SSM
 10 permit ipv4 239.232.0.0 0.0.255.255 any
 20 permit ipv4 232.0.0.0 0.255.255.255 any
!

RP/0/RP0/CPU0:B-P-2#
```

## show run router bgp

```
show run router bgp

Mon Jul 14 12:59:39.636 UTC
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
!

RP/0/RP0/CPU0:B-P-2#
```

## show run multicast-routing

```
show run multicast-routing

Mon Jul 14 12:59:39.859 UTC
! 20 permit ipv4 232.0.0.0 0.255.255.255 any
multicast-routing
 address-family ipv4
  interface GigabitEthernet0/0/0/0
   enable
  !
  interface GigabitEthernet0/0/0/2
   enable
  !
 !
!

RP/0/RP0/CPU0:B-P-2#
```

## show run router pim

```
show run router pim

Mon Jul 14 12:59:40.068 UTC
router pim
 address-family ipv4
  interface GigabitEthernet0/0/0/0
   enable
  !
  interface GigabitEthernet0/0/0/2
   enable
  !
  ssm range SSM
 !
!

RP/0/RP0/CPU0:B-P-2#
```

## show pim neighbor

```
show pim neighbor

Mon Jul 14 12:59:40.292 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.8.1                      GigabitEthernet0/0/0/0 2d01h     00:01:35 1           B
2.2.8.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:27 1           (DR) B E
2.2.4.1                      GigabitEthernet0/0/0/2 2d01h     00:01:41 1           B
2.2.4.2*                     GigabitEthernet0/0/0/2 2d01h     00:01:43 1           (DR) B E
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn summary

```
show bgp ipv4 mvpn summary

Mon Jul 14 12:59:40.440 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn advertised summary

```
show bgp ipv4 mvpn advertised summary

Mon Jul 14 12:59:40.603 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

```
show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

Mon Jul 14 12:59:40.747 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show pim vrf YELLOW mdt cache

```
show pim vrf YELLOW mdt cache

Mon Jul 14 12:59:40.893 UTC
No MDT Cache entries found.
RP/0/RP0/CPU0:B-P-2#
```

## show mrib vrf YELLOW route

```
show mrib vrf YELLOW route

Mon Jul 14 12:59:41.015 UTC
RP/0/RP0/CPU0:B-P-2#
```

