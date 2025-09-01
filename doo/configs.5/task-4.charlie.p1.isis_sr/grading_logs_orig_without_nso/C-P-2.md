# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-P-2 (192.168.100.136)
_Generated: 2025-08-05 02:53:18.239624_

## show isis interface brief

```
show isis interface brief

Tue Aug  5 06:53:15.778 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:C-P-2#
```

## show isis neighbors

```
show isis neighbors

Tue Aug  5 06:53:15.901 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-ASBR-2       Gi0/0/0/0        *PtoP*         Up    29       L2   Capable 
C-PE-4         Gi0/0/0/4        *PtoP*         Up    21       L2   Capable 
C-PE-2         Gi0/0/0/3        *PtoP*         Up    25       L2   Capable 
C-P-1          Gi0/0/0/2        *PtoP*         Up    22       L2   Capable 
C-PE-3         Gi0/0/0/1        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 5
RP/0/RP0/CPU0:C-P-2#
```

## show ip route isis

```
show ip route isis

Tue Aug  5 06:53:16.025 UTC

i L2 3.0.101.1/32 [115/20] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
                  [115/20] via 3.3.11.2, 00:00:54, GigabitEthernet0/0/0/3
i L2 3.0.101.2/32 [115/10] via 3.3.11.2, 00:00:54, GigabitEthernet0/0/0/3
i L2 3.0.101.3/32 [115/10] via 3.3.7.2, 00:00:54, GigabitEthernet0/0/0/1
i L2 3.0.101.4/32 [115/10] via 3.3.6.2, 00:00:54, GigabitEthernet0/0/0/4
i L2 3.0.101.5/32 [115/10] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
i L2 3.0.101.7/32 [115/20] via 3.3.3.1, 00:00:52, GigabitEthernet0/0/0/2
i L2 3.0.101.8/32 [115/10] via 3.3.2.1, 00:00:43, GigabitEthernet0/0/0/0
i L2 3.3.1.0/24 [115/20] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
i L2 3.3.4.0/24 [115/20] via 3.3.7.2, 00:00:54, GigabitEthernet0/0/0/1
                [115/20] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
i L2 3.3.5.0/24 [115/20] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
                [115/20] via 3.3.11.2, 00:00:54, GigabitEthernet0/0/0/3
i L2 3.3.8.0/24 [115/20] via 3.3.3.1, 00:00:54, GigabitEthernet0/0/0/2
i L2 3.3.9.0/24 [115/20] via 3.3.11.2, 00:00:54, GigabitEthernet0/0/0/3
i L2 3.3.10.0/24 [115/20] via 3.3.7.2, 00:00:54, GigabitEthernet0/0/0/1
                 [115/20] via 3.3.11.2, 00:00:54, GigabitEthernet0/0/0/3
i L2 3.3.12.0/24 [115/20] via 3.3.7.2, 00:00:54, GigabitEthernet0/0/0/1
                 [115/20] via 3.3.6.2, 00:00:54, GigabitEthernet0/0/0/4
RP/0/RP0/CPU0:C-P-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:53:16.200 UTC

i L2 2620:fc7:3:1::/64 
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:4::/64 
      [115/20] via fe80::5054:ff:fe81:70ff, 00:00:54, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:5::/64 
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:feb8:d87f, 00:00:54, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:8::/64 
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:9::/64 
      [115/20] via fe80::5054:ff:feb8:d87f, 00:00:54, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe81:70ff, 00:00:54, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:feb8:d87f, 00:00:54, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:12::/64 
      [115/20] via fe80::5054:ff:fe81:70ff, 00:00:54, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe98:c84e, 00:00:54, GigabitEthernet0/0/0/4
i L2 2620:fc7:3:101::1/128 
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:feb8:d87f, 00:00:54, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::2/128 
      [115/10] via fe80::5054:ff:feb8:d87f, 00:00:54, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::3/128 
      [115/10] via fe80::5054:ff:fe81:70ff, 00:00:54, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:101::4/128 
      [115/10] via fe80::5054:ff:fe98:c84e, 00:00:54, GigabitEthernet0/0/0/4
i L2 2620:fc7:3:101::5/128 
      [115/10] via fe80::5054:ff:fee9:b90e, 00:00:54, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::7/128 
      [115/20] via fe80::5054:ff:fee9:b90e, 00:00:52, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::8/128 
      [115/10] via fe80::5054:ff:fead:eaff, 00:00:46, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-P-2#
```

