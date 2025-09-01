# Full Output for Task task-1
**Device:** A-P-1 (192.168.100.105)
_Generated: 2025-08-27 15:53:54.881856_

## show run group

```
show run group

Wed Aug 27 15:53:32.044 UTC
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

RP/0/RP0/CPU0:A-P-1#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:32.241 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0005.00
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
   prefix-sid index 5
  !
  address-family ipv6 unicast
   prefix-sid index 1005
  !
 !
 interface GigabitEthernet0/0/0/1
 !
!
router isis CORE
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0005.00
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
   prefix-sid index 5
  !
  address-family ipv6 unicast
   prefix-sid index 1005
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/2
 !
 interface GigabitEthernet0/0/0/3
 !
 interface GigabitEthernet0/0/0/4
 !
!

RP/0/RP0/CPU0:A-P-1#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:32.437 UTC

IS-IS AGG1 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                No     -    -      0/2        0/2     Down  1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                No     -    -      0/2        0/2     Down  1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-P-1#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:32.558 UTC

IS-IS AGG1 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-PE-1         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable 

Total neighbor count: 1

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/2        *PtoP*         Up    21       L2   Capable 
A-P-3          Gi0/0/0/0        *PtoP*         Up    24       L2   Capable 
A-P-4          Gi0/0/0/3        *PtoP*         Up    25       L2   Capable 
A-RR-1         Gi0/0/0/4        *PtoP*         Up    29       L2   Capable 

Total neighbor count: 4
RP/0/RP0/CPU0:A-P-1#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:32.680 UTC

i L2 1.0.31.0/24 [115/200] via 1.0.33.2, 04:38:39, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.35.2, 04:38:39, GigabitEthernet0/0/0/3
i L2 1.0.32.0/24 [115/200] via 1.0.33.2, 6d08h, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.30.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.34.0/24 [115/200] via 1.0.35.2, 04:38:39, GigabitEthernet0/0/0/3
                 [115/200] via 1.0.30.2, 04:38:39, GigabitEthernet0/0/0/0
i L2 1.0.71.0/24 [115/200] via 1.0.30.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.73.0/24 [115/200] via 1.0.70.1, 6d08h, GigabitEthernet0/0/0/4
i L2 1.0.101.6/32 [115/200] via 1.0.33.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/200] via 1.0.30.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.8/32 [115/200] via 1.0.35.2, 04:38:39, GigabitEthernet0/0/0/3
i L2 1.0.101.11/32 [115/100] via 1.0.70.1, 6d08h, GigabitEthernet0/0/0/4
i L2 1.0.101.12/32 [115/200] via 1.0.70.1, 6d08h, GigabitEthernet0/0/0/4
                   [115/200] via 1.0.30.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.21.0/24 [115/300] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.22.0/24 [115/400] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.40.0/24 [115/200] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.1/32 [115/200] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.2/32 [115/300] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.3/32 [115/500] via 1.0.20.1, 6d08h, GigabitEthernet0/0/0/1
RP/0/RP0/CPU0:A-P-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:32.826 UTC

i L2 2620:fc7:1:31::/64 
      [115/300] via fe80::5054:ff:fe98:155c, 04:38:39, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe04:f4e0, 04:38:39, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:32::/64 
      [115/300] via fe80::5054:ff:fe98:155c, 6d08h, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee9:ff49, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:34::/64 
      [115/300] via fe80::5054:ff:fe04:f4e0, 04:38:39, GigabitEthernet0/0/0/3
      [115/300] via fe80::5054:ff:fee9:ff49, 04:38:39, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fe02:994c, 6d08h, GigabitEthernet0/0/0/4
      [115/300] via fe80::5054:ff:fee9:ff49, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:73::/64 
      [115/200] via fe80::5054:ff:fe02:994c, 6d08h, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fe98:155c, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fee9:ff49, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:fe04:f4e0, 04:38:39, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::11/128 
      [115/100] via fe80::5054:ff:fe02:994c, 6d08h, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fe02:994c, 6d08h, GigabitEthernet0/0/0/4
      [115/200] via fe80::5054:ff:fee9:ff49, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:21::/64 
      [115/400] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:22::/64 
      [115/500] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:40::/64 
      [115/300] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::1/128 
      [115/300] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::2/128 
      [115/400] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::3/128 
      [115/600] via fe80::5054:ff:feb9:879a, 6d08h, GigabitEthernet0/0/0/1
RP/0/RP0/CPU0:A-P-1#
```

