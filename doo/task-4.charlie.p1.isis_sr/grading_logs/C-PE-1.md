# Grading Output for Task task-4.charlie.p1.isis_sr
**Device:** C-PE-1 (192.168.100.131)
_Generated: 2025-08-07 03:45:43.788527_

## show isis interface brief

```
show isis interface brief

Thu Aug  7 07:45:38.902 UTC

IS-IS CORE Interfaces
    Interface      All     Adjs    Adj Topos  Adv Topos  CLNS   MTU    Prio  
                   OK    L1   L2    Run/Cfg    Run/Cfg                L1   L2
-----------------  ---  ---------  ---------  ---------  ----  ----  --------
Lo0                Yes    -    -      0/0        2/2     No       -    -    - 
Gi0/0/0/0          Yes    -    1      2/2        2/2     Up    1497    -    - 
Gi0/0/0/1          Yes    -    1      2/2        2/2     Up    1497    -    - 
RP/0/RP0/CPU0:C-PE-1#
```

## show isis neighbors

```
show isis neighbors

Thu Aug  7 07:45:39.089 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-PE-2         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable 
C-P-1          Gi0/0/0/0        *PtoP*         Up    25       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:C-PE-1#
```

## show ip route isis

```
show ip route isis

Thu Aug  7 07:45:39.273 UTC

i L2 3.0.101.2/32 [115/10] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 3.0.101.3/32 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.4/32 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.5/32 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1 (!)
                  [115/10] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.6/32 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.7/32 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1 (!)
                  [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.8/32 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.0.101.66/32 [115/30] via 3.0.101.4, 2d00h, srte_c_66_ep_3.0.101.4
i L2 3.3.1.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.2.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.3.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.4.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.5.0/24 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                [115/20] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.6.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.7.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.10.0/24 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 3.3.11.0/24 [115/20] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 3.3.12.0/24 [115/30] via 3.3.9.2, 1d23h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 1d23h, GigabitEthernet0/0/0/0
i L2 3.3.14.0/24 [115/40] via 3.3.9.2, 00:33:03, GigabitEthernet0/0/0/1
                 [115/40] via 3.3.8.2, 00:33:03, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Thu Aug  7 07:45:39.539 UTC

i L2 2620:fc7:3:1::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:2::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:3::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:4::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:5::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:6::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:7::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:12::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::2/128 
      [115/10] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:101::3/128 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::4/128 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::5/128 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/10] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::6/128 
      [115/20] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::7/128 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::8/128 
      [115/30] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:2::/48 
      [115/11] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0 (!)
i L2 fc00:100:3::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:4::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/31] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:5::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/11] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:6::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:7::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1 (!)
      [115/21] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
i L2 fc00:100:8::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 1d23h, GigabitEthernet0/0/0/1
      [115/31] via fe80::5054:ff:fea5:ba01, 1d23h, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-1#
```

## show mpls forwarding

```
show mpls forwarding

Thu Aug  7 07:45:39.736 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Aggregate   SR Pfx (idx 1)     default                      0           
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/1    3.3.9.2         284608      
       16002       SR Pfx (idx 2)     Gi0/0/0/0    3.3.8.2         0            (!)
16003  16003       SR Pfx (idx 3)     Gi0/0/0/0    3.3.8.2         0           
       16003       SR Pfx (idx 3)     Gi0/0/0/1    3.3.9.2         284667      
16004  16004       SR Pfx (idx 4)     Gi0/0/0/0    3.3.8.2         0           
       16004       SR Pfx (idx 4)     Gi0/0/0/1    3.3.9.2         284071      
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/0    3.3.8.2         0           
       16005       SR Pfx (idx 5)     Gi0/0/0/1    3.3.9.2         0            (!)
16006  16006       SR Pfx (idx 6)     Gi0/0/0/0    3.3.8.2         0           
       16006       SR Pfx (idx 6)     Gi0/0/0/1    3.3.9.2         0           
16007  16007       SR Pfx (idx 7)     Gi0/0/0/0    3.3.8.2         284090      
       16007       SR Pfx (idx 7)     Gi0/0/0/1    3.3.9.2         0            (!)
16008  16008       SR Pfx (idx 8)     Gi0/0/0/0    3.3.8.2         0           
       16008       SR Pfx (idx 8)     Gi0/0/0/1    3.3.9.2         283991      
16041  16041       SR Pfx (idx 41)    Gi0/0/0/0    3.3.8.2         0           
       16041       SR Pfx (idx 41)    Gi0/0/0/1    3.3.9.2         0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    3.3.9.2         0           
       16002       SR Adj (idx 1)     Gi0/0/0/0    3.3.8.2         0            (!)
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    3.3.9.2         0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/0    3.3.8.2         0           
       16005       SR Adj (idx 1)     Gi0/0/0/1    3.3.9.2         0            (!)
24005  Pop         SR Adj (idx 3)     Gi0/0/0/0    3.3.8.2         0           
24009  Pop         3.0.101.66/32      srte_c_66_ep 3.0.101.4       0           
24020  16006       SR TE: 1 [TE-INT]  Gi0/0/0/0    3.3.8.2         0           
       16005       SR TE: 1 [TE-INT]  Gi0/0/0/1    3.3.9.2         0            (!)
78787  Pop         No ID              srte_c_66_ep point2point     0           
RP/0/RP0/CPU0:C-PE-1#
```

## traceroute 3.0.101.4 source loopback 0

```
traceroute 3.0.101.4 source loopback 0

Thu Aug  7 07:45:39.987 UTC

Type escape sequence to abort.
Tracing the route to 3.0.101.4

 1  3.3.8.2 [MPLS: Label 16004 Exp 0] 9 msec 
    3.3.9.2 8 msec 
    3.3.8.2 9 msec 
 2  3.3.11.1 [MPLS: Label 16004 Exp 0] 26 msec 
    3.3.10.2 12 msec 
    3.3.11.1 10 msec 
 3  3.3.6.2 17 msec  *  8 msec 
RP/0/RP0/CPU0:C-PE-1#
```

