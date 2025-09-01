# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-ASBR-2 (192.168.100.138)
_Generated: 2025-08-07 03:46:11.731601_

## show isis interface brief

```
show isis interface brief

Thu Aug  7 07:46:06.867 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/2          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/4          Yes    -    0      1/1        1/1     Up    1497    -    - 
RP/0/RP0/CPU0:C-ASBR-2#
```

## show isis neighbors

```
show isis neighbors

Thu Aug  7 07:46:07.014 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-2          Gi0/0/0/2        *PtoP*         Up    28       L2   Capable 

Total neighbor count: 1
RP/0/RP0/CPU0:C-ASBR-2#
```

## show ip route isis

```
show ip route isis

Thu Aug  7 07:46:07.164 UTC

i L2 3.0.101.1/32 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.2/32 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.3/32 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.4/32 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.5/32 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.6/32 [115/10] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.7/32 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.0.101.66/32 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.1.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.3.0/24 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.4.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.5.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.6.0/24 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.7.0/24 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.8.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.9.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.10.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.11.0/24 [115/20] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
i L2 3.3.12.0/24 [115/30] via 3.3.2.2, 2d00h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:C-ASBR-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Thu Aug  7 07:46:07.360 UTC

i L2 2620:fc7:3:1::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:3::/64 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:4::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:5::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:6::/64 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:7::/64 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:8::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:9::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:10::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:12::/64 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::1/128 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::2/128 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::3/128 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::4/128 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::5/128 
      [115/20] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::6/128 
      [115/10] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 2620:fc7:3:101::7/128 
      [115/30] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:1::/48 
      [115/31] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:2::/48 
      [115/21] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:3::/48 
      [115/21] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:4::/48 
      [115/21] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:5::/48 
      [115/21] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:6::/48 
      [115/11] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
i L2 fc00:100:7::/48 
      [115/31] via fe80::5054:ff:feef:75a9, 1d23h, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:C-ASBR-2#
```

