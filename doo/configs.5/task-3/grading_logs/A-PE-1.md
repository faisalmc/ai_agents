# Grading Output for Task taREMOVED3
**Device:** A-PE-1 (192.168.100.101)
_Generated: 2025-08-26 16:46:39.172288_

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug 26 16:46:19.518 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.5         0   100                                         1d04h Idle        
1.0.101.6         0   100                                         1d06h Established 
RP/0/RP0/CPU0:A-PE-1#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug 26 16:46:19.639 UTC
BGP router identifier 1.0.101.1, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 31
BGP table nexthop route policy: 
BGP main routing table version 31
BGP NSR Initial initsync version 3 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
*> 1.0.101.1/32       0.0.0.0                  0         32768 i
*>i1.0.101.2/32       1.0.101.6                0    100      0 i
*>i1.0.101.3/32       1.0.101.6                0    100      0 i
*>i1.0.101.4/32       1.0.101.6                0    100      0 i
*>i1.0.101.6/32       1.0.101.6                0    100      0 i
*>i1.0.101.7/32       1.0.101.6                0    100      0 i
*>i1.0.101.8/32       1.0.101.6                0    100      0 i
*>i1.0.101.9/32       1.0.101.6                0    100      0 i
*>i1.0.101.10/32      1.0.101.6                0    100      0 i

Processed 9 prefixes, 9 paths
RP/0/RP0/CPU0:A-PE-1#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug 26 16:46:19.787 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Aggregate   SR Pfx (idx 1)     default                      0           
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/2    1.0.40.2        12737       
16003  16003       SR Pfx (idx 3)     Gi0/0/0/2    1.0.40.2        13175       
16004  16004       SR Pfx (idx 4)                  1.0.101.6       0           
16006  16006       SR Pfx (idx 6)     Gi0/0/0/2    1.0.40.2        182561      
16007  16007       SR Pfx (idx 7)                  1.0.101.6       1152        
16008  16008       SR Pfx (idx 8)                  1.0.101.6       0           
16009  16009       SR Pfx (idx 9)                  1.0.101.6       768         
16010  16010       SR Pfx (idx 10)                 1.0.101.6       0           
17001  Aggregate   SR Pfx (idx 1001)  default                      0           
17002  Pop         SR Pfx (idx 1002)  Gi0/0/0/2    fe80::5054:ff:fea8:2a5d   \
                                                                   0           
17003  17003       SR Pfx (idx 1003)  Gi0/0/0/2    fe80::5054:ff:fea8:2a5d   \
                                                                   0           
17006  17006       SR Pfx (idx 1006)  Gi0/0/0/2    fe80::5054:ff:fea8:2a5d   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.40.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.40.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.20.2        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.20.2        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fea8:2a5d   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fea8:2a5d   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fece:9dfa   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fece:9dfa   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-1#
```

## show bgp ipv4 labeled-unicast 1.0.101.7

```
show bgp ipv4 labeled-unicast 1.0.101.7

Tue Aug 26 16:46:20.015 UTC
BGP routing table entry for 1.0.101.7/32
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                  28           28
    Local Label: 16007
Last Modified: Aug 25 12:14:01.246 for 1d04h
Paths: (1 available, best #1)
  Not advertised to any peer
  Path #1: Received by speaker 0
  Not advertised to any peer
  Local
    1.0.101.6 (metric 300) from 1.0.101.6 (1.0.101.7)
      Received Label 16007 
      Origin IGP, metric 0, localpref 100, valid, internal, best, group-best, labeled-unicast
      Received Path ID 0, Local Path ID 1, version 28
      Originator: 1.0.101.7, Cluster list: 1.0.101.6, 1.0.101.11
      Label-Index: 7
RP/0/RP0/CPU0:A-PE-1#
```

## show bgp ipv4 labeled-unicast 1.0.101.9

```
show bgp ipv4 labeled-unicast 1.0.101.9

Tue Aug 26 16:46:20.159 UTC
BGP routing table entry for 1.0.101.9/32
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                  30           30
    Local Label: 16009
Last Modified: Aug 25 12:14:01.246 for 1d04h
Paths: (1 available, best #1)
  Not advertised to any peer
  Path #1: Received by speaker 0
  Not advertised to any peer
  Local
    1.0.101.6 (metric 300) from 1.0.101.6 (1.0.101.9)
      Received Label 16009 
      Origin IGP, metric 0, localpref 100, valid, internal, best, group-best, labeled-unicast
      Received Path ID 0, Local Path ID 1, version 30
      Originator: 1.0.101.9, Cluster list: 1.0.101.6, 1.0.101.11, 1.0.101.7
      Label-Index: 9
RP/0/RP0/CPU0:A-PE-1#
```

