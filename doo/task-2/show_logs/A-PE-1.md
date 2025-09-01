# Full Output for Task task-2
**Device:** A-PE-1 (192.168.100.101)
_Generated: 2025-08-05 02:36:02.268017_

## show run router isis

```
show run router isis

Tue Aug  5 06:35:58.950 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0001.00
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
   prefix-sid index 1
  !
  address-family ipv6 unicast
   prefix-sid index 1001
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/2
 !
!

RP/0/RP0/CPU0:A-PE-1#
```

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:35:59.170 UTC

i L2 1.0.21.0/24 [115/200] via 1.0.40.2, 00:01:25, GigabitEthernet0/0/0/2
i L2 1.0.22.0/24 [115/300] via 1.0.40.2, 00:01:25, GigabitEthernet0/0/0/2
i L2 1.0.101.2/32 [115/200] via 1.0.40.2, 00:01:25, GigabitEthernet0/0/0/2
i L2 1.0.101.3/32 [115/400] via 1.0.40.2, 00:01:25, GigabitEthernet0/0/0/2
i L2 1.0.101.5/32 [115/200] via 1.0.20.2, 00:01:18, GigabitEthernet0/0/0/0
i L2 1.0.101.6/32 [115/300] via 1.0.40.2, 00:01:13, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-PE-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:35:59.328 UTC

i L2 2620:fc7:1:21::/64 
      [115/300] via fe80::5054:ff:feb6:de61, 00:01:25, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:22::/64 
      [115/400] via fe80::5054:ff:feb6:de61, 00:01:25, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::2/128 
      [115/300] via fe80::5054:ff:feb6:de61, 00:01:25, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::3/128 
      [115/500] via fe80::5054:ff:feb6:de61, 00:01:25, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::5/128 
      [115/300] via fe80::5054:ff:fe73:d9a2, 00:01:18, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::6/128 
      [115/400] via fe80::5054:ff:feb6:de61, 00:01:13, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-PE-1#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:35:59.503 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-PE-1#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:35:59.639 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-PE-1#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:35:59.764 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Aggregate   SR Pfx (idx 1)     default                      0           
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/2    1.0.40.2        0           
16003  16003       SR Pfx (idx 3)     Gi0/0/0/2    1.0.40.2        0           
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/0    1.0.20.2        0           
16006  16006       SR Pfx (idx 6)     Gi0/0/0/2    1.0.40.2        0           
17001  Aggregate   SR Pfx (idx 1001)  default                      0           
17002  Pop         SR Pfx (idx 1002)  Gi0/0/0/2    fe80::5054:ff:feb6:de61   \
                                                                   0           
17003  17003       SR Pfx (idx 1003)  Gi0/0/0/2    fe80::5054:ff:feb6:de61   \
                                                                   0           
17005  Pop         SR Pfx (idx 1005)  Gi0/0/0/0    fe80::5054:ff:fe73:d9a2   \
                                                                   0           
17006  17006       SR Pfx (idx 1006)  Gi0/0/0/2    fe80::5054:ff:feb6:de61   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.40.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.40.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.20.2        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.20.2        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:feb6:de61   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:feb6:de61   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe73:d9a2   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe73:d9a2   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-1#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:00.038 UTC

IS-IS AGG1 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-PE-1#
```

