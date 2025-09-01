# Full Output for Task task-1
**Device:** A-P-2 (192.168.100.106)
_Generated: 2025-08-27 15:53:57.144145_

## show run group

```
show run group

Wed Aug 27 15:53:34.099 UTC
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

RP/0/RP0/CPU0:A-P-2#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:34.321 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0006.00
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
   prefix-sid index 6
  !
  address-family ipv6 unicast
   prefix-sid index 1006
  !
 !
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/4
 !
!
router isis CORE
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0006.00
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
   prefix-sid index 6
  !
  address-family ipv6 unicast
   prefix-sid index 1006
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/2
 !
 interface GigabitEthernet0/0/0/3
 !
!

RP/0/RP0/CPU0:A-P-2#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:34.517 UTC

IS-IS AGG1 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          Yes    -    1      2/2        2/2     Up    1497    -    - 

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-P-2#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:34.638 UTC

IS-IS AGG1 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-PE-2         Gi0/0/0/1        *PtoP*         Up    27       L2   Capable 
A-PE-3         Gi0/0/0/4        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 2

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-3          Gi0/0/0/3        *PtoP*         Up    21       L2   Capable 
A-P-1          Gi0/0/0/2        *PtoP*         Up    27       L2   Capable 
A-P-4          Gi0/0/0/0        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 3
RP/0/RP0/CPU0:A-P-2#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:34.759 UTC

i L2 1.0.20.0/24 [115/300] via 1.0.21.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.40.0/24 [115/200] via 1.0.21.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.1/32 [115/300] via 1.0.21.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.2/32 [115/200] via 1.0.21.1, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.3/32 [115/200] via 1.0.22.1, 6d08h, GigabitEthernet0/0/0/4
i L2 1.0.30.0/24 [115/200] via 1.0.33.1, 08:34:28, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.32.2, 08:34:28, GigabitEthernet0/0/0/3
i L2 1.0.34.0/24 [115/200] via 1.0.32.2, 04:38:45, GigabitEthernet0/0/0/3
                 [115/200] via 1.0.31.2, 04:38:45, GigabitEthernet0/0/0/0
i L2 1.0.35.0/24 [115/200] via 1.0.33.1, 04:38:45, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.31.2, 04:38:45, GigabitEthernet0/0/0/0
i L2 1.0.70.0/24 [115/200] via 1.0.33.1, 08:34:28, GigabitEthernet0/0/0/2
i L2 1.0.71.0/24 [115/200] via 1.0.32.2, 6d08h, GigabitEthernet0/0/0/3
i L2 1.0.73.0/24 [115/300] via 1.0.33.1, 6d08h, GigabitEthernet0/0/0/2
                 [115/300] via 1.0.32.2, 6d08h, GigabitEthernet0/0/0/3
i L2 1.0.101.7/32 [115/200] via 1.0.32.2, 6d08h, GigabitEthernet0/0/0/3
i L2 1.0.101.8/32 [115/200] via 1.0.31.2, 04:38:45, GigabitEthernet0/0/0/0
i L2 1.0.101.11/32 [115/200] via 1.0.33.1, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.12/32 [115/200] via 1.0.32.2, 6d08h, GigabitEthernet0/0/0/3
RP/0/RP0/CPU0:A-P-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:34.905 UTC

i L2 2620:fc7:1:20::/64 
      [115/400] via fe80::5054:ff:fe2d:48de, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:40::/64 
      [115/300] via fe80::5054:ff:fe2d:48de, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::1/128 
      [115/400] via fe80::5054:ff:fe2d:48de, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::2/128 
      [115/300] via fe80::5054:ff:fe2d:48de, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::3/128 
      [115/300] via fe80::5054:ff:fe84:ede, 6d08h, GigabitEthernet0/0/0/4
i L2 2620:fc7:1:30::/64 
      [115/300] via fe80::5054:ff:feed:ed82, 08:34:28, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fecc:bd9e, 08:34:28, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:34::/64 
      [115/300] via fe80::5054:ff:fecc:bd9e, 04:38:46, GigabitEthernet0/0/0/3
      [115/300] via fe80::5054:ff:fee7:b3a3, 04:38:46, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:35::/64 
      [115/300] via fe80::5054:ff:feed:ed82, 04:38:46, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee7:b3a3, 04:38:46, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:feed:ed82, 08:34:28, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fecc:bd9e, 6d08h, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:73::/64 
      [115/300] via fe80::5054:ff:feed:ed82, 6d08h, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fecc:bd9e, 6d08h, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fecc:bd9e, 6d08h, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:fee7:b3a3, 04:38:46, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:feed:ed82, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fecc:bd9e, 6d08h, GigabitEthernet0/0/0/3
RP/0/RP0/CPU0:A-P-2#
```

