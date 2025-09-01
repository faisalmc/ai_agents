# Grading Output for Task task-1
**Device:** A-ASBR-2 (192.168.100.110)
_Generated: 2025-08-27 15:54:10.077552_

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:47.071 UTC

IS-IS AGG2 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-ASBR-2#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:47.192 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-4          Gi0/0/0/1        *PtoP*         Up    27       L2   Capable 
A-ASBR-1       Gi0/0/0/2        *PtoP*         Up    24       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:A-ASBR-2#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:47.320 UTC

i L2 1.0.50.0/24 [115/200] via 1.0.60.1, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/300] via 1.0.60.1, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.8/32 [115/200] via 1.0.51.2, 04:38:59, GigabitEthernet0/0/0/1
i L2 1.0.101.9/32 [115/200] via 1.0.60.1, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:47.502 UTC

i L2 2620:fc7:1:50::/64 
      [115/300] via fe80::5054:ff:fee7:f63c, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/400] via fe80::5054:ff:fee7:f63c, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:feb6:3f58, 04:38:59, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::9/128 
      [115/300] via fe80::5054:ff:fee7:f63c, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-2#
```

