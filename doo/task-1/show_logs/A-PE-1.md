# Full Output for Task task-1
**Device:** A-PE-1 (192.168.100.101)
_Generated: 2025-08-27 15:53:45.758958_

## show run group

```
show run group

Wed Aug 27 15:53:22.800 UTC
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
   passive
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

RP/0/RP0/CPU0:A-PE-1#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:23.056 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0001.00
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
   prefix-sid index 1
  !
  address-family ipv6 unicast
   prefix-sid index 1001
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/2
 !
!

RP/0/RP0/CPU0:A-PE-1#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:23.295 UTC

IS-IS AGG1 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-PE-1#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:23.422 UTC

IS-IS AGG1 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-PE-2         Gi0/0/0/2        *PtoP*         Up    21       L2   Capable 
A-P-1          Gi0/0/0/0        *PtoP*         Up    27       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:A-PE-1#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:23.565 UTC

i L2 1.0.21.0/24 [115/200] via 1.0.40.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.22.0/24 [115/300] via 1.0.40.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.2/32 [115/200] via 1.0.40.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.3/32 [115/400] via 1.0.40.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.6/32 [115/300] via 1.0.40.2, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-PE-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:23.712 UTC

i L2 2620:fc7:1:21::/64 
      [115/300] via fe80::5054:ff:fea8:2a5d, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:22::/64 
      [115/400] via fe80::5054:ff:fea8:2a5d, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::2/128 
      [115/300] via fe80::5054:ff:fea8:2a5d, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::3/128 
      [115/500] via fe80::5054:ff:fea8:2a5d, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::6/128 
      [115/400] via fe80::5054:ff:fea8:2a5d, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-PE-1#
```

