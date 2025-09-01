# Grading Output for Task task-8.charlie.p2.evpn/
**Device:** C-PE-1 (192.168.100.131)
_Generated: 2025-08-06 03:09:10.734645_

## show l2vpn xconnect

```
show l2vpn xconnect

Wed Aug  6 07:09:06.920 UTC
Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
        SB = Standby, SR = Standby Ready, (PP) = Partially Programmed,
        LU = Local Up, RU = Remote Up, CO = Connected, (SI) = Seamless Inactive

XConnect                   Segment 1                       Segment 2                
Group      Name       ST   Description            ST       Description            ST    
------------------------   -----------------------------   -----------------------------
evpn-vpws  RED20      UP   Gi0/0/0/2.20           UP       EVPN 30020,30020,::ffff:10.0.0.1 
                                                                                  UP    
----------------------------------------------------------------------------------------
RP/0/RP0/CPU0:C-PE-1#
```

## show l2vpn xconnect detail

```
show l2vpn xconnect detail

Wed Aug  6 07:09:07.061 UTC

Group evpn-vpws, XC RED20, state is up; Interworking none
  AC: GigabitEthernet0/0/0/2.20, state is up
    Type VLAN; Num Ranges: 1
    Rewrite Tags: []
    VLAN ranges: [20, 20]
    MTU 1504; XC ID 0x2; interworking none
    Statistics:
      packets: received 163, sent 157
      bytes: received 18772, sent 18308
      drops: illegal VLAN 0, illegal length 0
  EVPN: neighbor ::ffff:10.0.0.1, PW ID: evi 30020, ac-id 30020, state is up ( established )
    XC ID 0xa0000003
    Encapsulation SRv6
    Encap type Ethernet
    Ignore MTU mismatch: Enabled
    Transmit MTU zero: Enabled
    Reachability: Up

      SRv6              Local                        Remote                      
      ----------------  ---------------------------- --------------------------
      uDX2              fc00:100:1:e004::            fc00:100:3:e008::
      AC ID             30020                        30020                       
      MTU               1518                         0                           
      Locator           CCIE_ALGO_0                  N/A                         
      Locator Resolved  Yes                          N/A                         
      SRv6 Headend      H.Encaps.L2.Red              N/A                         
    Statistics:
      packets: received 157, sent 163
      bytes: received 18308, sent 18772
RP/0/RP0/CPU0:C-PE-1#
```

## show bgp l2vpn evpn

```
show bgp l2vpn evpn

Wed Aug  6 07:09:07.218 UTC
BGP router identifier 3.0.101.1, local AS number 300
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 6
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 3.0.101.1:30020 (default for vrf VPWS:30020)
Route Distinguisher Version: 6
*> [1][0000.0000.0000.0000.0000][30020]/120
                      0.0.0.0                                0 i
*>i[1][0000.1122.3344.5566.7788][30020]/120
                      2620:fc7:3:101::3
                                                    100      0 i
*>i[1][0000.1122.3344.5566.7788][4294967295]/120
                      2620:fc7:3:101::3
                                                    100      0 i
Route Distinguisher: 3.0.101.3:1
Route Distinguisher Version: 3
*>i[1][3.0.101.3:1][0000.1122.3344.5566.7788][4294967295]/184
                      2620:fc7:3:101::3
                                                    100      0 i
Route Distinguisher: 3.0.101.3:30020
Route Distinguisher Version: 4
*>i[1][0000.1122.3344.5566.7788][30020]/120
                      2620:fc7:3:101::3
                                                    100      0 i

Processed 5 prefixes, 5 paths
RP/0/RP0/CPU0:C-PE-1#
```

