# Grading Output for Task task-1
**Device:** A-PE-2 (192.168.100.102)
_Generated: 2025-08-27 15:53:49.019076_

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:26.268 UTC

IS-IS AGG1 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-PE-2#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:26.388 UTC

IS-IS AGG1 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/0        *PtoP*         Up    24       L2   Capable 
A-PE-1         Gi0/0/0/2        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:A-PE-2#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:26.510 UTC

i L2 1.0.20.0/24 [115/200] via 1.0.40.1, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.22.0/24 [115/200] via 1.0.21.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.1/32 [115/200] via 1.0.40.1, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.3/32 [115/300] via 1.0.21.2, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.6/32 [115/200] via 1.0.21.2, 6d08h, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:26.657 UTC

i L2 2620:fc7:1:20::/64 
      [115/300] via fe80::5054:ff:fee2:bc15, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:22::/64 
      [115/300] via fe80::5054:ff:fee7:5424, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::1/128 
      [115/300] via fe80::5054:ff:fee2:bc15, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::3/128 
      [115/400] via fe80::5054:ff:fee7:5424, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fee7:5424, 6d08h, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-2#
```

