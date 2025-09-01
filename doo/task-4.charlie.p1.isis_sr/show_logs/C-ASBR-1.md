# Full Output for Task task-4.charlie.p1.isis_sr
**Device:** C-ASBR-1 (192.168.100.137)
_Generated: 2025-08-07 03:46:07.359155_

## show run group

```
show run group

Thu Aug  7 07:46:02.475 UTC
% No such configuration item(s)

RP/0/RP0/CPU0:C-ASBR-1#
```

## show run router isis

```
show run router isis

Thu Aug  7 07:46:02.734 UTC
router isis CORE
 is-type level-2-only
 net 49.1001.0003.0101.0007.00
 log adjacency changes
 address-family ipv4 unicast
  metric-style wide
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  metric-style wide
  microloop avoidance segment-routing
  segment-routing srv6
   locator CCIE_ALGO_0
    tag 300
   !
  !
 !
 interface Loopback0
  passive
  address-family ipv4 unicast
   prefix-sid index 7
  !
  address-family ipv6 unicast
  !
 !
 interface GigabitEthernet0/0/0/2
  point-to-point
  address-family ipv4 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
  address-family ipv6 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
 !
!

RP/0/RP0/CPU0:C-ASBR-1#
```

## show isis interface brief

```
show isis interface brief

Thu Aug  7 07:46:03.009 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:C-ASBR-1#
```

## show isis neighbors

```
show isis neighbors

Thu Aug  7 07:46:03.154 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-1          Gi0/0/0/2        *PtoP*         Up    24       L2   Capable 

Total neighbor count: 1
RP/0/RP0/CPU0:C-ASBR-1#
```

## show ip route isis

```
show ip route isis

Thu Aug  7 07:46:03.360 UTC

i L2 3.0.101.1/32 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.2/32 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.3/32 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.4/32 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.5/32 [115/10] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.6/32 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.8/32 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.66/32 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.2.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.3.0/24 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.4.0/24 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.5.0/24 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.6.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.7.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.8.0/24 [115/20] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.9.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.10.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.11.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.12.0/24 [115/30] via 3.3.1.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.14.0/24 [115/40] via 3.3.1.2, 00:33:27, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:C-ASBR-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Thu Aug  7 07:46:03.576 UTC

i L2 2620:fc7:3:2::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:3::/64 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:4::/64 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:5::/64 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:6::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:7::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:8::/64 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:9::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:10::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:11::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:12::/64 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::1/128 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::2/128 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::3/128 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::4/128 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::5/128 
      [115/10] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::6/128 
      [115/20] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::8/128 
      [115/30] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:1::/48 
      [115/21] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:2::/48 
      [115/21] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:3::/48 
      [115/21] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:4::/48 
      [115/31] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:5::/48 
      [115/11] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:6::/48 
      [115/21] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:8::/48 
      [115/31] via fe80::5054:ff:fe50:e7c2, 1d23h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:C-ASBR-1#
```

