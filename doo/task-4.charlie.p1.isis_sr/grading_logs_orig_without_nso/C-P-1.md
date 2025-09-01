# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-P-1 (192.168.100.135)
_Generated: 2025-08-05 02:53:15.286300_

## show isis interface brief

```
show isis interface brief

Tue Aug  5 06:53:12.889 UTC

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
RP/0/RP0/CPU0:C-P-1#
```

## show isis neighbors

```
show isis neighbors

Tue Aug  5 06:53:13.012 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-2          Gi0/0/0/2        *PtoP*         Up    29       L2   Capable 
C-PE-2         Gi0/0/0/1        *PtoP*         Up    28       L2   Capable 
C-ASBR-1       Gi0/0/0/0        *PtoP*         Up    29       L2   Capable 
C-PE-3         Gi0/0/0/3        *PtoP*         Up    29       L2   Capable 
C-PE-1         Gi0/0/0/4        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 5
RP/0/RP0/CPU0:C-P-1#
```

## show ip route isis

```
show ip route isis

Tue Aug  5 06:53:13.161 UTC

i L2 3.0.101.1/32 [115/10] via 3.3.8.1, 00:00:57, GigabitEthernet0/0/0/4
i L2 3.0.101.2/32 [115/10] via 3.3.5.2, 00:00:57, GigabitEthernet0/0/0/1
i L2 3.0.101.3/32 [115/10] via 3.3.4.2, 00:00:57, GigabitEthernet0/0/0/3
i L2 3.0.101.4/32 [115/20] via 3.3.3.2, 00:00:49, GigabitEthernet0/0/0/2
                  [115/20] via 3.3.4.2, 00:00:49, GigabitEthernet0/0/0/3
i L2 3.0.101.6/32 [115/10] via 3.3.3.2, 00:00:56, GigabitEthernet0/0/0/2
i L2 3.0.101.7/32 [115/10] via 3.3.1.1, 00:00:49, GigabitEthernet0/0/0/0
i L2 3.0.101.8/32 [115/20] via 3.3.3.2, 00:00:44, GigabitEthernet0/0/0/2
i L2 3.3.2.0/24 [115/20] via 3.3.3.2, 00:00:57, GigabitEthernet0/0/0/2
i L2 3.3.6.0/24 [115/20] via 3.3.3.2, 00:00:57, GigabitEthernet0/0/0/2
i L2 3.3.7.0/24 [115/20] via 3.3.3.2, 00:00:57, GigabitEthernet0/0/0/2
                [115/20] via 3.3.4.2, 00:00:57, GigabitEthernet0/0/0/3
i L2 3.3.9.0/24 [115/20] via 3.3.5.2, 00:00:57, GigabitEthernet0/0/0/1
                [115/20] via 3.3.8.1, 00:00:57, GigabitEthernet0/0/0/4
i L2 3.3.10.0/24 [115/20] via 3.3.5.2, 00:00:57, GigabitEthernet0/0/0/1
                 [115/20] via 3.3.4.2, 00:00:57, GigabitEthernet0/0/0/3
i L2 3.3.11.0/24 [115/20] via 3.3.5.2, 00:00:57, GigabitEthernet0/0/0/1
                 [115/20] via 3.3.3.2, 00:00:57, GigabitEthernet0/0/0/2
i L2 3.3.12.0/24 [115/20] via 3.3.4.2, 00:00:57, GigabitEthernet0/0/0/3
RP/0/RP0/CPU0:C-P-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:53:13.332 UTC

i L2 2620:fc7:3:2::/64 
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:57, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:6::/64 
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:57, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:7::/64 
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:57, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:fea0:feda, 00:00:57, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:9::/64 
      [115/20] via fe80::5054:ff:fe0a:798c, 00:00:57, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe56:7033, 00:00:57, GigabitEthernet0/0/0/4
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe0a:798c, 00:00:57, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea0:feda, 00:00:57, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:fe0a:798c, 00:00:57, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:57, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:12::/64 
      [115/20] via fe80::5054:ff:fea0:feda, 00:00:57, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::1/128 
      [115/10] via fe80::5054:ff:fe56:7033, 00:00:57, GigabitEthernet0/0/0/4
i L2 2620:fc7:3:101::2/128 
      [115/10] via fe80::5054:ff:fe0a:798c, 00:00:57, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:101::3/128 
      [115/10] via fe80::5054:ff:fea0:feda, 00:00:57, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::4/128 
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:47, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:fea0:feda, 00:00:47, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::6/128 
      [115/10] via fe80::5054:ff:fe4f:facb, 00:00:57, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::7/128 
      [115/10] via fe80::5054:ff:fe6d:6ad2, 00:00:47, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::8/128 
      [115/20] via fe80::5054:ff:fe4f:facb, 00:00:42, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:C-P-1#
```

