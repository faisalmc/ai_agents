# Grading Output for Task taREMOVED3
**Device:** A-PE-4 (192.168.100.104)
_Generated: 2025-08-26 16:46:45.228807_

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug 26 16:46:25.463 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.7         0   100                                         1d06h Established 
1.0.101.8         0   100                                         1d06h Established 
RP/0/RP0/CPU0:A-PE-4#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug 26 16:46:25.584 UTC
BGP router identifier 1.0.101.4, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 27
BGP table nexthop route policy: 
BGP main routing table version 27
BGP NSR Initial initsync version 3 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
* i1.0.101.1/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.2/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.3/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
*> 1.0.101.4/32       0.0.0.0                  0         32768 i
* i1.0.101.6/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.7/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.8/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.9/32       1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i
* i1.0.101.10/32      1.0.101.7                0    100      0 i
*>i                   1.0.101.8                0    100      0 i

Processed 9 prefixes, 17 paths
RP/0/RP0/CPU0:A-PE-4#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug 26 16:46:25.730 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)                  1.0.101.8       0           
16002  16002       SR Pfx (idx 2)                  1.0.101.8       0           
16003  16003       SR Pfx (idx 3)                  1.0.101.8       0           
16004  Aggregate   SR Pfx (idx 4)     default                      0           
16006  16006       SR Pfx (idx 6)                  1.0.101.8       0           
16007  16007       SR Pfx (idx 7)     Gi0/0/0/0    1.0.23.2        180299      
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/0    1.0.23.2        180259      
16009  16009       SR Pfx (idx 9)     Gi0/0/0/0    1.0.23.2        0           
16010  16010       SR Pfx (idx 10)    Gi0/0/0/0    1.0.23.2        0           
17004  Aggregate   SR Pfx (idx 1004)  default                      0           
17007  17007       SR Pfx (idx 1007)  Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
17008  Pop         SR Pfx (idx 1008)  Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
17009  17009       SR Pfx (idx 1009)  Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
17010  17010       SR Pfx (idx 1010)  Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.23.2        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.23.2        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fe6c:c8cf   \
                                                                   0           
RP/0/RP0/CPU0:A-PE-4#
```

