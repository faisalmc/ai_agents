# Grading Output for Task taREMOVED3
**Device:** A-PE-3 (192.168.100.103)
_Generated: 2025-08-26 16:46:43.287168_

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug 26 16:46:23.609 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.5         0   100                                         1d04h Idle        
1.0.101.6         0   100                                         1d06h Established 
RP/0/RP0/CPU0:A-PE-3#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug 26 16:46:23.730 UTC
BGP router identifier 1.0.101.3, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 17
BGP table nexthop route policy: 
BGP main routing table version 17
BGP NSR Initial initsync version 3 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
*>i1.0.101.1/32       1.0.101.6                0    100      0 i
*>i1.0.101.2/32       1.0.101.6                0    100      0 i
*> 1.0.101.3/32       0.0.0.0                  0         32768 i
*>i1.0.101.4/32       1.0.101.6                0    100      0 i
*>i1.0.101.6/32       1.0.101.6                0    100      0 i
*>i1.0.101.7/32       1.0.101.6                0    100      0 i
*>i1.0.101.8/32       1.0.101.6                0    100      0 i
*>i1.0.101.9/32       1.0.101.6                0    100      0 i
*>i1.0.101.10/32      1.0.101.6                0    100      0 i

Processed 9 prefixes, 9 paths
RP/0/RP0/CPU0:A-PE-3#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug 26 16:46:23.881 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)     Gi0/0/0/0    1.0.22.2        0           
16002  16002       SR Pfx (idx 2)     Gi0/0/0/0    1.0.22.2        0           
16003  Aggregate   SR Pfx (idx 3)     default                      0           
16004  16004       SR Pfx (idx 4)                  1.0.101.6       0           
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/0    1.0.22.2        180339      
16007  16007       SR Pfx (idx 7)                  1.0.101.6       0           
16008  16008       SR Pfx (idx 8)                  1.0.101.6       0           
16009  16009       SR Pfx (idx 9)                  1.0.101.6       0           
16010  16010       SR Pfx (idx 10)                 1.0.101.6       0           
17001  17001       SR Pfx (idx 1001)  Gi0/0/0/0    fe80::5054:ff:fe99:b62d   \
                                                                   0           
17002  17002       SR Pfx (idx 1002)  Gi0/0/0/0    fe80::5054:ff:fe99:b62d   \
                                                                   0           
17003  Aggregate   SR Pfx (idx 1003)  default                      0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/0    fe80::5054:ff:fe99:b62d   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.22.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.22.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe99:b62d   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe99:b62d   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-3#
```

