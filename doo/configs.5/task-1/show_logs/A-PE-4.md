# Full Output for Task task-1
**Device:** A-PE-4 (192.168.100.104)
_Generated: 2025-08-27 15:53:52.662351_

## show run group

```
show run group

Wed Aug 27 15:53:29.586 UTC
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

RP/0/RP0/CPU0:A-PE-4#
```

## show run router isis

```
show run router isis

Wed Aug 27 15:53:29.807 UTC
router isis AGG2
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0004.00
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
   prefix-sid index 4
  !
  address-family ipv6 unicast
   prefix-sid index 1004
  !
 !
 interface GigabitEthernet0/0/0/0
 !
!

RP/0/RP0/CPU0:A-PE-4#
```

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:30.004 UTC

IS-IS AGG2 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          No     -    -      0/2        0/2     Down  1497    -    - 
RP/0/RP0/CPU0:A-PE-4#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:30.125 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
RP/0/RP0/CPU0:A-PE-4#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:30.246 UTC

% No matching routes found

RP/0/RP0/CPU0:A-PE-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:30.369 UTC

% No matching routes found

RP/0/RP0/CPU0:A-PE-4#
```

