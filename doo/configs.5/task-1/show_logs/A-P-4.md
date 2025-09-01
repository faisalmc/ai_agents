# Full Output for Task task-1
**Device:** A-P-4 (192.168.100.108)
_Generated: 2025-08-27 15:54:01.683886_

## show run group

```
show run group

Wed Aug 27 15:53:38.781 UTC
group ISIS-GRP
 router isis '.*'
  set-overload-bit on-startup 180
  is-type level-2-only
  address-family ipv4 unicast
   metric-style wide
  !
  address-family ipv6 unicast
   metric-style wide
   single-topology
  !
  interface 'Loopback.*'
   point-to-point
   address-family ipv4 unicast
    metric 100 level 2
   !
   address-family ipv6 unicast
    metric 200 level 2
   !
  !
  interface 'GigabitEthernet.*'
   point-to-point
   address-family ipv4 unicast
    metric 100 level 2
   !
   address-family ipv6 unicast
    metric 200 level 2
   !
  !
 !
end-group

RP/0/RP0/CPU0:A-P-4#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:38.972 UTC
router isis AGG2
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0008.00
 address-family ipv4 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 interface Loopback0
  address-family ipv4 unicast
   prefix-sid index 8
  !
  address-family ipv6 unicast
   prefix-sid index 1008
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/4
 !
!
router isis CORE
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0008.00
 address-family ipv4 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 interface Loopback0
  address-family ipv4 unicast
   prefix-sid index 8
  !
  address-family ipv6 unicast
   prefix-sid index 1008
  !
 !
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/2
 !
 interface GigabitEthernet0/0/0/3
 !
!

RP/0/RP0/CPU0:A-P-4#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:39.144 UTC

IS-IS AGG2 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          No     -    -      0/2        0/2     Down  1497    -    - 

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-P-4#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:39.266 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-ASBR-2       Gi0/0/0/0        *PtoP*         Up    23       L2   Capable 

Total neighbor count: 1

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/1        *PtoP*         Up    26       L2   Capable 
A-P-3          Gi0/0/0/2        *PtoP*         Up    21       L2   Capable 
A-P-1          Gi0/0/0/3        *PtoP*         Up    29       L2   Capable 

Total neighbor count: 3
RP/0/RP0/CPU0:A-P-4#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:39.388 UTC

i L2 1.0.50.0/24 [115/300] via 1.0.51.1, 04:38:49, GigabitEthernet0/0/0/0
i L2 1.0.60.0/24 [115/200] via 1.0.51.1, 04:38:49, GigabitEthernet0/0/0/0
i L2 1.0.101.9/32 [115/300] via 1.0.51.1, 04:38:49, GigabitEthernet0/0/0/0
i L2 1.0.101.10/32 [115/200] via 1.0.51.1, 04:38:49, GigabitEthernet0/0/0/0
i L2 1.0.30.0/24 [115/200] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.35.1, 04:38:45, GigabitEthernet0/0/0/3
i L2 1.0.32.0/24 [115/200] via 1.0.31.1, 04:38:45, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
i L2 1.0.33.0/24 [115/200] via 1.0.31.1, 04:38:45, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.35.1, 04:38:45, GigabitEthernet0/0/0/3
i L2 1.0.70.0/24 [115/200] via 1.0.35.1, 04:38:45, GigabitEthernet0/0/0/3
i L2 1.0.71.0/24 [115/200] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
i L2 1.0.73.0/24 [115/300] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
                 [115/300] via 1.0.35.1, 04:38:45, GigabitEthernet0/0/0/3
i L2 1.0.101.6/32 [115/200] via 1.0.31.1, 04:38:49, GigabitEthernet0/0/0/1
i L2 1.0.101.7/32 [115/200] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
i L2 1.0.101.11/32 [115/200] via 1.0.35.1, 04:38:45, GigabitEthernet0/0/0/3
i L2 1.0.101.12/32 [115/200] via 1.0.34.1, 04:38:45, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:39.534 UTC

i L2 2620:fc7:1:50::/64 
      [115/400] via fe80::5054:ff:fe57:46ea, 04:38:49, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:60::/64 
      [115/300] via fe80::5054:ff:fe57:46ea, 04:38:49, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::9/128 
      [115/400] via fe80::5054:ff:fe57:46ea, 04:38:49, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::10/128 
      [115/300] via fe80::5054:ff:fe57:46ea, 04:38:49, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:30::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:45, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:32::/64 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:45, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:33::/64 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:45, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:45, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:45, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:73::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:45, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:49, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:fee3:e3d, 04:38:45, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fe05:dda7, 04:38:45, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

