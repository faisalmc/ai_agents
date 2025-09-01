# Full Output for Task task-17.charlie.ha_frr_isis/
**Device:** C-PE-3 (192.168.100.133)
_Generated: 2025-08-07 04:19:24.597377_

## show isis neighb

```
show isis neighb

Thu Aug  7 08:19:19.428 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-P-2          Gi0/0/0/0        *PtoP*         Up    22       L2   Capable 
C-PE-4         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable 
C-PE-2         Gi0/0/0/2        *PtoP*         Up    28       L2   Capable 
C-P-1          Gi0/0/0/3        *PtoP*         Up    28       L2   Capable 

Total neighbor count: 4
RP/0/RP0/CPU0:C-PE-3#
```

## show isis ipv6 route detail

```
show isis ipv6 route detail

Thu Aug  7 08:19:19.585 UTC

IS-IS CORE IPv6 Unicast routes

Codes: L1 - level 1, L2 - level 2, ia - interarea (leaked into level 1)
       df - level 1 default (closest attached router), su - summary null
       C - connected, S - static, R - RIP, B - BGP, O - OSPF
       E - EIGRP, A - access/subscriber, M - mobile, a - application
       i - IS-IS (redistributed from another instance)

Maximum parallel path count: 8

L2 2620:fc7:3:1::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.160 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     src C-P-1.00-00, 2620:fc7:3:101::5
L2 2620:fc7:3:2::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.160 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6
L2 2620:fc7:3:3::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.160 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6
     src C-P-1.00-00, 2620:fc7:3:101::5
C  2620:fc7:3:4::/64
   Installed Aug 05 08:12:59.349 for 2d00h
     is directly connected, GigabitEthernet0/0/0/3
   L2 adv [10] IS-IS interface
L2 2620:fc7:3:5::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.160 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2, SRGB Base: 16000, Weight: 0
     src C-P-1.00-00, 2620:fc7:3:101::5
     src C-PE-2.00-00, 2620:fc7:3:101::2
L2 2620:fc7:3:6::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.160 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe8b:19b8, GigabitEthernet0/0/0/1, C-PE-4, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6
     src C-PE-4.00-00, 2620:fc7:3:101::4
C  2620:fc7:3:7::/64
   Installed Aug 05 08:12:59.349 for 2d00h
     is directly connected, GigabitEthernet0/0/0/0
   L2 adv [10] IS-IS interface
L2 2620:fc7:3:8::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     src C-P-1.00-00, 2620:fc7:3:101::5
L2 2620:fc7:3:9::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2, SRGB Base: 16000, Weight: 0
     src C-PE-2.00-00, 2620:fc7:3:101::2
C  2620:fc7:3:10::/64
   Installed Aug 05 08:12:59.348 for 2d00h
     is directly connected, GigabitEthernet0/0/0/2
   L2 adv [10] IS-IS interface
L2 2620:fc7:3:11::/64 [20/115] Label: None, low priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6
     src C-PE-2.00-00, 2620:fc7:3:101::2
C  2620:fc7:3:12::/64
   Installed Aug 05 08:12:59.348 for 2d00h
     is directly connected, GigabitEthernet0/0/0/1
   L2 adv [10] IS-IS interface
L2 2620:fc7:3:101::1/128 [20/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2, SRGB Base: 16000, Weight: 0
     src C-PE-1.00-00, 2620:fc7:3:101::1
L2 2620:fc7:3:101::2/128 [10/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2, SRGB Base: 16000, Weight: 0
     src C-PE-2.00-00, 2620:fc7:3:101::2
C  2620:fc7:3:101::3/128
   Installed Aug 05 06:51:47.434 for 2d01h
     is directly connected, Loopback0
   L2 adv [0] IS-IS interface
L2 2620:fc7:3:101::4/128 [10/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fe8b:19b8, GigabitEthernet0/0/0/1, C-PE-4, SRGB Base: 16000, Weight: 0
     src C-PE-4.00-00, 2620:fc7:3:101::4
L2 2620:fc7:3:101::5/128 [10/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     src C-P-1.00-00, 2620:fc7:3:101::5
L2 2620:fc7:3:101::6/128 [10/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6
L2 2620:fc7:3:101::7/128 [20/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1, SRGB Base: 16000, Weight: 0
     src C-ASBR-1.00-00, 2620:fc7:3:101::7
L2 2620:fc7:3:101::8/128 [20/115] Label: None, low priority
   Installed Aug 07 08:18:26.656 for 00:00:53
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2, SRGB Base: 16000, Weight: 0
     src C-ASBR-2.00-00, 2620:fc7:3:101::8
L2 fc00:100:1::/48 [21/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2 tag 300, SRGB Base: 16000, Weight: 0
     src C-PE-1.00-00, 2620:fc7:3:101::1, tag 300
L2 fc00:100:2::/48 [11/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2 tag 300, SRGB Base: 16000, Weight: 0
     src C-PE-2.00-00, 2620:fc7:3:101::2, tag 300
C  fc00:100:3::/48
   Installed Aug 05 08:12:57.357 for 2d00h
     is directly connected, SRv6Locator
L2 fc00:100:4::/48 [11/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe8b:19b8, GigabitEthernet0/0/0/1, C-PE-4 tag 300, SRGB Base: 16000, Weight: 0
     src C-PE-4.00-00, 2620:fc7:3:101::4, tag 300
L2 fc00:100:5::/48 [11/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
     src C-P-1.00-00, 2620:fc7:3:101::5, tag 300
L2 fc00:100:6::/48 [11/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2 tag 300, SRGB Base: 16000, Weight: 0
     src C-P-2.00-00, 2620:fc7:3:101::6, tag 300
L2 fc00:100:7::/48 [21/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
     src C-ASBR-1.00-00, 2620:fc7:3:101::7, tag 300
L2 fc00:100:8::/48 [21/115] Label: None, critical priority
   Installed Aug 07 08:18:27.159 for 00:00:52
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2 tag 300, SRGB Base: 16000, Weight: 0
     src C-ASBR-2.00-00, 2620:fc7:3:101::8, tag 300
RP/0/RP0/CPU0:C-PE-3#
```

