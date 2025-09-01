# Full Output for Task task-6.charlie.ti_lfa
**Device:** C-PE-4 (192.168.100.134)
_Generated: 2025-08-05 04:06:16.402372_

## show run router isis

```
show run router isis

Tue Aug  5 08:06:13.776 UTC
router isis CORE
 is-type level-2-only
 net 49.1001.0003.0101.0004.00
 log adjacency changes
 address-family ipv4 unicast
  metric-style wide
  microloop avoidance segment-routing
  mpls traffic-eng level-2-only
  mpls traffic-eng router-id Loopback0
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  metric-style wide
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 interface Loopback0
  passive
  address-family ipv4 unicast
   prefix-sid index 4
  !
  address-family ipv6 unicast
   prefix-sid index 1004
  !
 !
 interface Loopback66
  passive
  address-family ipv4 unicast
   prefix-sid index 41
  !
 !
 interface GigabitEthernet0/0/0/0
  point-to-point
  address-family ipv4 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
  address-family ipv6 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
 !
 interface GigabitEthernet0/0/0/1
  point-to-point
  address-family ipv4 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
  address-family ipv6 unicast
   fast-reroute per-prefix level 2
   fast-reroute per-prefix ti-lfa level 2
  !
 !
!

RP/0/RP0/CPU0:C-PE-4#
```

## show route ipv4

```
show route ipv4

Tue Aug  5 08:06:13.998 UTC

Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

Gateway of last resort is not set

i L2 3.0.101.1/32 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.0.101.2/32 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.0.101.3/32 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0 (!)
                  [115/10] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
L    3.0.101.4/32 is directly connected, 1d18h, Loopback0
i L2 3.0.101.5/32 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.0.101.6/32 [115/10] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1 (!)
i L2 3.0.101.7/32 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.0.101.8/32 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                  [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1 (!)
L    3.0.101.66/32 is directly connected, 03:26:42, Loopback66
L    3.0.101.77/32 is directly connected, 03:26:41, Loopback77
i L2 3.3.1.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.2.0/24 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1 (!)
i L2 3.3.3.0/24 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1 (!)
i L2 3.3.4.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0 (!)
                [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.5.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
C    3.3.6.0/24 is directly connected, 03:26:46, GigabitEthernet0/0/0/0
L    3.3.6.2/32 is directly connected, 03:26:46, GigabitEthernet0/0/0/0
i L2 3.3.7.0/24 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.8.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.9.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.10.0/24 [115/30] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0 (!)
                 [115/20] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1
i L2 3.3.11.0/24 [115/20] via 3.3.6.1, 00:09:19, GigabitEthernet0/0/0/0
                 [115/30] via 3.3.12.1, 00:09:19, GigabitEthernet0/0/0/1 (!)
C    3.3.12.0/24 is directly connected, 03:26:45, GigabitEthernet0/0/0/1
L    3.3.12.2/32 is directly connected, 03:26:45, GigabitEthernet0/0/0/1
C    10.13.4.0/24 is directly connected, 03:26:44, GigabitEthernet0/0/0/2
L    10.13.4.1/32 is directly connected, 03:26:44, GigabitEthernet0/0/0/2
C    192.168.100.0/24 is directly connected, 1d18h, MgmtEth0/RP0/CPU0/0
L    192.168.100.134/32 is directly connected, 1d18h, MgmtEth0/RP0/CPU0/0
RP/0/RP0/CPU0:C-PE-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 08:06:14.173 UTC

i L2 2620:fc7:3:1::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:2::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:3::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:4::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:5::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:7::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:8::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:9::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:11::/64 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::1/128 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::2/128 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::3/128 
      [115/10] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0 (!)
i L2 2620:fc7:3:101::5/128 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::6/128 
      [115/20] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1 (!)
      [115/10] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::7/128 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::8/128 
      [115/30] via fe80::5054:ff:fe8e:608a, 00:09:20, GigabitEthernet0/0/0/1 (!)
      [115/20] via fe80::5054:ff:fe17:1019, 00:09:20, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-4#
```

## show isis interface | inc "Loopback|Gigabit|FRR|LFA"

```
show isis interface | inc "Loopback|Gigabit|FRR|LFA"

Tue Aug  5 08:06:14.345 UTC
Loopback0                   Enabled
    FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled 
      FRR Type:             None               None           
    FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled 
      FRR Type:             None               None           
Loopback66                  Enabled
    FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled 
      FRR Type:             None               None           
GigabitEthernet0/0/0/0      Enabled
    FRR (L1/L2):            L1 Not Enabled     L2 Enabled     
      FRR Type:             None               per-prefix     
      Direct LFA:           Not Enabled        Enabled        
      Remote LFA:           Not Enabled        Not Enabled    
      TI LFA:               Not Enabled        Enabled        
    FRR (L1/L2):            L1 Not Enabled     L2 Enabled     
      FRR Type:             None               per-prefix     
      Direct LFA:           Not Enabled        Enabled        
      Remote LFA:           Not Enabled        Not Enabled    
      TI LFA:               Not Enabled        Enabled        
GigabitEthernet0/0/0/1      Enabled
    FRR (L1/L2):            L1 Not Enabled     L2 Enabled     
      FRR Type:             None               per-prefix     
      Direct LFA:           Not Enabled        Enabled        
      Remote LFA:           Not Enabled        Not Enabled    
      TI LFA:               Not Enabled        Enabled        
    FRR (L1/L2):            L1 Not Enabled     L2 Enabled     
      FRR Type:             None               per-prefix     
      Direct LFA:           Not Enabled        Enabled        
      Remote LFA:           Not Enabled        Not Enabled    
      TI LFA:               Not Enabled        Enabled        
RP/0/RP0/CPU0:C-PE-4#
```

