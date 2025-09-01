# Full Output for Task task-11.bravo.multicast_vpn
**Device:** B-PE-4 (192.168.100.120)
_Generated: 2025-06-29 03:18:37.632669_

## show ip pim neighbor

```
show ip pim neighbor

Sun Jun 29 07:18:23.065 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.6.1*                     GigabitEthernet0/0/0/0 00:34:11  00:01:30 1           B E
2.2.6.2                      GigabitEthernet0/0/0/0 00:34:03  00:01:21 1           (DR) B
2.2.2.1                      GigabitEthernet0/0/0/2 00:34:11  00:01:26 1           B
2.2.2.2*                     GigabitEthernet0/0/0/2 00:34:11  00:01:43 1           (DR) B E
RP/0/RP0/CPU0:B-PE-4#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Sun Jun 29 07:18:23.189 UTC

PIM neighbors in VRF YELLOW
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

10.20.3.1*                   GigabitEthernet0/0/0/1 00:34:11  00:01:38 1           B E
10.20.3.2                    GigabitEthernet0/0/0/1 00:34:08  00:01:32 1           (DR) P
RP/0/RP0/CPU0:B-PE-4#
```

## show run ipv4 access-list

```
show run ipv4 access-list

Sun Jun 29 07:18:23.308 UTC
ipv4 access-list SSM
 10 permit ipv4 239.232.0.0 0.0.255.255 any
!

RP/0/RP0/CPU0:B-PE-4#
```

## show run router bgp

```
show run router bgp

Sun Jun 29 07:18:23.508 UTC
router bgp 200
 mvpn
 address-family vpnv4 unicast
 !
 address-family vpnv6 unicast
 !
 address-family ipv4 mvpn
 !
 neighbor-group IBGP-VPN
  remote-as 200
  update-source Loopback0
  address-family vpnv4 unicast
  !
  address-family vpnv6 unicast
  !
  address-family ipv4 mvpn
  !
 !
 neighbor 2.0.101.10
  use neighbor-group IBGP-VPN
 !
 vrf YELLOW
  rd 200:2
  address-family ipv4 unicast
   redistribute ospf 100
  !
  address-family ipv4 mvpn
  !
 !
!

RP/0/RP0/CPU0:B-PE-4#
```

## show run multicast-routing

```
show run multicast-routing

Sun Jun 29 07:18:23.729 UTC
multicast-routing
 address-family ipv4
  interface GigabitEthernet0/0/0/0
   enable
  !
  interface GigabitEthernet0/0/0/2
   enable
  !
 !
 vrf YELLOW
  address-family ipv4
   ! CE-facing interface
   interface GigabitEthernet0/0/0/1
    enable
   !
   mdt source Loopback0
   rate-per-route
   accounting per-prefix
   bgp auto-discovery pim
   !
   mdt default ipv4 239.232.0.1
  !
 !
!

RP/0/RP0/CPU0:B-PE-4#
```

## show run router pim

```
show run router pim

Sun Jun 29 07:18:23.925 UTC
router pim
 address-family ipv4
  interface Loopback0
   enable
  !
  interface GigabitEthernet0/0/0/0
   enable
  !
  interface GigabitEthernet0/0/0/2
   enable
  !
  ssm range SSM
 !
 vrf YELLOW
  address-family ipv4
   rpf topology route-policy CORE_TREE
   interface GigabitEthernet0/0/0/1
    enable
   !
  !
 !
!

RP/0/RP0/CPU0:B-PE-4#
```

