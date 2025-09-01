# Grading Output for Task task-8.charlie.p2.evpn/
**Device:** C-PE-2 (192.168.100.132)
_Generated: 2025-08-06 03:09:13.112928_

## show l2vpn xconnect

```
show l2vpn xconnect

Wed Aug  6 07:09:09.222 UTC
Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
        SB = Standby, SR = Standby Ready, (PP) = Partially Programmed,
        LU = Local Up, RU = Remote Up, CO = Connected, (SI) = Seamless Inactive

XConnect                   Segment 1                       Segment 2                
Group      Name       ST   Description            ST       Description            ST    
------------------------   -----------------------------   -----------------------------
evpn-vpws  RED20      DN   BE23.20                DN       EVPN 30020,30020,::ffff:10.0.0.1 
                                                                                  DN    
----------------------------------------------------------------------------------------
RP/0/RP0/CPU0:C-PE-2#
```

## show l2vpn xconnect detail

```
show l2vpn xconnect detail

Wed Aug  6 07:09:09.378 UTC

Group evpn-vpws, XC RED20, state is down; Interworking none
  AC: Bundle-Ether23.20, state is down
    Type VLAN; Num Ranges: 1
    Rewrite Tags: []
    VLAN ranges: [20, 20]
    MTU 1504; XC ID 0xc0000002; interworking none
    Statistics:
      packets: received 0, sent 0
      bytes: received 0, sent 0
      drops: illegal VLAN 0, illegal length 0
  EVPN: neighbor ::ffff:10.0.0.1, PW ID: evi 30020, ac-id 30020, state is down ( provisioned )
    XC ID 0xa0000003
    Encapsulation SRv6
    Encap type Ethernet
    Ignore MTU mismatch: Enabled
    Transmit MTU zero: Enabled
    Reachability: Up
    Down reason(s): AC parent down
                    Waiting for DF election

      SRv6              Local                        Remote                      
      ----------------  ---------------------------- --------------------------
      uDX2              fc00:100:2:e008::            fc00:100:1:e004::
      AC ID             30020                        30020                       
      MTU               1518                         0                           
      Locator           CCIE_ALGO_0                  N/A                         
      Locator Resolved  Yes                          N/A                         
      SRv6 Headend      H.Encaps.L2.Red              N/A                         
    Statistics:
      packets: received 0, sent 0
      bytes: received 0, sent 0
RP/0/RP0/CPU0:C-PE-2#
```

## show bgp l2vpn evpn

```
show bgp l2vpn evpn

Wed Aug  6 07:09:09.502 UTC
BGP router identifier 3.0.101.2, local AS number 300
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 12
BGP NSR Initial initsync version 1 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

Status codes: s suppressed, d damped, h history, * valid, > best
              i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
   Network            Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 3.0.101.1:30020
Route Distinguisher Version: 2
*>i[1][0000.0000.0000.0000.0000][30020]/120
                      2620:fc7:3:101::1
                                                    100      0 i
Route Distinguisher: 3.0.101.2:0 (default for vrf ES:GLOBAL)
Route Distinguisher Version: 6
*>i[4][0000.1122.3344.5566.7788][32][3.0.101.3]/128
                      3.0.101.3                     100      0 i
Route Distinguisher: 3.0.101.2:30020 (default for vrf VPWS:30020)
Route Distinguisher Version: 10
*>i[1][0000.0000.0000.0000.0000][30020]/120
                      2620:fc7:3:101::1
                                                    100      0 i
*>i[1][0000.1122.3344.5566.7788][30020]/120
                      3.0.101.3                     100      0 i
*>i[1][0000.1122.3344.5566.7788][4294967295]/120
                      3.0.101.3                     100      0 i
Route Distinguisher: 3.0.101.3:0
Route Distinguisher Version: 5
*>i[4][0000.1122.3344.5566.7788][32][3.0.101.3]/128
                      3.0.101.3                     100      0 i
* i                   2620:fc7:3:101::3
                                                    100      0 i
Route Distinguisher: 3.0.101.3:1
Route Distinguisher Version: 11
*>i[1][3.0.101.3:1][0000.1122.3344.5566.7788][4294967295]/184
                      3.0.101.3                     100      0 i
* i                   2620:fc7:3:101::3
                                                    100      0 i
Route Distinguisher: 3.0.101.3:30020
Route Distinguisher Version: 12
*>i[1][0000.1122.3344.5566.7788][30020]/120
                      3.0.101.3                     100      0 i
* i                   2620:fc7:3:101::3
                                                    100      0 i

Processed 8 prefixes, 11 paths
RP/0/RP0/CPU0:C-PE-2#
```

## show bundle bundle-ether 23

```
show bundle bundle-ether 23

Wed Aug  6 07:09:09.699 UTC

Bundle-Ether23
  Status:                                    Down
  Local links <active/standby/configured>:   0 / 0 / 1
  Local bandwidth <effective/available>:     0 (0) kbps
  MAC address (source):                      0050.507a.1604 (Chassis pool)
  Inter-chassis link:                        No
  Minimum active links / bandwidth:          1 / 1 kbps
  Maximum active links:                      24
  Wait while timer:                          2000 ms
  Load balancing:                            
    Link order signaling:                    Not configured
    Hash type:                               Default
    Locality threshold:                      None
  LACP:                                      Operational
    Flap suppression timer:                  Off
    Cisco extensions:                        Disabled
    Non-revertive:                           Disabled
  mLACP:                                     Not configured
  IPv4 BFD:                                  Not configured
  IPv6 BFD:                                  Not configured

  Port                  Device           State        Port ID         B/W, kbps
  --------------------  ---------------  -----------  --------------  ----------
  Gi0/0/0/4             Local            Negotiating  0x8000, 0x0001     1000000
      Partner is not Synchronized (Waiting, Standby, or LAG ID mismatch)
RP/0/RP0/CPU0:C-PE-2#
```

