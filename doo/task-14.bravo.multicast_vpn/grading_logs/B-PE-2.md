# Grading Output for Task task-14.bravo.multicast_vpn/
**Device:** B-PE-2 (192.168.100.118)
_Generated: 2025-07-14 08:59:29.371924_

## show ip pim neighbor

```
show ip pim neighbor

Mon Jul 14 12:59:25.951 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.1.1                      GigabitEthernet0/0/0/0 2d01h     00:01:33 1           B
2.2.1.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:15 1           (DR) B E
2.0.101.2*                   Loopback0              2d01h     00:01:31 1           (DR) B E
2.2.4.1*                     GigabitEthernet0/0/0/2 2d01h     00:01:25 1           B E
2.2.4.2                      GigabitEthernet0/0/0/2 2d01h     00:01:27 1           (DR) B
RP/0/RP0/CPU0:B-PE-2#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Mon Jul 14 12:59:26.088 UTC

PIM neighbors in VRF YELLOW
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.0.101.1                    mdtYELLOW              1d15h     00:01:19 1          
2.0.101.2*                   mdtYELLOW              2d01h     00:01:35 1          
2.0.101.3                    mdtYELLOW              1d15h     00:01:37 1           (DR)
10.20.6.1*                   GigabitEthernet0/0/0/4 1d22h     00:01:27 1           (DR) B E
RP/0/RP0/CPU0:B-PE-2#
```

## show pim neighbor

```
show pim neighbor

Mon Jul 14 12:59:26.223 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.1.1                      GigabitEthernet0/0/0/0 2d01h     00:01:33 1           B
2.2.1.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:15 1           (DR) B E
2.0.101.2*                   Loopback0              2d01h     00:01:30 1           (DR) B E
2.2.4.1*                     GigabitEthernet0/0/0/2 2d01h     00:01:24 1           B E
2.2.4.2                      GigabitEthernet0/0/0/2 2d01h     00:01:26 1           (DR) B
RP/0/RP0/CPU0:B-PE-2#
```

## show bgp ipv4 mvpn summary

```
show bgp ipv4 mvpn summary

Mon Jul 14 12:59:26.360 UTC
BGP router identifier 2.0.101.2, local AS number 200
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 8
BGP NSR Initial initsync version 3 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker               8          8          8          8           8           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
2.0.101.10        0   200    3441    3029        8    0    0    1d15h          2

RP/0/RP0/CPU0:B-PE-2#
```

## show bgp ipv4 mvpn advertised summary

```
show bgp ipv4 mvpn advertised summary

Mon Jul 14 12:59:26.580 UTC
Network            Next Hop        From            Advertised to
Route Distinguisher: 200:2
Route Distinguisher Version: 8
[1][2.0.101.2]/40  2.0.101.2       Local           2.0.101.10

Processed 1 prefixes, 1 paths
RP/0/RP0/CPU0:B-PE-2#
```

## show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

```
show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

Mon Jul 14 12:59:26.727 UTC
BGP routing table entry for [1][2.0.101.1]/40, Route Distinguisher: 200:2
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                   6            6
Last Modified: Jul 12 21:53:20.541 for 1d15h
Paths: (1 available, best #1, not advertised to EBGP peer)
  Not advertised to any peer
  Path #1: Received by speaker 0
  Not advertised to any peer
  Local
    2.0.101.1 (metric 2) from 2.0.101.10 (2.0.101.1)
      Origin IGP, localpref 100, valid, internal, best, group-best, import-candidate, imported
      Received Path ID 0, Local Path ID 1, version 6
      Community: no-export
      Extended community: RT:200:2 
      Originator: 2.0.101.1, Cluster list: 2.0.101.10
      PMSI: flags 0x00, type 3, label 0, ID 0x02006501efe80001
      Source AFI: IPv4 MVPN, Source VRF: YELLOW, Source Route Distinguisher: 200:2
RP/0/RP0/CPU0:B-PE-2#
```

## show pim vrf YELLOW mdt cache

```
show pim vrf YELLOW mdt cache

Mon Jul 14 12:59:26.883 UTC
No MDT Cache entries found.
RP/0/RP0/CPU0:B-PE-2#
```

## show mrib vrf YELLOW route

```
show mrib vrf YELLOW route

Mon Jul 14 12:59:27.005 UTC

IP Multicast Routing Information Base
Entry flags: L - Domain-Local Source, E - External Source to the Domain,
    C - Directly-Connected Check, S - Signal, IA - Inherit Accept,
    IF - Inherit From, D - Drop, ME - MDT Encap, EID - Encap ID,
    MD - MDT Decap, MT - MDT Threshold Crossed, MH - MDT interface handle
    CD - Conditional Decap, MPLS - MPLS Decap, EX - Extranet
    MoFE - MoFRR Enabled, MoFS - MoFRR State, MoFP - MoFRR Primary
    MoFB - MoFRR Backup, RPFID - RPF ID Set, X - VXLAN
Interface flags: F - Forward, A - Accept, IC - Internal Copy,
    NS - Negate Signal, DP - Don't Preserve, SP - Signal Present,
    II - Internal Interest, ID - Internal Disinterest, LI - Local Interest,
    LD - Local Disinterest, DI - Decapsulation Interface
    EI - Encapsulation Interface, MI - MDT Interface, LVIF - MPLS Encap,
    EX - Extranet, A2 - Secondary Accept, MT - MDT Threshold Crossed,
    MA - Data MDT Assigned, LMI - mLDP MDT Interface, TMI - P2MP-TE MDT Interface
    IRMI - IR MDT Interface, TRMI - TREE SID MDT Interface, MH - Multihome Interface

(*,224.0.0.0/4) RPF nbr: 2.0.101.3 Flags: C RPF P
  Up: 1d15h

(*,224.0.0.0/24) Flags: D P
  Up: 2d01h

(*,224.0.1.39) Flags: S P
  Up: 2d01h

(*,224.0.1.40) Flags: S P
  Up: 2d01h
  Outgoing Interface List
    GigabitEthernet0/0/0/4 Flags: II LI, Up: 1d22h

(*,232.0.0.0/8) Flags: D P
  Up: 2d01h
RP/0/RP0/CPU0:B-PE-2#
```

