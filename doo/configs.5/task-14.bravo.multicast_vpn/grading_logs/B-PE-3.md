# Grading Output for Task task-14.bravo.multicast_vpn/
**Device:** B-PE-3 (192.168.100.119)
_Generated: 2025-08-07 01:49:02.521627_

## show mrib vrf YELLOW route

```
show mrib vrf YELLOW route

Thu Aug  7 05:48:58.598 UTC

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

(*,224.0.0.0/4) RPF nbr: 10.20.2.2 Flags: C RPF P
  Up: 00:12:46

(*,224.0.0.0/24) Flags: D P
  Up: 00:12:59

(*,224.0.1.39) Flags: S P
  Up: 00:12:59

(*,224.0.1.40) Flags: S P
  Up: 00:12:59
  Outgoing Interface List
    GigabitEthernet0/0/0/1 Flags: II LI, Up: 00:12:59

(*,224.1.1.1) RPF nbr: 10.20.2.2 Flags: C RPF
  Up: 00:10:45
  Incoming Interface List
    GigabitEthernet0/0/0/1 Flags: A, Up: 00:10:45
  Outgoing Interface List
    mdtYELLOW Flags: F NS MI, Up: 00:10:45

(10.2.1.3,224.1.1.1) RPF nbr: 10.20.2.2 Flags: RPF
  Up: 00:07:08
  Incoming Interface List
    GigabitEthernet0/0/0/1 Flags: A, Up: 00:07:08
  Outgoing Interface List
    mdtYELLOW Flags: F NS MI, Up: 00:07:08

(*,232.0.0.0/8) Flags: D P
  Up: 00:12:59
RP/0/RP0/CPU0:B-PE-3#
```

## show bgp ipv4 mvpn summary

```
show bgp ipv4 mvpn summary

Thu Aug  7 05:48:58.727 UTC
BGP router identifier 2.0.101.3, local AS number 200
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0x0
BGP table nexthop route policy: 
BGP main routing table version 7
BGP NSR Initial initsync version 6 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker               7          7          7          7           7           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
2.0.101.10        0   200    3368    2955        7    0    0 00:12:51          2

RP/0/RP0/CPU0:B-PE-3#
```

## show mrib route

```
show mrib route

Thu Aug  7 05:48:58.995 UTC

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

(*,224.0.0.0/24) Flags: D P
  Up: 00:13:00

(*,224.0.1.39) Flags: S P
  Up: 00:13:00

(*,224.0.1.40) Flags: S P
  Up: 00:13:00
  Outgoing Interface List
    Loopback0 Flags: II LI, Up: 00:13:00

(*,232.0.0.0/8) Flags: D P
  Up: 00:13:00

(*,239.232.0.0/16) Flags: D P
  Up: 00:13:00

(2.0.101.1,239.232.0.1) RPF nbr: 2.2.5.2 Flags: RPF MD MH CD
  MVPN TID: 0xe0000001
  MVPN Remote TID: 0x0
  MVPN Payload: IPv4
  MDT IFH: 0x1c
  Up: 00:10:58
  Incoming Interface List
    GigabitEthernet0/0/0/0 Flags: A, Up: 00:10:58
  Outgoing Interface List
    Loopback0 Flags: F NS, Up: 00:10:58

(2.0.101.2,239.232.0.1) RPF nbr: 2.2.5.2 Flags: RPF MD MH CD
  MVPN TID: 0xe0000001
  MVPN Remote TID: 0x0
  MVPN Payload: IPv4
  MDT IFH: 0x1c
  Up: 00:10:58
  Incoming Interface List
    GigabitEthernet0/0/0/0 Flags: A, Up: 00:10:58
  Outgoing Interface List
    Loopback0 Flags: F NS, Up: 00:10:58

(2.0.101.3,239.232.0.1) RPF nbr: 2.0.101.3 Flags: RPF ME MH
  MVPN TID: 0xe0000001
  MVPN Remote TID: 0x0
  MVPN Payload: IPv4
  MDT IFH: 0x1c
  Up: 00:13:00
  Incoming Interface List
    Loopback0 Flags: F A, Up: 00:13:00
  Outgoing Interface List
    Loopback0 Flags: F A, Up: 00:13:00
    GigabitEthernet0/0/0/0 Flags: F NS, Up: 00:10:58
RP/0/RP0/CPU0:B-PE-3#
```

