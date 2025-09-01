# Full Output for Task task-2
**Device:** A-ASBR-1 (192.168.100.109)
_Generated: 2025-08-05 02:36:28.948638_

## show run router isis

```
show run router isis

Tue Aug  5 06:36:26.435 UTC
router isis AGG2
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0009.00
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
   prefix-sid index 9
  !
  address-family ipv6 unicast
   prefix-sid index 1009
  !
 !
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/2
 !
!

RP/0/RP0/CPU0:A-ASBR-1#
```

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:26.764 UTC

i L2 1.0.23.0/24 [115/300] via 1.0.60.2, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.51.0/24 [115/200] via 1.0.60.2, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.101.4/32 [115/400] via 1.0.60.2, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/200] via 1.0.50.2, 00:01:24, GigabitEthernet0/0/0/1
i L2 1.0.101.8/32 [115/300] via 1.0.60.2, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.101.10/32 [115/200] via 1.0.60.2, 00:01:20, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:26.983 UTC

i L2 2620:fc7:1:23::/64 
      [115/400] via fe80::5054:ff:febc:9f43, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:51::/64 
      [115/300] via fe80::5054:ff:febc:9f43, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::4/128 
      [115/500] via fe80::5054:ff:febc:9f43, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe6b:b9a7, 00:01:24, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::8/128 
      [115/400] via fe80::5054:ff:febc:9f43, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::10/128 
      [115/300] via fe80::5054:ff:febc:9f43, 00:01:20, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-1#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:27.175 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-ASBR-1#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:27.299 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-ASBR-1#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:27.434 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16004  16004       SR Pfx (idx 4)     Gi0/0/0/2    1.0.60.2        0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/1    1.0.50.2        0           
16008  16008       SR Pfx (idx 8)     Gi0/0/0/2    1.0.60.2        0           
16009  Aggregate   SR Pfx (idx 9)     default                      0           
16010  Pop         SR Pfx (idx 10)    Gi0/0/0/2    1.0.60.2        0           
17004  17004       SR Pfx (idx 1004)  Gi0/0/0/2    fe80::5054:ff:febc:9f43   \
                                                                   0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/1    fe80::5054:ff:fe6b:b9a7   \
                                                                   0           
17008  17008       SR Pfx (idx 1008)  Gi0/0/0/2    fe80::5054:ff:febc:9f43   \
                                                                   0           
17009  Aggregate   SR Pfx (idx 1009)  default                      0           
17010  Pop         SR Pfx (idx 1010)  Gi0/0/0/2    fe80::5054:ff:febc:9f43   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.50.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.50.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.60.2        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.60.2        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fe6b:b9a7   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fe6b:b9a7   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:febc:9f43   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:febc:9f43   \
                                                                   0           
RP/0/RP0/CPU0:A-ASBR-1#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:27.782 UTC

IS-IS AGG2 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-ASBR-1#
```

