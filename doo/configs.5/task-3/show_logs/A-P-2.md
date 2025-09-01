# Full Output for Task task-3
**Device:** A-P-2 (192.168.100.106)
_Generated: 2025-08-05 02:48:27.978387_

## show run router bgp

```
show run router bgp

Tue Aug  5 06:48:24.686 UTC
router bgp 100
 bgp router-id 1.0.101.6
 ibgp policy out enforce-modifications
 address-family ipv4 unicast
  network 1.0.101.6/32 route-policy SID(6)
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
 neighbor 1.0.101.1
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.2
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.3
  use neighbor-group RR_CLIENT
 !
 neighbor 1.0.101.11
  use neighbor-group RR
 !
 neighbor 1.0.101.12
  use neighbor-group RR
 !
!

RP/0/RP0/CPU0:A-P-2#
```

## show bgp neighbors brief

```
show bgp neighbors brief

Tue Aug  5 06:48:24.916 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
1.0.101.1         0   100                                      00:06:37 Established 
1.0.101.2         0   100                                      00:06:39 Established 
1.0.101.3         0   100                                      00:06:39 Established 
1.0.101.11        0   100                                      00:06:32 Established 
1.0.101.12        0   100                                      00:06:24 Established 
RP/0/RP0/CPU0:A-P-2#
```

## show bgp ipv4 labeled-unicast

```
show bgp ipv4 labeled-unicast

Tue Aug  5 06:48:25.093 UTC
BGP router identifier 1.0.101.6, local AS number 100
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 18
BGP table nexthop route policy: 
BGP main routing table version 18
BGP NSR Initial initsync version 6 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
* i1.0.101.1/32       1.0.101.1                0    100      0 i
*>i                   1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.2/32       1.0.101.2                0    100      0 i
* i                   1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.3/32       1.0.101.3                0    100      0 i
* i                   1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*>i1.0.101.4/32       1.0.101.8                0    100      0 i
* i                   1.0.101.8                0    100      0 i
*>i1.0.101.5/32       1.0.101.5                0    100      0 i
* i                   1.0.101.5                0    100      0 i
*> 1.0.101.6/32       0.0.0.0                  0         32768 i
*>i1.0.101.7/32       1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*>i1.0.101.8/32       1.0.101.8                0    100      0 i
* i                   1.0.101.8                0    100      0 i
*>i1.0.101.9/32       1.0.101.7                0    100      0 i
* i                   1.0.101.7                0    100      0 i
*>i1.0.101.10/32      1.0.101.8                0    100      0 i
* i                   1.0.101.8                0    100      0 i

Processed 10 prefixes, 22 paths
RP/0/RP0/CPU0:A-P-2#
```

## show mpls forwarding

```
show mpls forwarding

Tue Aug  5 06:48:25.284 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  16001       SR Pfx (idx 1)     Gi0/0/0/1    1.0.21.1        2521        
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/1    1.0.21.1        2334        
16003  Pop         SR Pfx (idx 3)     Gi0/0/0/4    1.0.22.1        4627        
16004  16004       SR Pfx (idx 4)                  1.0.101.8       0           
16005  Pop         SR Pfx (idx 5)     Gi0/0/0/2    1.0.33.1        1347        
16006  Aggregate   SR Pfx (idx 6)     default                      0           
16007  Pop         SR Pfx (idx 7)     Gi0/0/0/3    1.0.32.2        0           
16008  Pop         SR Pfx (idx 8)     Gi0/0/0/0    1.0.31.2        0           
16009  16009       SR Pfx (idx 9)                  1.0.101.7       0           
16010  16010       SR Pfx (idx 10)                 1.0.101.8       0           
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

