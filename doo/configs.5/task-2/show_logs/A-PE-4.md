# Full Output for Task task-2
**Device:** A-PE-4 (192.168.100.104)
_Generated: 2025-08-05 02:36:11.869523_

## show run router isis

```
show run router isis

Tue Aug  5 06:36:09.106 UTC
router isis AGG2
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0004.00
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
   prefix-sid index 4
  !
  address-family ipv6 unicast
   prefix-sid index 1004
  !
 !
 interface GigabitEthernet0/0/0/0
 !
!

RP/0/RP0/CPU0:A-PE-4#
```

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:09.328 UTC

i L2 1.0.50.0/24 [115/400] via 1.0.23.2, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.51.0/24 [115/200] via 1.0.23.2, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.60.0/24 [115/300] via 1.0.23.2, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.101.7/32 [115/500] via 1.0.23.2, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.101.8/32 [115/200] via 1.0.23.2, 00:01:11, GigabitEthernet0/0/0/0
i L2 1.0.101.9/32 [115/400] via 1.0.23.2, 00:01:02, GigabitEthernet0/0/0/0
i L2 1.0.101.10/32 [115/300] via 1.0.23.2, 00:01:02, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-4#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:09.503 UTC

i L2 2620:fc7:1:50::/64 
      [115/500] via fe80::5054:ff:feb2:6e9, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:51::/64 
      [115/300] via fe80::5054:ff:feb2:6e9, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:60::/64 
      [115/400] via fe80::5054:ff:feb2:6e9, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::7/128 
      [115/600] via fe80::5054:ff:feb2:6e9, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:feb2:6e9, 00:01:11, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::9/128 
      [115/500] via fe80::5054:ff:feb2:6e9, 00:01:02, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::10/128 
      [115/400] via fe80::5054:ff:feb2:6e9, 00:01:02, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-4#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:09.673 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-PE-4#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:09.798 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-PE-4#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:09.917 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16004  Aggregate   SR Pfx (idx 4)     default                      0           
16007  16007       SR Pfx (idx 7)     Gi0/0/0/0    1.0.23.2        0           
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/0    1.0.23.2        0           
16009  16009       SR Pfx (idx 9)     Gi0/0/0/0    1.0.23.2        0           
16010  16010       SR Pfx (idx 10)    Gi0/0/0/0    1.0.23.2        0           
17004  Aggregate   SR Pfx (idx 1004)  default                      0           
17007  17007       SR Pfx (idx 1007)  Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
17008  Pop         SR Pfx (idx 1008)  Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
17009  17009       SR Pfx (idx 1009)  Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
17010  17010       SR Pfx (idx 1010)  Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.23.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.23.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:feb2:6e9   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-4#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:10.143 UTC

IS-IS AGG2 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 2 (starts 1, restarts 1, aborts 0, finishes 1)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-PE-4#
```

