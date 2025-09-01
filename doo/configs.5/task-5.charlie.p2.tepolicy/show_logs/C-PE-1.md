# Full Output for Task task-5.charlie.p2.tepolicy/
**Device:** C-PE-1 (192.168.100.131)
_Generated: 2025-08-05 03:00:47.002385_

## show run segment-routing

```
show run segment-routing

Tue Aug  5 07:00:44.244 UTC
segment-routing
 global-block 16000 23999
 local-block 25000 26000
 traffic-eng
  policy p1
   binding-sid mpls 78787
   color 66 end-point ipv4 3.0.101.4
   autoroute
    include ipv4 3.0.101.66/32
   !
   candidate-paths
    preference 100
     dynamic
      metric
       type te
      !
     !
    !
   !
  !
 !
!

RP/0/RP0/CPU0:C-PE-1#
```

## show segment-routing traffic-eng policy

```
show segment-routing traffic-eng policy

Tue Aug  5 07:00:44.636 UTC

SR-TE policy database
---------------------

Color: 66, End-point: 3.0.101.4
  Name: srte_c_66_ep_3.0.101.4
  Status:
    Admin: up  Operational: up for 00:01:00 (since Aug  5 06:59:44.283)
  Candidate-paths:
    Preference: 100 (configuration) (active)
      Name: p1
      Requested BSID: 78787
      Constraints:
        Protection Type: protected-preferred
        Maximum SID Depth: 10 
      Dynamic (valid)
        Metric Type: TE,   Path Accumulated Metric: 30 
          SID[0]: 16005 [Prefix-SID, 3.0.101.5]
          SID[1]: 16006 [Prefix-SID, 3.0.101.6]
          SID[2]: 16004 [Prefix-SID, 3.0.101.4]
  Attributes:
    Binding SID: 78787
    Forward Class: Not Configured
    Steering labeled-services disabled: no
    Steering BGP disabled: no
    IPv6 caps enable: yes
    Invalidation drop enabled: no
    Max Install Standby Candidate Paths: 0

RP/0/RP0/CPU0:C-PE-1#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 07:00:44.882 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Aggregate   SR Pfx (idx 1)     default                      0           
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/1    3.3.9.2         930         
16003  16003       SR Pfx (idx 3)     Gi0/0/0/0    3.3.8.2         0           
       16003       SR Pfx (idx 3)     Gi0/0/0/1    3.3.9.2         799         
16004  16004       SR Pfx (idx 4)     Gi0/0/0/0    3.3.8.2         224         
       16004       SR Pfx (idx 4)     Gi0/0/0/1    3.3.9.2         1119        
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/0    3.3.8.2         0           
16006  16006       SR Pfx (idx 6)     Gi0/0/0/0    3.3.8.2         0           
       16006       SR Pfx (idx 6)     Gi0/0/0/1    3.3.9.2         0           
16007  16007       SR Pfx (idx 7)     Gi0/0/0/0    3.3.8.2         847         
16008  16008       SR Pfx (idx 8)     Gi0/0/0/0    3.3.8.2         0           
       16008       SR Pfx (idx 8)     Gi0/0/0/1    3.3.9.2         807         
16041  16041       SR Pfx (idx 41)    Gi0/0/0/0    3.3.8.2         0           
       16041       SR Pfx (idx 41)    Gi0/0/0/1    3.3.9.2         0           
17001  Aggregate   SR Pfx (idx 1001)  default                      0           
17002  Pop         SR Pfx (idx 1002)  Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
17003  17003       SR Pfx (idx 1003)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
       17003       SR Pfx (idx 1003)  Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
17004  17004       SR Pfx (idx 1004)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
       17004       SR Pfx (idx 1004)  Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
17005  Pop         SR Pfx (idx 1005)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
17006  17006       SR Pfx (idx 1006)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
       17006       SR Pfx (idx 1006)  Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
17007  17007       SR Pfx (idx 1007)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
17008  17008       SR Pfx (idx 1008)  Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
       17008       SR Pfx (idx 1008)  Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    3.3.9.2         0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    3.3.9.2         0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fe39:b02f   \
                                                                   0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/0    3.3.8.2         0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/0    3.3.8.2         0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fea5:ba01   \
                                                                   0           
24008  16006       SR TE: 1 [TE-INT]  Gi0/0/0/0    3.3.8.2         0           
24009  Pop         3.0.101.66/32      srte_c_66_ep 3.0.101.4       0           
78787  Pop         No ID              srte_c_66_ep point2point     0           
RP/0/RP0/CPU0:C-PE-1#
```

## show mpls forwarding labels 78787

```
show mpls forwarding labels 78787

Tue Aug  5 07:00:45.413 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
78787  Pop         No ID              srte_c_66_ep point2point     0           
RP/0/RP0/CPU0:C-PE-1#
```

## show bgp ipv4 unicast 3.0.101.77/32

```
show bgp ipv4 unicast 3.0.101.77/32

Tue Aug  5 07:00:45.644 UTC
BGP routing table entry for 3.0.101.77/32
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                   3            3
Last Modified: Aug  5 07:00:42.992 for 00:00:02
Paths: (1 available, best #1)
  Not advertised to any peer
  Path #1: Received by speaker 0
  Not advertised to any peer
  Local
    3.0.101.4 C:66 (bsid:78787) (metric 30) from 3.0.101.4 (3.0.101.4)
      Origin IGP, metric 0, localpref 100, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 1, version 3
      Extended community: Color:66 
      SR policy color 66, up, not-registered, bsid 78787

RP/0/RP0/CPU0:C-PE-1#
```

## ping 3.0.101.77 source loopback 0 repeat 40

```
ping 3.0.101.77 source loopback 0 repeat 40

Tue Aug  5 07:00:45.787 UTC
Type escape sequence to abort.
Sending 40, 100-byte ICMP Echos to 3.0.101.77 timeout is 2 seconds:
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (40/40), round-trip min/avg/max = 7/10/21 ms
RP/0/RP0/CPU0:C-PE-1#
```

## traceroute 3.0.101.77 source loopback 0

```
traceroute 3.0.101.77 source loopback 0

Tue Aug  5 07:00:50.097 UTC

Type escape sequence to abort.
Tracing the route to 3.0.101.77

 1  3.3.8.2 [MPLS: Labels 16006/16004 Exp 0] 13 msec  7 msec  13 msec 
 2  3.3.3.2 [MPLS: Label 16004 Exp 0] 9 msec  8 msec  13 msec 
 3  3.3.6.2 12 msec  *  10 msec 
RP/0/RP0/CPU0:C-PE-1#
```

