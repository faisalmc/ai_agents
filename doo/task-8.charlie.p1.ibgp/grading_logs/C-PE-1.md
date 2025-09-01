# Grading Output for Task task-8.charlie.p1.ibgp/
**Device:** C-PE-1 (192.168.100.131)
_Generated: 2025-08-05 04:36:52.505955_

## show ip bgp neighbors brief

```
show ip bgp neighbors brief

Tue Aug  5 08:36:49.670 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
3.0.101.2         0   300                                      01:38:27 Established 
3.0.101.3         0   300                                      01:38:23 Established 
3.0.101.4         0   300                                      01:38:17 Established 
3.0.101.7         0   300                                      01:38:16 Established 
3.0.101.8         0   300                                      01:38:11 Established 
2620:fc7:3:101::2
                  0   300                                      00:16:57 Established 
2620:fc7:3:101::3
                  0   300                                      00:16:52 Established 
2620:fc7:3:101::4
                  0   300                                      00:16:46 Established 
2620:fc7:3:101::7
                  0   300                                      00:16:52 Established 
2620:fc7:3:101::8
                  0   300                                      00:16:51 Established 
RP/0/RP0/CPU0:C-PE-1#
```

## show ip bgp vpnv4 unicast summary

```
show ip bgp vpnv4 unicast summary

Tue Aug  5 08:36:49.845 UTC
BGP router identifier 3.0.101.1, local AS number 300
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 1
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker               1          1          1          1           1           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
3.0.101.2         0   300     104     105        1    0    0 01:38:27          0
3.0.101.3         0   300     104     104        1    0    0 01:38:24          0
3.0.101.4         0   300     105     104        1    0    0 01:38:18          0
3.0.101.7         0   300     104     104        1    0    0 01:38:16          0
3.0.101.8         0   300     104     104        1    0    0 01:38:12          0
2620:fc7:3:101::2
                  0   300      22      22        1    0    0 00:16:57          0
2620:fc7:3:101::3
                  0   300      22      22        1    0    0 00:16:52          0
2620:fc7:3:101::4
                  0   300      23      22        1    0    0 00:16:47          0
2620:fc7:3:101::7
                  0   300      22      22        1    0    0 00:16:52          0
2620:fc7:3:101::8
                  0   300      22      22        1    0    0 00:16:51          0

RP/0/RP0/CPU0:C-PE-1#
```

