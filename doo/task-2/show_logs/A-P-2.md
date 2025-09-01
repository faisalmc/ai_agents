# Full Output for Task task-2
**Device:** A-P-2 (192.168.100.106)
_Generated: 2025-08-05 02:36:18.481684_

## show run router isis

```
show run router isis

Tue Aug  5 06:36:15.194 UTC
router isis AGG1
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0006.00
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
   prefix-sid index 6
  !
  address-family ipv6 unicast
   prefix-sid index 1006
  !
 !
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/4
 !
!
router isis CORE
 apply-group ISIS-GRP
 net 49.0001.0001.0000.0101.0006.00
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
   prefix-sid index 6
  !
  address-family ipv6 unicast
   prefix-sid index 1006
  !
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/2
 !
 interface GigabitEthernet0/0/0/3
 !
!

RP/0/RP0/CPU0:A-P-2#
```

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:15.450 UTC

i L2 1.0.20.0/24 [115/300] via 1.0.21.1, 00:01:32, GigabitEthernet0/0/0/1
i L2 1.0.40.0/24 [115/200] via 1.0.21.1, 00:01:32, GigabitEthernet0/0/0/1
i L2 1.0.101.1/32 [115/300] via 1.0.21.1, 00:01:32, GigabitEthernet0/0/0/1
i L2 1.0.101.2/32 [115/200] via 1.0.21.1, 00:01:32, GigabitEthernet0/0/0/1
i L2 1.0.101.3/32 [115/200] via 1.0.22.1, 00:01:32, GigabitEthernet0/0/0/4
i L2 1.0.30.0/24 [115/200] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.32.2, 00:01:24, GigabitEthernet0/0/0/3
i L2 1.0.34.0/24 [115/200] via 1.0.32.2, 00:01:24, GigabitEthernet0/0/0/3
                 [115/200] via 1.0.31.2, 00:01:24, GigabitEthernet0/0/0/0
i L2 1.0.35.0/24 [115/200] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.31.2, 00:01:24, GigabitEthernet0/0/0/0
i L2 1.0.70.0/24 [115/200] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.71.0/24 [115/200] via 1.0.32.2, 00:01:24, GigabitEthernet0/0/0/3
i L2 1.0.73.0/24 [115/300] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
                 [115/300] via 1.0.32.2, 00:01:24, GigabitEthernet0/0/0/3
i L2 1.0.101.5/32 [115/200] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/200] via 1.0.32.2, 00:01:22, GigabitEthernet0/0/0/3
i L2 1.0.101.8/32 [115/200] via 1.0.31.2, 00:01:17, GigabitEthernet0/0/0/0
i L2 1.0.101.11/32 [115/200] via 1.0.33.1, 00:01:24, GigabitEthernet0/0/0/2
i L2 1.0.101.12/32 [115/200] via 1.0.32.2, 00:01:24, GigabitEthernet0/0/0/3
RP/0/RP0/CPU0:A-P-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:15.628 UTC

i L2 2620:fc7:1:20::/64 
      [115/400] via fe80::5054:ff:fec1:d6f8, 00:01:32, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:40::/64 
      [115/300] via fe80::5054:ff:fec1:d6f8, 00:01:32, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::1/128 
      [115/400] via fe80::5054:ff:fec1:d6f8, 00:01:32, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::2/128 
      [115/300] via fe80::5054:ff:fec1:d6f8, 00:01:32, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::3/128 
      [115/300] via fe80::5054:ff:fe62:5057, 00:01:32, GigabitEthernet0/0/0/4
i L2 2620:fc7:1:30::/64 
      [115/300] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe6f:621b, 00:01:24, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:34::/64 
      [115/300] via fe80::5054:ff:fe6f:621b, 00:01:24, GigabitEthernet0/0/0/3
      [115/300] via fe80::5054:ff:feea:74e3, 00:01:24, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:35::/64 
      [115/300] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:feea:74e3, 00:01:24, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:70::/64 
      [115/300] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:fe6f:621b, 00:01:24, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:73::/64 
      [115/300] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe6f:621b, 00:01:24, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::5/128 
      [115/300] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe6f:621b, 00:01:22, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:feea:74e3, 00:01:17, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::11/128 
      [115/200] via fe80::5054:ff:fe39:743b, 00:01:24, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:fe6f:621b, 00:01:24, GigabitEthernet0/0/0/3
RP/0/RP0/CPU0:A-P-2#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:15.829 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-P-2#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:15.963 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-P-2#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:16.125 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)     Gi0/0/0/1    1.0.21.1        0           
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/1    1.0.21.1        0           
16003  Pop         SR Pfx (idx 3)     Gi0/0/0/4    1.0.22.1        0           
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/2    1.0.33.1        0           
16006  Aggregate   SR Pfx (idx 6)     default                      0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/3    1.0.32.2        0           
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/0    1.0.31.2        0           
17001  17001       SR Pfx (idx 1001)  Gi0/0/0/1    fe80::5054:ff:fec1:d6f8   \
                                                                   0           
17002  Pop         SR Pfx (idx 1002)  Gi0/0/0/1    fe80::5054:ff:fec1:d6f8   \
                                                                   0           
17003  Pop         SR Pfx (idx 1003)  Gi0/0/0/4    fe80::5054:ff:fe62:5057   \
                                                                   0           
17005  Pop         SR Pfx (idx 1005)  Gi0/0/0/2    fe80::5054:ff:fe39:743b   \
                                                                   0           
17006  Aggregate   SR Pfx (idx 1006)  default                      0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/3    fe80::5054:ff:fe6f:621b   \
                                                                   0           
17008  Pop         SR Pfx (idx 1008)  Gi0/0/0/0    fe80::5054:ff:feea:74e3   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.21.1        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.21.1        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/4    1.0.22.1        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/4    1.0.22.1        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fec1:d6f8   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fec1:d6f8   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/4    fe80::5054:ff:fe62:5057   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/4    fe80::5054:ff:fe62:5057   \
                                                                   0           
24008  Pop         SR Adj (idx 1)     Gi0/0/0/3    1.0.32.2        0           
24009  Pop         SR Adj (idx 3)     Gi0/0/0/3    1.0.32.2        0           
24010  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.33.1        0           
24011  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.33.1        0           
24012  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.31.2        0           
24013  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.31.2        0           
24014  Pop         SR Adj (idx 1)     Gi0/0/0/3    fe80::5054:ff:fe6f:621b   \
                                                                   0           
24015  Pop         SR Adj (idx 3)     Gi0/0/0/3    fe80::5054:ff:fe6f:621b   \
                                                                   0           
24016  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fe39:743b   \
                                                                   0           
24017  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fe39:743b   \
                                                                   0           
24018  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:feea:74e3   \
                                                                   0           
24019  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:feea:74e3   \
                                                                   0           
RP/0/RP0/CPU0:A-P-2#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:16.486 UTC

IS-IS AGG1 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress

IS-IS CORE Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-P-2#
```

