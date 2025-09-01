# Grading Output for Task task-2
**Device:** A-PE-3 (192.168.100.103)
_Generated: 2025-08-05 02:36:09.965705_

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:08.008 UTC

i L2 1.0.20.0/24 [115/400] via 1.0.22.2, 00:01:27, GigabitEthernet0/0/0/0
i L2 1.0.21.0/24 [115/200] via 1.0.22.2, 00:01:27, GigabitEthernet0/0/0/0
i L2 1.0.40.0/24 [115/300] via 1.0.22.2, 00:01:27, GigabitEthernet0/0/0/0
i L2 1.0.101.1/32 [115/400] via 1.0.22.2, 00:01:27, GigabitEthernet0/0/0/0
i L2 1.0.101.2/32 [115/300] via 1.0.22.2, 00:01:27, GigabitEthernet0/0/0/0
i L2 1.0.101.5/32 [115/500] via 1.0.22.2, 00:01:24, GigabitEthernet0/0/0/0
i L2 1.0.101.6/32 [115/200] via 1.0.22.2, 00:01:19, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-3#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:08.179 UTC

i L2 2620:fc7:1:20::/64 
      [115/500] via fe80::5054:ff:fe64:57d6, 00:01:27, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:21::/64 
      [115/300] via fe80::5054:ff:fe64:57d6, 00:01:27, GigabitEthernet0/0/0/0
i L2 2620:fc7:1:40::/64 
      [115/400] via fe80::5054:ff:fe64:57d6, 00:01:27, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::1/128 
      [115/500] via fe80::5054:ff:fe64:57d6, 00:01:27, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::2/128 
      [115/400] via fe80::5054:ff:fe64:57d6, 00:01:27, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::5/128 
      [115/600] via fe80::5054:ff:fe64:57d6, 00:01:24, GigabitEthernet0/0/0/0
i L2 2620:fc7:1001::6/128 
      [115/300] via fe80::5054:ff:fe64:57d6, 00:01:19, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:A-PE-3#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:08.354 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-PE-3#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:08.476 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-PE-3#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:08.643 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)     Gi0/0/0/0    1.0.22.2        0           
16002  16002       SR Pfx (idx 2)     Gi0/0/0/0    1.0.22.2        0           
16003  Aggregate   SR Pfx (idx 3)     default                      0           
16005  16005       SR Pfx (idx 5)     Gi0/0/0/0    1.0.22.2        0           
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/0    1.0.22.2        0           
17001  17001       SR Pfx (idx 1001)  Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
17002  17002       SR Pfx (idx 1002)  Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
17003  Aggregate   SR Pfx (idx 1003)  default                      0           
17005  17005       SR Pfx (idx 1005)  Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.22.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.22.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe64:57d6   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-3#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:08.893 UTC

IS-IS AGG1 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 3 (starts 1, restarts 2, aborts 0, finishes 1)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-PE-3#
```

