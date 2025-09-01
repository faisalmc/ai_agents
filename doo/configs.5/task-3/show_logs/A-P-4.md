# Full Output for Task task-3
**Device:** A-P-4 (192.168.100.108)
_Generated: 2025-08-05 02:48:33.195420_

## show run router bgp

```
show run router bgp

Tue Aug  5 06:48:29.958 UTC
router bgp 100
 bgp router-id 1.0.101.8
 ibgp policy out enforce-modifications
 address-family ipv4 unicast
  network 1.0.101.8/32 route-policy SID(8)
  allocate-label all
 !
 neighbor-group RR
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
   next-hop-self
  !
 !
 neighbor-group RR_CLIENT
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
   next-hop-self
   route-reflector-client
  !
 !
 neighbor 1.0.101.4
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.9
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.10
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.11
  use neighbor-group RR
 !
 neighbor 1.0.101.12
  use neighbor-group RR
 !
!

RP/0/RP0/CPU0:A-P-4#
```

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug  5 06:48:30.207 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.4         0   100                                      00:06:33 Established 
1.0.101.9         0   100                                      00:06:24 Established 
1.0.101.10        0   100                                      00:06:23 Established 
1.0.101.11        0   100                                      00:06:35 Established 
1.0.101.12        0   100                                      00:06:34 Established 
RP/0/RP0/CPU0:A-P-4#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug  5 06:48:30.354 UTC
BGP router identifier 1.0.101.8, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 15
BGP table nexthop route policy: 
BGP main routing table version 15
BGP NSR Initial initsync version 10 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
*>i1.0.101.1/32       1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.2/32       1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.3/32       1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.4/32       1.0.101.4                0    100      0 i
*>i1.0.101.5/32       1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.6/32       1.0.101.6                0    100      0 i
* i                   1.0.101.6                0    100      0 i
*>i1.0.101.7/32       1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*> 1.0.101.8/32       0.0.0.0                  0         32768 i
* i1.0.101.9/32       1.0.101.9                0    100      0 i
*>i                   1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*>i1.0.101.10/32      1.0.101.10               0    100      0 i

Processed 10 prefixes, 18 paths
RP/0/RP0/CPU0:A-P-4#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:48:30.550 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)                  1.0.101.5       0           
16002  16002       SR Pfx (idx 2)                  1.0.101.5       0           
16003  16003       SR Pfx (idx 3)                  1.0.101.5       0           
16004  Pop         SR Pfx (idx 4)     Gi0/0/0/4    1.0.23.1        4932        
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/3    1.0.35.1        0           
16006  Pop         SR Pfx (idx 6)     Gi0/0/0/1    1.0.31.1        0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/2    1.0.34.1        1523        
16008  Aggregate   SR Pfx (idx 8)     default                      0           
16009  16009       SR Pfx (idx 9)     Gi0/0/0/0    1.0.51.1        2365        
16010  Pop         SR Pfx (idx 10)    Gi0/0/0/0    1.0.51.1        1930        
17004  Pop         SR Pfx (idx 1004)  Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
17005  Pop         SR Pfx (idx 1005)  Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
17006  Pop         SR Pfx (idx 1006)  Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
17007  Pop         SR Pfx (idx 1007)  Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
17008  Aggregate   SR Pfx (idx 1008)  default                      0           
17009  17009       SR Pfx (idx 1009)  Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
17010  Pop         SR Pfx (idx 1010)  Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/4    1.0.23.1        0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/4    1.0.23.1        0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    1.0.51.1        0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    1.0.51.1        0           
24004  Pop         SR Adj (idx 1)     Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
24005  Pop         SR Adj (idx 3)     Gi0/0/0/4    fe80::5054:ff:fe3a:661b   \
                                                                   0           
24006  Pop         SR Adj (idx 1)     Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24007  Pop         SR Adj (idx 3)     Gi0/0/0/0    fe80::5054:ff:fed6:139b   \
                                                                   0           
24008  Pop         SR Adj (idx 1)     Gi0/0/0/1    1.0.31.1        0           
24009  Pop         SR Adj (idx 3)     Gi0/0/0/1    1.0.31.1        0           
24010  Pop         SR Adj (idx 1)     Gi0/0/0/2    1.0.34.1        0           
24011  Pop         SR Adj (idx 3)     Gi0/0/0/2    1.0.34.1        0           
24012  Pop         SR Adj (idx 1)     Gi0/0/0/3    1.0.35.1        0           
24013  Pop         SR Adj (idx 3)     Gi0/0/0/3    1.0.35.1        0           
24014  Pop         SR Adj (idx 1)     Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
24015  Pop         SR Adj (idx 3)     Gi0/0/0/1    fe80::5054:ff:fe71:b16f   \
                                                                   0           
24016  Pop         SR Adj (idx 1)     Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
24017  Pop         SR Adj (idx 3)     Gi0/0/0/2    fe80::5054:ff:fe0c:c8dc   \
                                                                   0           
24018  Pop         SR Adj (idx 1)     Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
24019  Pop         SR Adj (idx 3)     Gi0/0/0/3    fe80::5054:ff:fe52:e6e6   \
                                                                   0           
RP/0/RP0/CPU0:A-P-4#
```

