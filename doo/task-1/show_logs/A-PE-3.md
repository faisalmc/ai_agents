# Full Output for Task task-1
**Device:** A-PE-3 (192.168.100.103)
_Generated: 2025-08-27 15:53:50.424297_

## show run group

```
show run group

Wed Aug 27 15:53:27.435 UTC
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

RP/0/RP0/CPU0:A-PE-3#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:27.632 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0003.00
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
   prefix-sid index 3
  !
  address-family ipv6 unicast
   prefix-sid index 1003
  !
 !
 interface GigabitEthernet0/0/0/0
 !
!

RP/0/RP0/CPU0:A-PE-3#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:27.805 UTC

IS-IS AGG1 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-PE-3#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:27.926 UTC

IS-IS AGG1 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/0        *PtoP*         Up    29       L2   Capable 

Total neighbor count: 1
RP/0/RP0/CPU0:A-PE-3#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:28.071 UTC

i L2 1.0.20.0/24 [115/400] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.21.0/24 [115/200] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.40.0/24 [115/300] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.1/32 [115/400] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.2/32 [115/300] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.6/32 [115/200] via 1.0.22.2, 6d08h, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-3#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:28.218 UTC

i L2 2620:fc7:1:20::/64 
      [115/500] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:21::/64 
      [115/300] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:40::/64 
      [115/400] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::1/128 
      [115/500] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::2/128 
      [115/400] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fe99:b62d, 6d08h, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-3#
```

