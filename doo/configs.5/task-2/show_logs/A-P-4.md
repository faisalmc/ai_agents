# Full Output for Task task-2
**Device:** A-P-4 (192.168.100.108)
_Generated: 2025-08-05 02:36:25.413991_

## show run router isis

```
show run router isis

Tue Aug  5 06:36:22.185 UTC
router isis AGG2
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0008.00
 address-family ipv4 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 interface Loopback0
  address-family ipv4 unicast
   prefix-sid index 8
  !
  address-family ipv6 unicast
   prefix-sid index 1008
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/4
 !
!
router isis CORE
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0008.00
 address-family ipv4 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 address-family ipv6 unicast
  microloop avoidance segment-routing
  segment-routing mpls sr-prefer
 !
 interface Loopback0
  address-family ipv4 unicast
   prefix-sid index 8
  !
  address-family ipv6 unicast
   prefix-sid index 1008
  !
 !
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/2
 !
 interface GigabitEthernet0/0/0/3
 !
!

RP/0/RP0/CPU0:A-P-4#
```

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:22.405 UTC

i L2 1.0.50.0/24 [115/300] via 1.0.51.1, 00:01:20, GigabitEthernet0/0/0/0
i L2 1.0.60.0/24 [115/200] via 1.0.51.1, 00:01:20, GigabitEthernet0/0/0/0
i L2 1.0.101.4/32 [115/200] via 1.0.23.1, 00:01:20, GigabitEthernet0/0/0/4
i L2 1.0.101.9/32 [115/300] via 1.0.51.1, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.101.10/32 [115/200] via 1.0.51.1, 00:01:12, GigabitEthernet0/0/0/0
i L2 1.0.30.0/24 [115/200] via 1.0.34.1, 00:01:27, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.32.0/24 [115/200] via 1.0.31.1, 00:01:27, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.34.1, 00:01:27, GigabitEthernet0/0/0/2
i L2 1.0.33.0/24 [115/200] via 1.0.31.1, 00:01:27, GigabitEthernet0/0/0/1
                 [115/200] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.70.0/24 [115/200] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.71.0/24 [115/200] via 1.0.34.1, 00:01:27, GigabitEthernet0/0/0/2
i L2 1.0.73.0/24 [115/300] via 1.0.34.1, 00:01:27, GigabitEthernet0/0/0/2
                 [115/300] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.101.5/32 [115/200] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.101.6/32 [115/200] via 1.0.31.1, 00:01:27, GigabitEthernet0/0/0/1
i L2 1.0.101.7/32 [115/200] via 1.0.34.1, 00:01:26, GigabitEthernet0/0/0/2
i L2 1.0.101.11/32 [115/200] via 1.0.35.1, 00:01:27, GigabitEthernet0/0/0/3
i L2 1.0.101.12/32 [115/200] via 1.0.34.1, 00:01:27, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:22.580 UTC

i L2 2620:fc7:1:50::/64 
      [115/400] via fe80::5054:ff:fed6:139b, 00:01:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:60::/64 
      [115/300] via fe80::5054:ff:fed6:139b, 00:01:20, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::4/128 
      [115/300] via fe80::5054:ff:fe3a:661b, 00:01:20, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::9/128 
      [115/400] via fe80::5054:ff:fed6:139b, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::10/128 
      [115/300] via fe80::5054:ff:fed6:139b, 00:01:12, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:30::/64 
      [115/300] via fe80::5054:ff:fe0c:c8dc, 00:01:27, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:32::/64 
      [115/300] via fe80::5054:ff:fe71:b16f, 00:01:27, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe0c:c8dc, 00:01:27, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:33::/64 
      [115/300] via fe80::5054:ff:fe71:b16f, 00:01:27, GigabitEthernet0/0/0/1
      [115/300] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fe0c:c8dc, 00:01:27, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:73::/64 
      [115/300] via fe80::5054:ff:fe0c:c8dc, 00:01:27, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::5/128 
      [115/300] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fe71:b16f, 00:01:27, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe0c:c8dc, 00:01:26, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:fe52:e6e6, 00:01:27, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fe0c:c8dc, 00:01:27, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-P-4#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:22.753 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-P-4#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:22.902 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-P-4#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:23.024 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16004  Pop         SR Pfx (idx 4)     Gi0/0/0/4    1.0.23.1        0           
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/3    1.0.35.1        0           
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/1    1.0.31.1        0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/2    1.0.34.1        0           
16008  Aggregate   SR Pfx (idx 8)     default                      0           
16009  16009       SR Pfx (idx 9)     Gi0/0/0/0    1.0.51.1        0           
16010  Pop         SR Pfx (idx 10)    Gi0/0/0/0    1.0.51.1        0           
17004  Pop         SR Pfx (idx 1004)  Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
17005  Pop         SR Pfx (idx 1005)  Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
17008  Aggregate   SR Pfx (idx 1008)  default                      0           
17009  17009       SR Pfx (idx 1009)  Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
17010  Pop         SR Pfx (idx 1010)  Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/4    1.0.23.1        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/4    1.0.23.1        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.51.1        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.51.1        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24008  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.31.1        0           
24009  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.31.1        0           
24010  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.34.1        0           
24011  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.34.1        0           
24012  Pop         SR Adj (idx 1)     Gi0/0/0/3    1.0.35.1        0           
24013  Pop         SR Adj (idx 3)     Gi0/0/0/3    1.0.35.1        0           
24014  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
24015  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
24016  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
24017  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
24018  Pop         SR Adj (idx 1)     Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
24019  Pop         SR Adj (idx 3)     Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
RP/0/RP0/CPU0:A-P-4#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:23.322 UTC

IS-IS AGG2 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress

IS-IS CORE Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-P-4#
```

