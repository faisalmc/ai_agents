# Grading Output for Task task-1
**Device:** A-P-3 (192.168.100.107)
_Generated: 2025-08-27 15:54:00.342399_

## show isis interface brief

```
show isis interface brief

Wed Aug 27 15:53:37.569 UTC

IS-IS AGG2 Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    0      2/2        2/2     Up    1500    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:A-P-3#
```

## show isis neighbors

```
show isis neighbors

Wed Aug 27 15:53:37.692 UTC

IS-IS AGG2 neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-ASBR-1       Gi0/0/0/0        *PtoP*         Up    21       L2   Capable 

Total neighbor count: 1

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
A-P-2          Gi0/0/0/3        *PtoP*         Up    29       L2   Capable 
A-P-1          Gi0/0/0/1        *PtoP*         Up    28       L2   Capable 
A-P-4          Gi0/0/0/2        *PtoP*         Up    28       L2   Capable 
A-RR-2         Gi0/0/0/4        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 4
RP/0/RP0/CPU0:A-P-3#
```

## show ip route isis

```
show ip route isis

Wed Aug 27 15:53:37.813 UTC

i L2 1.0.51.0/24 [115/300] via 1.0.50.1, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.60.0/24 [115/200] via 1.0.50.1, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.9/32 [115/200] via 1.0.50.1, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.101.10/32 [115/300] via 1.0.50.1, 6d08h, GigabitEthernet0/0/0/0
i L2 1.0.31.0/24 [115/200] via 1.0.34.2, 04:38:44, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.32.1, 04:38:44, GigabitEthernet0/0/0/3
i L2 1.0.33.0/24 [115/200] via 1.0.30.1, 08:34:31, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.32.1, 08:34:31, GigabitEthernet0/0/0/3
i L2 1.0.35.0/24 [115/200] via 1.0.30.1, 04:38:44, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.34.2, 04:38:44, GigabitEthernet0/0/0/2
i L2 1.0.70.0/24 [115/200] via 1.0.30.1, 08:34:31, GigabitEthernet0/0/0/1
i L2 1.0.73.0/24 [115/200] via 1.0.71.1, 6d08h, GigabitEthernet0/0/0/4
i L2 1.0.101.6/32 [115/200] via 1.0.32.1, 6d08h, GigabitEthernet0/0/0/3
i L2 1.0.101.8/32 [115/200] via 1.0.34.2, 04:38:44, GigabitEthernet0/0/0/2
i L2 1.0.101.11/32 [115/200] via 1.0.30.1, 6d08h, GigabitEthernet0/0/0/1
                   [115/200] via 1.0.71.1, 6d08h, GigabitEthernet0/0/0/4
i L2 1.0.101.12/32 [115/100] via 1.0.71.1, 6d08h, GigabitEthernet0/0/0/4
RP/0/RP0/CPU0:A-P-3#
```

## show route ipv6 isis

```
show route ipv6 isis

Wed Aug 27 15:53:37.959 UTC

i L2 2620:fc7:1:51::/64 
      [115/400] via fe80::5054:ff:fec8:fa60, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:60::/64 
      [115/300] via fe80::5054:ff:fec8:fa60, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::9/128 
      [115/300] via fe80::5054:ff:fec8:fa60, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::10/128 
      [115/400] via fe80::5054:ff:fec8:fa60, 6d08h, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:31::/64 
      [115/300] via fe80::5054:ff:fe20:5e65, 04:38:44, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fee1:dce4, 04:38:44, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:33::/64 
      [115/300] via fe80::5054:ff:fe92:5e25, 08:34:31, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fee1:dce4, 08:34:31, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:35::/64 
      [115/300] via fe80::5054:ff:fe92:5e25, 04:38:44, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe20:5e65, 04:38:44, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:fe92:5e25, 08:34:31, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe22:a66c, 08:34:31, GigabitEthernet0/0/0/4
i L2 2620:fc7:1:73::/64 
      [115/200] via fe80::5054:ff:fe22:a66c, 6d08h, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fee1:dce4, 6d08h, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:fe20:5e65, 04:38:44, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:fe92:5e25, 6d08h, GigabitEthernet0/0/0/1
      [115/200] via fe80::5054:ff:fe22:a66c, 6d08h, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::12/128 
      [115/100] via fe80::5054:ff:fe22:a66c, 6d08h, GigabitEthernet0/0/0/4
RP/0/RP0/CPU0:A-P-3#
```

