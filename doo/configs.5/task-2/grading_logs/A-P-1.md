# Grading Output for Task task-2
**Device:** A-P-1 (192.168.100.105)
_Generated: 2025-08-05 02:36:16.341500_

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:12.916 UTC

i L2 1.0.31.0/24 [115/200] via 1.0.33.2, 00:01:21, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.35.2, 00:01:21, GigabitEthernet0/0/0/3
i L2 1.0.32.0/24 [115/200] via 1.0.33.2, 00:01:21, GigabitEthernet0/0/0/2
                 [115/200] via 1.0.30.2, 00:01:21, GigabitEthernet0/0/0/0
i L2 1.0.34.0/24 [115/200] via 1.0.35.2, 00:01:21, GigabitEthernet0/0/0/3
                 [115/200] via 1.0.30.2, 00:01:21, GigabitEthernet0/0/0/0
i L2 1.0.71.0/24 [115/200] via 1.0.30.2, 00:01:21, GigabitEthernet0/0/0/0
i L2 1.0.73.0/24 [115/200] via 1.0.70.1, 00:01:39, GigabitEthernet0/0/0/4
i L2 1.0.101.6/32 [115/200] via 1.0.33.2, 00:01:21, GigabitEthernet0/0/0/2
i L2 1.0.101.7/32 [115/200] via 1.0.30.2, 00:01:21, GigabitEthernet0/0/0/0
i L2 1.0.101.8/32 [115/200] via 1.0.35.2, 00:01:16, GigabitEthernet0/0/0/3
i L2 1.0.101.11/32 [115/100] via 1.0.70.1, 00:01:39, GigabitEthernet0/0/0/4
i L2 1.0.101.12/32 [115/200] via 1.0.70.1, 00:01:21, GigabitEthernet0/0/0/4
                   [115/200] via 1.0.30.2, 00:01:21, GigabitEthernet0/0/0/0
i L2 1.0.21.0/24 [115/300] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
i L2 1.0.22.0/24 [115/400] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
i L2 1.0.40.0/24 [115/200] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
i L2 1.0.101.1/32 [115/200] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
i L2 1.0.101.2/32 [115/300] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
i L2 1.0.101.3/32 [115/500] via 1.0.20.1, 00:01:36, GigabitEthernet0/0/0/1
RP/0/RP0/CPU0:A-P-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:13.091 UTC

i L2 2620:fc7:1:31::/64 
      [115/300] via fe80::5054:ff:fe04:3b13, 00:01:21, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe3b:5ec3, 00:01:21, GigabitEthernet0/0/0/3
i L2 2620:fc7:1:32::/64 
      [115/300] via fe80::5054:ff:fe04:3b13, 00:01:21, GigabitEthernet0/0/0/2
      [115/300] via fe80::5054:ff:fe95:4f6d, 00:01:21, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:34::/64 
      [115/300] via fe80::5054:ff:fe3b:5ec3, 00:01:21, GigabitEthernet0/0/0/3
      [115/300] via fe80::5054:ff:fe95:4f6d, 00:01:21, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:71::/64 
      [115/300] via fe80::5054:ff:feac:d954, 00:01:21, GigabitEthernet0/0/0/4
      [115/300] via fe80::5054:ff:fe95:4f6d, 00:01:21, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:73::/64 
      [115/200] via fe80::5054:ff:feac:d954, 00:01:36, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fe04:3b13, 00:01:21, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::7/128 
      [115/300] via fe80::5054:ff:fe95:4f6d, 00:01:21, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:fe3b:5ec3, 00:01:16, GigabitEthernet0/0/0/3
i L2 2620:fc7:1001::11/128 
      [115/100] via fe80::5054:ff:feac:d954, 00:01:36, GigabitEthernet0/0/0/4
i L2 2620:fc7:1001::12/128 
      [115/200] via fe80::5054:ff:feac:d954, 00:01:21, GigabitEthernet0/0/0/4
      [115/200] via fe80::5054:ff:fe95:4f6d, 00:01:21, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:21::/64 
      [115/400] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:22::/64 
      [115/500] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:40::/64 
      [115/300] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::1/128 
      [115/300] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::2/128 
      [115/400] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::3/128 
      [115/600] via fe80::5054:ff:fe6a:3c99, 00:01:36, GigabitEthernet0/0/0/1
RP/0/RP0/CPU0:A-P-1#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:13.287 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-P-1#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:13.416 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-P-1#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:13.568 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Pop         SR Pfx (idx 1)     Gi0/0/0/1    1.0.20.1        0           
16002  16002       SR Pfx (idx 2)     Gi0/0/0/1    1.0.20.1        0           
16003  16003       SR Pfx (idx 3)     Gi0/0/0/1    1.0.20.1        0           
16005  Aggregate   SR Pfx (idx 5)     default                      0           
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/2    1.0.33.2        0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/0    1.0.30.2        0           
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/3    1.0.35.2        0           
17001  Pop         SR Pfx (idx 1001)  Gi0/0/0/1    fe80::5054:ff:fe6a:3c99   \
                                                                   0           
17002  17002       SR Pfx (idx 1002)  Gi0/0/0/1    fe80::5054:ff:fe6a:3c99   \
                                                                   0           
17003  17003       SR Pfx (idx 1003)  Gi0/0/0/1    fe80::5054:ff:fe6a:3c99   \
                                                                   0           
17005  Aggregate   SR Pfx (idx 1005)  default                      0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/2    fe80::5054:ff:fe04:3b13   \
                                                                   0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/0    fe80::5054:ff:fe95:4f6d   \
                                                                   0           
17008  Pop         SR Pfx (idx 1008)  Gi0/0/0/3    fe80::5054:ff:fe3b:5ec3   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.20.1        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.20.1        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fe6a:3c99   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fe6a:3c99   \
                                                                   0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.33.2        0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.33.2        0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.30.2        0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.30.2        0           
24008  Pop         SR Adj (idx 1)     Gi0/0/0/3    1.0.35.2        0           
24009  Pop         SR Adj (idx 3)     Gi0/0/0/3    1.0.35.2        0           
24010  Pop         SR Adj (idx 1)     Gi0/0/0/4    1.0.70.1        0           
24011  Pop         SR Adj (idx 3)     Gi0/0/0/4    1.0.70.1        0           
24012  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fe04:3b13   \
                                                                   0           
24013  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fe04:3b13   \
                                                                   0           
24014  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe95:4f6d   \
                                                                   0           
24015  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe95:4f6d   \
                                                                   0           
24016  Pop         SR Adj (idx 1)     Gi0/0/0/3    fe80::5054:ff:fe3b:5ec3   \
                                                                   0           
24017  Pop         SR Adj (idx 3)     Gi0/0/0/3    fe80::5054:ff:fe3b:5ec3   \
                                                                   0           
24018  Pop         SR Adj (idx 1)     Gi0/0/0/4    fe80::5054:ff:feac:d954   \
                                                                   0           
24019  Pop         SR Adj (idx 3)     Gi0/0/0/4    fe80::5054:ff:feac:d954   \
                                                                   0           
RP/0/RP0/CPU0:A-P-1#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:13.942 UTC

IS-IS AGG1 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 1 (starts 1, restarts 0, aborts 0, finishes 1)
  State: no SR microloop avoidance currently in progress

IS-IS CORE Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-P-1#
```

