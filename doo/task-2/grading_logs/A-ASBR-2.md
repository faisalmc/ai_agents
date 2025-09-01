# Grading Output for Task task-2
**Device:** A-ASBR-2 (192.168.100.110)
_Generated: 2025-08-05 02:36:34.766368_

## show route ipv4 isis

```
show route ipv4 isis

Tue Aug  5 06:36:31.989 UTC

i L2 1.0.23.0/24 [115/200] via 1.0.51.2, 00:01:26, GigabitEthernet0/0/0/1
i L2 1.0.50.0/24 [115/200] via 1.0.60.1, 00:01:26, GigabitEthernet0/0/0/2
i L2 1.0.101.4/32 [115/300] via 1.0.51.2, 00:01:26, GigabitEthernet0/0/0/1
i L2 1.0.101.7/32 [115/300] via 1.0.60.1, 00:01:26, GigabitEthernet0/0/0/2
i L2 1.0.101.8/32 [115/200] via 1.0.51.2, 00:01:26, GigabitEthernet0/0/0/1
i L2 1.0.101.9/32 [115/200] via 1.0.60.1, 00:01:25, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-2#
```

## show route ipv6 isis

```
show route ipv6 isis

Tue Aug  5 06:36:32.194 UTC

i L2 2620:fc7:1:23::/64 
      [115/300] via fe80::5054:ff:feff:5d51, 00:01:26, GigabitEthernet0/0/0/1
i L2 2620:fc7:1:50::/64 
      [115/300] via fe80::5054:ff:fedf:334d, 00:01:26, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::4/128 
      [115/400] via fe80::5054:ff:feff:5d51, 00:01:26, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::7/128 
      [115/400] via fe80::5054:ff:fedf:334d, 00:01:26, GigabitEthernet0/0/0/2
i L2 2620:fc7:1001::8/128 
      [115/300] via fe80::5054:ff:feff:5d51, 00:01:26, GigabitEthernet0/0/0/1
i L2 2620:fc7:1001::9/128 
      [115/300] via fe80::5054:ff:fedf:334d, 00:01:25, GigabitEthernet0/0/0/2
RP/0/RP0/CPU0:A-ASBR-2#
```

## show mpls lsd private | inc SRLB

```
show mpls lsd private | inc SRLB

Tue Aug  5 06:36:32.399 UTC
SRLB Lbl Mgr:
   Current Active SRLB block      = [25000, 26000] 
   Configured Pending SRLB block  = [0, 0] 
RP/0/RP0/CPU0:A-ASBR-2#
```

## show mpls label table detail private | inc "SRLB|SRGB"

```
show mpls label table detail private | inc "SRLB|SRGB"

Tue Aug  5 06:36:32.532 UTC
  (Lbl-blk SRGB, vers:0, (start_label=16000, size=8000)
  (Lbl-blk SRLB, vers:0, (start_label=25000, size=1001, app_notify=0)
RP/0/RP0/CPU0:A-ASBR-2#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:36:32.703 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16004  16004       SR Pfx (idx 4)     Gi0/0/0/1    1.0.51.2        0           
16007  16007       SR Pfx (idx 7)     Gi0/0/0/2    1.0.60.1        0           
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/1    1.0.51.2        0           
16009  Pop         SR Pfx (idx 9)     Gi0/0/0/2    1.0.60.1        0           
16010  Aggregate   SR Pfx (idx 10)    default                      0           
17004  17004       SR Pfx (idx 1004)  Gi0/0/0/1    fe80::5054:ff:feff:5d51   \
                                                                   0           
17007  17007       SR Pfx (idx 1007)  Gi0/0/0/2    fe80::5054:ff:fedf:334d   \
                                                                   0           
17008  Pop         SR Pfx (idx 1008)  Gi0/0/0/1    fe80::5054:ff:feff:5d51   \
                                                                   0           
17009  Pop         SR Pfx (idx 1009)  Gi0/0/0/2    fe80::5054:ff:fedf:334d   \
                                                                   0           
17010  Aggregate   SR Pfx (idx 1010)  default                      0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.51.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.51.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.60.1        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.60.1        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:feff:5d51   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:feff:5d51   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fedf:334d   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fedf:334d   \
                                                                   0           
RP/0/RP0/CPU0:A-ASBR-2#
```

## show isis ipv4 microloop avoidance

```
show isis ipv4 microloop avoidance

Tue Aug  5 06:36:32.999 UTC

IS-IS AGG2 Level-2, IPv4 Unicast, Microloop Avoidance Statistics:
  Microloop avoidance: enabled, type: Segment Routing, RIB update delay: 5000 msec
  Nr of events: 0 (starts 0, restarts 0, aborts 0, finishes 0)
  State: no SR microloop avoidance currently in progress
RP/0/RP0/CPU0:A-ASBR-2#
```

