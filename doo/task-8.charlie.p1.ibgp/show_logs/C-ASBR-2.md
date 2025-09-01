# Full Output for Task task-8.charlie.p1.ibgp/
**Device:** C-ASBR-2 (192.168.100.138)
_Generated: 2025-08-05 04:37:01.873164_

## show ip bgp neighbors brief

```
show ip bgp neighbors brief

Tue Aug  5 08:36:59.055 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
3.0.101.1         0   300                                      01:38:21 Established 
3.0.101.2         0   300                                      01:38:18 Established 
3.0.101.3         0   300                                      01:38:18 Established 
3.0.101.4         0   300                                      01:38:19 Established 
2620:fc7:3:101::1
                  0   300                                      00:17:00 Established 
2620:fc7:3:101::2
                  0   300                                      00:16:54 Established 
2620:fc7:3:101::3
                  0   300                                      00:16:57 Established 
2620:fc7:3:101::4
                  0   300                                      00:16:51 Established 
RP/0/RP0/CPU0:C-ASBR-2#
```

## show ip bgp vpnv4 unicast summary

```
show ip bgp vpnv4 unicast summary

Tue Aug  5 08:36:59.204 UTC
BGP router identifier 3.0.101.8, local AS number 300
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
3.0.101.1         0   300     104     104        1    0    0 01:38:21          0
3.0.101.2         0   300     104     104        1    0    0 01:38:18          0
3.0.101.3         0   300     104     105        1    0    0 01:38:18          0
3.0.101.4         0   300     106     104        1    0    0 01:38:19          0
2620:fc7:3:101::1
                  0   300      22      22        1    0    0 00:17:00          0
2620:fc7:3:101::2
                  0   300      22      22        1    0    0 00:16:54          0
2620:fc7:3:101::3
                  0   300      22      22        1    0    0 00:16:57          0
2620:fc7:3:101::4
                  0   300      23      22        1    0    0 00:16:51          0

RP/0/RP0/CPU0:C-ASBR-2#
```

