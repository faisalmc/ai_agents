# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-PE-3 (192.168.100.133)
_Generated: 2025-08-05 02:53:09.493732_

## show isis interface brief

```
show isis interface brief

Tue Aug  5 06:53:06.467 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/3          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:C-PE-3#
```

## show isis neighbors

```
show isis neighbors

Tue Aug  5 06:53:06.614 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-2          Gi0/0/0/0        *PtoP*         Up    25       L2   Capable 
C-PE-4         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable 
C-PE-2         Gi0/0/0/2        *PtoP*         Up    28       L2   Capable 
C-P-1          Gi0/0/0/3        *PtoP*         Up    27       L2   Capable 

Total neighbor count: 4
RP/0/RP0/CPU0:C-PE-3#
```

## show ip route isis

```
show ip route isis

Tue Aug  5 06:53:06.770 UTC

i L2 3.0.101.1/32 [115/20] via 3.3.10.1, 00:00:48, GigabitEthernet0/0/0/2
                  [115/20] via 3.3.4.1, 00:00:48, GigabitEthernet0/0/0/3
i L2 3.0.101.2/32 [115/10] via 3.3.10.1, 00:01:05, GigabitEthernet0/0/0/2
i L2 3.0.101.4/32 [115/10] via 3.3.12.2, 00:01:05, GigabitEthernet0/0/0/1
i L2 3.0.101.5/32 [115/10] via 3.3.4.1, 00:00:53, GigabitEthernet0/0/0/3
i L2 3.0.101.6/32 [115/10] via 3.3.7.1, 00:00:48, GigabitEthernet0/0/0/0
i L2 3.0.101.7/32 [115/20] via 3.3.4.1, 00:00:43, GigabitEthernet0/0/0/3
i L2 3.0.101.8/32 [115/20] via 3.3.7.1, 00:00:38, GigabitEthernet0/0/0/0
i L2 3.3.1.0/24 [115/20] via 3.3.4.1, 00:00:53, GigabitEthernet0/0/0/3
i L2 3.3.2.0/24 [115/20] via 3.3.7.1, 00:00:48, GigabitEthernet0/0/0/0
i L2 3.3.3.0/24 [115/20] via 3.3.4.1, 00:00:48, GigabitEthernet0/0/0/3
                [115/20] via 3.3.7.1, 00:00:48, GigabitEthernet0/0/0/0
i L2 3.3.5.0/24 [115/20] via 3.3.10.1, 00:00:53, GigabitEthernet0/0/0/2
                [115/20] via 3.3.4.1, 00:00:53, GigabitEthernet0/0/0/3
i L2 3.3.6.0/24 [115/20] via 3.3.12.2, 00:00:48, GigabitEthernet0/0/0/1
                [115/20] via 3.3.7.1, 00:00:48, GigabitEthernet0/0/0/0
i L2 3.3.8.0/24 [115/20] via 3.3.4.1, 00:00:53, GigabitEthernet0/0/0/3
i L2 3.3.9.0/24 [115/20] via 3.3.10.1, 00:01:05, GigabitEthernet0/0/0/2
i L2 3.3.11.0/24 [115/20] via 3.3.10.1, 00:00:48, GigabitEthernet0/0/0/2
                 [115/20] via 3.3.7.1, 00:00:48, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-3#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:53:06.975 UTC

i L2 2620:fc7:3:1::/64 
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:58, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:2::/64 
      [115/20] via fe80::5054:ff:fec8:e10c, 00:00:53, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:3::/64 
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:53, GigabitEthernet0/0/0/3
      [115/20] via fe80::5054:ff:fec8:e10c, 00:00:53, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:5::/64 
      [115/20] via fe80::5054:ff:fe56:4116, 00:00:58, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:58, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:6::/64 
      [115/20] via fe80::5054:ff:fe8b:19b8, 00:00:53, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fec8:e10c, 00:00:53, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:8::/64 
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:58, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:9::/64 
      [115/20] via fe80::5054:ff:fe56:4116, 00:01:05, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:fe56:4116, 00:00:53, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:fec8:e10c, 00:00:53, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::1/128 
      [115/20] via fe80::5054:ff:fe56:4116, 00:00:48, GigabitEthernet0/0/0/2
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:48, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::2/128 
      [115/10] via fe80::5054:ff:fe56:4116, 00:01:05, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::4/128 
      [115/10] via fe80::5054:ff:fe8b:19b8, 00:01:05, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:101::5/128 
      [115/10] via fe80::5054:ff:fe91:6a26, 00:00:58, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::6/128 
      [115/10] via fe80::5054:ff:fec8:e10c, 00:00:48, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::7/128 
      [115/20] via fe80::5054:ff:fe91:6a26, 00:00:43, GigabitEthernet0/0/0/3
i L2 2620:fc7:3:101::8/128 
      [115/20] via fe80::5054:ff:fec8:e10c, 00:00:38, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-3#
```

