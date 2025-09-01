# Full Output for Task task-9.alpha.p2.inter-as
**Device:** S-CE-3 (192.168.100.130)
_Generated: 2025-08-06 04:07:28.339344_

## show run | sec bgp

```
show run | sec bgp
router bgp 1003
 bgp router-id 10.2.1.4
 bgp log-neighbor-changes
 neighbor 10.20.1.1 remote-as 200
 neighbor 2620:FC7:10:201::1 remote-as 200
 !
 address-family ipv4
  network 10.2.1.4 mask 255.255.255.255
  neighbor 10.20.1.1 activate
  no neighbor 2620:FC7:10:201::1 activate
 exit-address-family
 !
 address-family ipv6
  network 2620:FC7:2:1::4/128
  network 2620:FC7:1021::4/128
  neighbor 2620:FC7:10:201::1 activate
 exit-address-family
S-CE-3#
```

## show ip bgp neighbors

```
show ip bgp neighbors
BGP neighbor is 10.20.1.1,  remote AS 200, external link
  BGP version 4, remote router ID 2.0.101.4
  BGP state = Established, up for 00:01:40
  Last read 00:00:35, last write 00:00:01, hold time is 180, keepalive interval is 60 seconds
  Neighbor sessions:
    1 active, is not multisession capable (disabled)
  Neighbor capabilities:
    Route refresh: advertised and received(new)
    Four-octets ASN Capability: advertised and received
    Address family IPv4 Unicast: advertised and received
    Enhanced Refresh Capability: advertised
    Multisession Capability: 
    Stateful switchover support enabled: NO for session 1
  Message statistics:
    InQ depth is 0
    OutQ depth is 0
    
                         Sent       Rcvd
    Opens:                  1          1
    Notifications:          0          0
    Updates:                2          5
    Keepalives:             4          2
    Route Refresh:          0          0
    Total:                  7          8
  Do log neighbor state changes (via global configuration)
  Default minimum time between advertisement runs is 30 seconds

 For address family: IPv4 Unicast
  Session: 10.20.1.1
  BGP table version 19, neighbor version 19/0
  Output queue size : 0
  Index 2, Advertise bit 0
  2 update-group member
  Slow-peer detection is disabled
  Slow-peer split-update-group dynamic is disabled
                                 Sent       Rcvd
  Prefix activity:               ----       ----
    Prefixes Current:               1          5 (Consumes 680 bytes)
    Prefixes Total:                 1          5
    Implicit Withdraw:              0          0
    Explicit Withdraw:              0          0
    Used as bestpath:             n/a          5
    Used as multipath:            n/a          0
    Used as secondary:            n/a          0

                                   Outbound    Inbound
  Local Policy Denied Prefixes:    --------    -------
    Bestpath from this peer:              5        n/a
    Total:                                5          0
  Number of NLRIs in the update sent: max 1, min 0
  Current session network count peaked at 5 entries at 08:05:51 Aug 6 2025 UTC (00:01:35.411 ago)
  Highest network count observed at 5 entries at 07:50:03 Aug 6 2025 UTC (00:17:23.411 ago)
  Last detected as dynamic slow peer: never
  Dynamic slow peer recovered: never
  Refresh Epoch: 1
  Last Sent Refresh Start-of-rib: never
  Last Sent Refresh End-of-rib: never
  Last Received Refresh Start-of-rib: never
  Last Received Refresh End-of-rib: never
				       Sent	  Rcvd
	Refresh activity:	       ----	  ----
	  Refresh Start-of-RIB          0          0
	  Refresh End-of-RIB            0          0

  Address tracking is enabled, the RIB does have a route to 10.20.1.1
  Route to peer address reachability Up: 1; Down: 0
    Last notification 00:18:26
  Connections established 2; dropped 1
  Last reset 00:01:54, due to Peer closed the session of session 1
  External BGP neighbor configured for connected checks (single-hop no-disable-connected-check)
  Interface associated: GigabitEthernet2 (peering address in same link)
  Transport(tcp) path-mtu-discovery is enabled
  Graceful-Restart is disabled
  SSO is disabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0            
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.20.1.2, Local port: 32985
Foreign host: 10.20.1.1, Foreign port: 179
Connection tableid (VRF): 0
Maximum output segment queue size: 50

Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

Event Timers (current time is 0xABE8609):
Timer          Starts    Wakeups            Next
Retrans             6          1             0x0
TimeWait            0          0             0x0
AckHold             4          2             0x0
SendWnd             0          0             0x0
KeepAlive           0          0             0x0
GiveUp              0          0             0x0
PmtuAger            1          0       0xAC61B73
DeadWait            0          0             0x0
Linger              0          0             0x0
ProcessQ            0          0             0x0

iss:  522076877  snduna:  522077089  sndnxt:  522077089
irs: 2363295394  rcvnxt: 2363295730

sndwnd:  32614  scale:      0  maxrcvwnd:  16384
rcvwnd:  16049  scale:      0  delrcvwnd:    335

SRTT: 413 ms, RTTO: 3205 ms, RTV: 2792 ms, KRTT: 0 ms
minRTT: 9 ms, maxRTT: 1000 ms, ACK hold: 200 ms
uptime: 103007 ms, Sent idletime: 1620 ms, Receive idletime: 1414 ms 
Status Flags: active open
Option Flags: nagle, path mtu capable
IP Precedence value : 6

Datagrams (max data segment is 1460 bytes):
Rcvd: 8 (out of order: 0), with data: 3, total data bytes: 335
Sent: 10 (retransmit: 1, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 6, total data bytes: 211

 Packets received in fast path: 0, fast processed: 0, slow path: 0
 fast lock acquisition failures: 0, slow path: 0
TCP Semaphore      0x7FB9C79C0C38  FREE 

S-CE-3#
```

## show ip route

```
show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR
       & - replicated local route overrides by connected

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
B        10.1.1.1/32 [20/0] via 10.20.1.1, 00:01:36
B        10.1.1.3/32 [20/0] via 10.20.1.1, 00:01:36
C        10.2.1.4/32 is directly connected, Loopback0
B        10.10.1.0/24 [20/0] via 10.20.1.1, 00:01:36
B        10.10.3.0/24 [20/0] via 10.20.1.1, 00:01:36
C        10.20.1.0/24 is directly connected, GigabitEthernet2
L        10.20.1.2/32 is directly connected, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.130/32 is directly connected, GigabitEthernet1
S-CE-3#
```

## show ipv6 route

```
show ipv6 route
IPv6 Routing Table - default - 8 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
LC  2620:FC7:2:1::4/128 [0/0]
     via Loopback0, receive
B   2620:FC7:10:101::/64 [20/0], tag 200
     via FE80::5054:FF:FEA6:5272, GigabitEthernet2
B   2620:FC7:10:103::/64 [20/0], tag 200
     via FE80::5054:FF:FEA6:5272, GigabitEthernet2
C   2620:FC7:10:201::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:10:201::2/128 [0/0]
     via GigabitEthernet2, receive
B   2620:FC7:1011::1/128 [20/0], tag 200
     via FE80::5054:FF:FEA6:5272, GigabitEthernet2
B   2620:FC7:1011::3/128 [20/0], tag 200
     via FE80::5054:FF:FEA6:5272, GigabitEthernet2
L   FF00::/8 [0/0]
     via Null0, receive
S-CE-3#
```

