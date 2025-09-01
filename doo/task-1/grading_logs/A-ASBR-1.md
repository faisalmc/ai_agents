# Grading Output for Task task-1
**Device:** A-ASBR-1 (192.168.100.109)
_Generated: 2025-08-27 15:54:07.571086_

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:44.744 UTC

IS-IS AGG2 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-ASBR-1#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:44.866 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-3          Gi0/0/0/1        *PtoP*         Up    26       L2   Capable 
A-ASBR-2       Gi0/0/0/2        *PtoP*         Up    23       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:A-ASBR-1#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:44.988 UTC

i L2 1.0.51.0/24 [115/200] via 1.0.60.2, 6d08h, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/200] via 1.0.50.2, 6d08h, GigabitEthernet0/0/0/1
i L2 1.0.101.8/32 [115/300] via 1.0.60.2, 04:39:15, GigabitEthernet0/0/0/2
i L2 1.0.101.10/32 [115/200] via 1.0.60.2, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:45.144 UTC

i L2 2620:fc7:1:51::/64 
      [115/300] via fe80::5054:ff:fea0:38db, 6d08h, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe1f:6393, 6d08h, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::8/128 
      [115/400] via fe80::5054:ff:fea0:38db, 04:39:15, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::10/128 
      [115/300] via fe80::5054:ff:fea0:38db, 6d08h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-1#
```

