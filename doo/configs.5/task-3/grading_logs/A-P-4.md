# Grading Output for Task taREMOVED3
**Device:** A-P-4 (192.168.100.108)
_Generated: 2025-08-26 16:46:53.277028_

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug 26 16:46:33.680 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.4         0   100                                         1d06h Established 
1.0.101.9         0   100                                         1d06h Established 
1.0.101.10        0   100                                         1d06h Established 
1.0.101.11        0   100                                         1d06h Established 
1.0.101.12        0   100                                         1d06h Established 
RP/0/RP0/CPU0:A-P-4#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug 26 16:46:33.803 UTC
BGP router identifier 1.0.101.8, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 26
BGP table nexthop route policy: 
BGP main routing table version 26
BGP NSR Initial initsync version 10 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
*>i1.0.101.1/32       1.0.101.6                0    100      0 i
* i                   1.0.101.6                0    100      0 i
*>i1.0.101.2/32       1.0.101.6                0    100      0 i
* i                   1.0.101.6                0    100      0 i
*>i1.0.101.3/32       1.0.101.6                0    100      0 i
* i                   1.0.101.6                0    100      0 i
*>i1.0.101.4/32       1.0.101.4                0    100      0 i
*>i1.0.101.6/32       1.0.101.6                0    100      0 i
* i                   1.0.101.6                0    100      0 i
*>i1.0.101.7/32       1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*> 1.0.101.8/32       0.0.0.0                  0         32768 i
* i1.0.101.9/32       1.0.101.9                0    100      0 i
*>i                   1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*>i1.0.101.10/32      1.0.101.10               0    100      0 i

Processed 9 prefixes, 16 paths
RP/0/RP0/CPU0:A-P-4#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug 26 16:46:33.948 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)                  1.0.101.6       0           
16002  16002       SR Pfx (idx 2)                  1.0.101.6       0           
16003  16003       SR Pfx (idx 3)                  1.0.101.6       0           
16004  Pop         SR Pfx (idx 4)     Gi0/0/0/4    1.0.23.1        363077      
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/1    1.0.31.1        0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/2    1.0.34.1        180358      
16008  Aggregate   SR Pfx (idx 8)     default                      0           
16009  16009       SR Pfx (idx 9)     Gi0/0/0/0    1.0.51.1        181642      
16010  Pop         SR Pfx (idx 10)    Gi0/0/0/0    1.0.51.1        177575      
17004  Pop         SR Pfx (idx 1004)  Gi0/0/0/4    fe80::5054:ff:fe7f:ac62   \
                                                                   0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/1    fe80::5054:ff:feca:8b79   \
                                                                   0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/2    fe80::5054:ff:fe05:dda7   \
                                                                   0           
17008  Aggregate   SR Pfx (idx 1008)  default                      0           
17009  17009       SR Pfx (idx 1009)  Gi0/0/0/0    fe80::5054:ff:fe57:46ea   \
                                                                   0           
17010  Pop         SR Pfx (idx 1010)  Gi0/0/0/0    fe80::5054:ff:fe57:46ea   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/4    1.0.23.1        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/4    1.0.23.1        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.51.1        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.51.1        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/4    fe80::5054:ff:fe7f:ac62   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/4    fe80::5054:ff:fe7f:ac62   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe57:46ea   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe57:46ea   \
                                                                   0           
24008  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.31.1        0           
24009  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.31.1        0           
24010  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.34.1        0           
24011  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.34.1        0           
24012  Pop         SR Adj (idx 1)     Gi0/0/0/3    1.0.35.1        0           
24013  Pop         SR Adj (idx 3)     Gi0/0/0/3    1.0.35.1        0           
24014  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:feca:8b79   \
                                                                   0           
24015  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:feca:8b79   \
                                                                   0           
24016  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fe05:dda7   \
                                                                   0           
24017  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fe05:dda7   \
                                                                   0           
24018  Pop         SR Adj (idx 1)     Gi0/0/0/3    fe80::5054:ff:fee3:e3d   \
                                                                   0           
24019  Pop         SR Adj (idx 3)     Gi0/0/0/3    fe80::5054:ff:fee3:e3d   \
                                                                   0           
RP/0/RP0/CPU0:A-P-4#
```