## show isis fast-reroute summary

```
show isis fast-reroute summary

Tue Aug  5 08:06:14.478 UTC

IS-IS CORE IPv4 Unicast FRR summary

                          Critical   High       Medium     Low        Total     
                          Priority   Priority   Priority   Priority             
Prefixes reachable in L2
  All paths protected     0          0          7          10         17        
  Some paths protected    0          0          0          0          0         
  Unprotected             0          0          0          0          0         
  Protection coverage     0.00%      0.00%      100.00%    100.00%    100.00%   
RP/0/RP0/CPU0:C-PE-4#
```

## show isis fast-reroute detail

```
show isis fast-reroute detail

Tue Aug  5 08:06:14.587 UTC

IS-IS CORE IPv4 Unicast FRR backups

Codes: L1 - level 1, L2 - level 2, ia - interarea (leaked into level 1)
       df - level 1 default (closest attached router), su - summary null
       C - connected, S - static, R - RIP, B - BGP, O - OSPF
       E - EIGRP, A - access/subscriber, M - mobile, a - application
       i - IS-IS (redistributed from another instance)
       D - Downstream, LC - Line card disjoint, NP - Node protecting
       P - Primary path, SRLG - SRLG disjoint, TM - Total metric via backup

Maximum parallel path count: 8

L2 3.0.101.1/32 [30/115] Label: 16001, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16001, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16001, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16001, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16001, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-PE-1.00-00, 3.0.101.1
       prefix-SID index 1, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.2/32 [20/115] Label: 16002, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16002, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16002, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16002, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16002, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-PE-2.00-00, 3.0.101.2
       prefix-SID index 2, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.3/32 [10/115] Label: 16003, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.12.1, GigabitEthernet0/0/0/1, Label: ImpNull, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16003, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 20
       P: No, TM: 20, LC: No, NP: No, D: No, SRLG: Yes
     src C-PE-3.00-00, 3.0.101.3
       prefix-SID index 3, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.5/32 [20/115] Label: 16005, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16005, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16005, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16005, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16005, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-P-1.00-00, 3.0.101.5
       prefix-SID index 5, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.6/32 [10/115] Label: 16006, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: ImpNull, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16006, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 20
       P: No, TM: 20, LC: No, NP: No, D: No, SRLG: Yes
     src C-P-2.00-00, 3.0.101.6
       prefix-SID index 6, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.7/32 [30/115] Label: 16007, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16007, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16007, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16007, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16007, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-ASBR-1.00-00, 3.0.101.7
       prefix-SID index 7, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.0.101.8/32 [20/115] Label: 16008, medium priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, Label: 16008, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, Label: 16008, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-ASBR-2.00-00, 3.0.101.8
       prefix-SID index 8, R:0 N:1 P:0 E:0 V:0 L:0, Alg:0
L2 3.3.1.0/24 [30/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-P-1.00-00, 3.0.101.5
L2 3.3.2.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-P-2.00-00, 3.0.101.6
L2 3.3.3.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-P-2.00-00, 3.0.101.6
L2 3.3.4.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-PE-3.00-00, 3.0.101.3
L2 3.3.5.0/24 [30/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-P-1.00-00, 3.0.101.5
     src C-PE-2.00-00, 3.0.101.2
C  3.3.6.0/24
   Installed Aug 05 06:52:14.445 for 01:14:00
     is directly connected, GigabitEthernet0/0/0/0
   L2 RIB backup [20/115] Label: None, low priority
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       No FRR backup
     src C-P-2.00-00, 3.0.101.6
   L2 adv [10] IS-IS interface
L2 3.3.7.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 20
       P: Yes, TM: 20, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-P-2.00-00, 3.0.101.6
     src C-PE-3.00-00, 3.0.101.3
L2 3.3.8.0/24 [30/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-P-1.00-00, 3.0.101.5
L2 3.3.9.0/24 [30/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: Yes, TM: 30, LC: No, NP: Yes, D: Yes, SRLG: Yes
     src C-PE-2.00-00, 3.0.101.2
L2 3.3.10.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-PE-3.00-00, 3.0.101.3
L2 3.3.11.0/24 [20/115] Label: None, low priority
   Installed Aug 05 07:56:54.102 for 00:09:20
     via 3.3.6.1, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
       Backup path: LFA, via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0, Metric: 30
       P: No, TM: 30, LC: No, NP: No, D: No, SRLG: Yes
     src C-P-2.00-00, 3.0.101.6
C  3.3.12.0/24
   Installed Aug 05 06:52:08.879 for 01:14:06
     is directly connected, GigabitEthernet0/0/0/1
   L2 RIB backup [20/115] Label: None, low priority
     via 3.3.12.1, GigabitEthernet0/0/0/1, C-PE-3, SRGB Base: 16000, Weight: 0
       No FRR backup
     src C-PE-3.00-00, 3.0.101.3
   L2 adv [10] IS-IS interface
RP/0/RP0/CPU0:C-PE-4#
```

