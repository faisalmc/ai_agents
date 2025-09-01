# Full Output for Task task-8.charlie.p1.ibgp/
**Device:** C-PE-4 (192.168.100.134)
_Generated: 2025-08-05 04:36:58.066190_

## show ip bgp neighbors brief

```
show ip bgp neighbors brief

Tue Aug  5 08:36:55.415 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
3.0.101.1         0   300                                      01:38:23 Established 
3.0.101.2         0   300                                      01:38:25 Established 
3.0.101.3         0   300                                      01:38:20 Established 
3.0.101.7         0   300                                      01:38:18 Established 
3.0.101.8         0   300                                      01:38:15 Established 
2620:fc7:3:101::1
                  0   300                                      00:16:52 Established 
2620:fc7:3:101::2
                  0   300                                      00:16:57 Established 
2620:fc7:3:101::3
                  0   300                                      00:16:46 Established 
2620:fc7:3:101::7
                  0   300                                      00:16:46 Established 
2620:fc7:3:101::8
                  0   300                                      00:16:47 Established 
RP/0/RP0/CPU0:C-PE-4#
```

## show ip bgp vpnv4 unicast summary

```
show ip bgp vpnv4 unicast summary

Tue Aug  5 08:36:55.565 UTC
BGP router identifier 3.0.101.4, local AS number 300
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
3.0.101.1         0   300     104     105        1    0    0 01:38:23          0
3.0.101.2         0   300     104     106        1    0    0 01:38:25          0
3.0.101.3         0   300     104     106        1    0    0 01:38:20          0
3.0.101.7         0   300     104     106        1    0    0 01:38:18          0
3.0.101.8         0   300     104     107        1    0    0 01:38:16          0
2620:fc7:3:101::1
                  0   300      22      23        1    0    0 00:16:52          0
2620:fc7:3:101::2
                  0   300      22      23        1    0    0 00:16:57          0
2620:fc7:3:101::3
                  0   300      22      23        1    0    0 00:16:47          0
2620:fc7:3:101::7
                  0   300      22      23        1    0    0 00:16:47          0
2620:fc7:3:101::8
                  0   300      22      23        1    0    0 00:16:47          0

RP/0/RP0/CPU0:C-PE-4#
```

