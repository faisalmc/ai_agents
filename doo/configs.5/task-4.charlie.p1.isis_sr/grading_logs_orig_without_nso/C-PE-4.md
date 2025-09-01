# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-PE-4 (192.168.100.134)
_Generated: 2025-08-05 02:53:12.522948_

## show isis interface brief

```
show isis interface brief

Tue Aug  5 06:53:09.941 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:C-PE-4#
```

## show isis neighbors

```
show isis neighbors

Tue Aug  5 06:53:10.063 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-2          Gi0/0/0/0        *PtoP*         Up    28       L2   Capable 
C-PE-3         Gi0/0/0/1        *PtoP*         Up    23       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:C-PE-4#
```

## show ip route isis

```
show ip route isis

Tue Aug  5 06:53:10.211 UTC

i L2 3.0.101.1/32 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.0.101.2/32 [115/20] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.0.101.3/32 [115/10] via 3.3.12.1, 00:01:01, GigabitEthernet0/0/0/1
i L2 3.0.101.5/32 [115/20] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.0.101.6/32 [115/10] via 3.3.6.1, 00:00:50, GigabitEthernet0/0/0/0
i L2 3.0.101.7/32 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.0.101.8/32 [115/20] via 3.3.6.1, 00:00:40, GigabitEthernet0/0/0/0
i L2 3.3.1.0/24 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.3.2.0/24 [115/20] via 3.3.6.1, 00:00:55, GigabitEthernet0/0/0/0
i L2 3.3.3.0/24 [115/20] via 3.3.6.1, 00:00:55, GigabitEthernet0/0/0/0
i L2 3.3.4.0/24 [115/20] via 3.3.12.1, 00:01:01, GigabitEthernet0/0/0/1
i L2 3.3.5.0/24 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.3.7.0/24 [115/20] via 3.3.12.1, 00:00:55, GigabitEthernet0/0/0/1
                [115/20] via 3.3.6.1, 00:00:55, GigabitEthernet0/0/0/0
i L2 3.3.8.0/24 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.3.9.0/24 [115/30] via 3.3.12.1, 00:00:45, GigabitEthernet0/0/0/1
                [115/30] via 3.3.6.1, 00:00:45, GigabitEthernet0/0/0/0
i L2 3.3.10.0/24 [115/20] via 3.3.12.1, 00:01:01, GigabitEthernet0/0/0/1
i L2 3.3.11.0/24 [115/20] via 3.3.6.1, 00:00:55, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:53:10.391 UTC

i L2 2620:fc7:3:1::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:2::/64 
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:59, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:3::/64 
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:59, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:4::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:01:01, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:5::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:7::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:00:59, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:59, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:8::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:9::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:01:01, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:59, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::1/128 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::2/128 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::3/128 
      [115/10] via fe80::5054:ff:fe8e:608a, 00:01:01, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:101::5/128 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::6/128 
      [115/10] via fe80::5054:ff:fe17:1019, 00:00:54, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::7/128 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:00:44, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:00:44, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::8/128 
      [115/20] via fe80::5054:ff:fe17:1019, 00:00:39, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-4#
```

