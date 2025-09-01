# Grading Output for Task task-1
**Device:** A-P-4 (192.168.100.108)
_Generated: 2025-08-27 15:54:02.588462_

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:39.679 UTC

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

Wed Aug 27 15:53:39.799 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-ASBR-2       Gi0/0/0/0        *PtoP*         Up    23       L2   Capable 

Total neighbor count: 1

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/1        *PtoP*         Up    25       L2   Capable 
A-P-3          Gi0/0/0/2        *PtoP*         Up    29       L2   Capable 
A-P-1          Gi0/0/0/3        *PtoP*         Up    29       L2   Capable 

Total neighbor count: 3
RP/0/RP0/CPU0:A-P-4#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:39.921 UTC

i L2 1.0.50.0/24 [115/300] via 1.0.51.1, 04:38:50, GigabitEthernet0/0/0/0
i L2 1.0.60.0/24 [115/200] via 1.0.51.1, 04:38:50, GigabitEthernet0/0/0/0
i L2 1.0.101.9/32 [115/300] via 1.0.51.1, 04:38:50, GigabitEthernet0/0/0/0
i L2 1.0.101.10/32 [115/200] via 1.0.51.1, 04:38:50, GigabitEthernet0/0/0/0
i L2 1.0.30.0/24 [115/200] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.35.1, 04:38:46, GigabitEthernet0/0/0/3
i L2 1.0.32.0/24 [115/200] via 1.0.31.1, 04:38:46, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
i L2 1.0.33.0/24 [115/200] via 1.0.31.1, 04:38:46, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.35.1, 04:38:46, GigabitEthernet0/0/0/3
i L2 1.0.70.0/24 [115/200] via 1.0.35.1, 04:38:46, GigabitEthernet0/0/0/3
i L2 1.0.71.0/24 [115/200] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
i L2 1.0.73.0/24 [115/300] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
                 [115/300] via 1.0.35.1, 04:38:46, GigabitEthernet0/0/0/3
i L2 1.0.101.6/32 [115/200] via 1.0.31.1, 04:38:50, GigabitEthernet0/0/0/1
i L2 1.0.101.7/32 [115/200] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
i L2 1.0.101.11/32 [115/200] via 1.0.35.1, 04:38:46, GigabitEthernet0/0/0/3
i L2 1.0.101.12/32 [115/200] via 1.0.34.1, 04:38:46, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:40.067 UTC

i L2 2620:fc7:1:50::/64 
      [115/400] via fe80::5054:ff:fe57:46ea, 04:38:50, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:60::/64 
      [115/300] via fe80::5054:ff:fe57:46ea, 04:38:50, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::9/128 
      [115/400] via fe80::5054:ff:fe57:46ea, 04:38:50, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::10/128 
      [115/300] via fe80::5054:ff:fe57:46ea, 04:38:50, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:30::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:46, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:32::/64 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:46, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:33::/64 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:46, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:46, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:46, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:73::/64 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee3:e3d, 04:38:46, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:feca:8b79, 04:38:50, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:fee3:e3d, 04:38:46, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fe05:dda7, 04:38:46, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

