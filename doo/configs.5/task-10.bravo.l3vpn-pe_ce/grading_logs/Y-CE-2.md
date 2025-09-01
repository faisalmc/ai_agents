# Grading Output for Task task-10.bravo.l3vpn-pe_ce
**Device:** Y-CE-2 (192.168.100.128)
_Generated: 2025-08-06 10:51:12.061082_

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

      10.0.0.0/8 is variably subnetted, 9 subnets, 2 masks
B        10.2.1.1/32 [20/0] via 10.20.6.1, 00:12:31
C        10.2.1.2/32 is directly connected, Loopback0
B        10.2.1.3/32 [20/0] via 10.20.5.1, 00:12:31
B        10.20.2.0/24 [20/0] via 10.20.5.1, 00:12:31
B        10.20.4.0/24 [20/0] via 10.20.5.1, 00:12:31
C        10.20.5.0/24 is directly connected, GigabitEthernet2
L        10.20.5.2/32 is directly connected, GigabitEthernet2
C        10.20.6.0/24 is directly connected, GigabitEthernet3
L        10.20.6.2/32 is directly connected, GigabitEthernet3
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.128/32 is directly connected, GigabitEthernet1
Y-CE-2#
```

## show ipv6 route

```
show ipv6 route
IPv6 Routing Table - default - 10 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
B   2620:FC7:2:1::1/128 [20/0], tag 200
     via FE80::5054:FF:FE64:4AE4, GigabitEthernet3
LC  2620:FC7:2:1::2/128 [0/0]
     via Loopback0, receive
B   2620:FC7:2:1::3/128 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
B   2620:FC7:20:2::/64 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
B   2620:FC7:20:4::/64 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
C   2620:FC7:20:5::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:20:5::2/128 [0/0]
     via GigabitEthernet2, receive
C   2620:FC7:20:6::/64 [0/0]
     via GigabitEthernet3, directly connected
L   2620:FC7:20:6::2/128 [0/0]
     via GigabitEthernet3, receive
L   FF00::/8 [0/0]
     via Null0, receive
Y-CE-2#
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

      10.0.0.0/8 is variably subnetted, 9 subnets, 2 masks
B        10.2.1.1/32 [20/0] via 10.20.6.1, 00:12:31
C        10.2.1.2/32 is directly connected, Loopback0
B        10.2.1.3/32 [20/0] via 10.20.5.1, 00:12:31
B        10.20.2.0/24 [20/0] via 10.20.5.1, 00:12:31
B        10.20.4.0/24 [20/0] via 10.20.5.1, 00:12:31
C        10.20.5.0/24 is directly connected, GigabitEthernet2
L        10.20.5.2/32 is directly connected, GigabitEthernet2
C        10.20.6.0/24 is directly connected, GigabitEthernet3
L        10.20.6.2/32 is directly connected, GigabitEthernet3
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.128/32 is directly connected, GigabitEthernet1
Y-CE-2#
```

## show ipv6 route

```
show ipv6 route
IPv6 Routing Table - default - 10 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
B   2620:FC7:2:1::1/128 [20/0], tag 200
     via FE80::5054:FF:FE64:4AE4, GigabitEthernet3
LC  2620:FC7:2:1::2/128 [0/0]
     via Loopback0, receive
B   2620:FC7:2:1::3/128 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
B   2620:FC7:20:2::/64 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
B   2620:FC7:20:4::/64 [20/0], tag 200
     via FE80::5054:FF:FE87:B731, GigabitEthernet2
C   2620:FC7:20:5::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:20:5::2/128 [0/0]
     via GigabitEthernet2, receive
C   2620:FC7:20:6::/64 [0/0]
     via GigabitEthernet3, directly connected
L   2620:FC7:20:6::2/128 [0/0]
     via GigabitEthernet3, receive
L   FF00::/8 [0/0]
     via Null0, receive
Y-CE-2#
```

## show ip bgp neighbor

```
show ip bgp neighbor
BGP neighbor is 10.20.5.1,  remote AS 200, external link
  BGP version 4, remote router ID 2.0.101.1
  BGP state = Established, up for 00:13:39
  Last read 00:00:37, last write 00:00:36, hold time is 180, keepalive interval is 60 seconds
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
    Updates:                5          7
    Keepalives:            15         13
    Route Refresh:          0          0
    Total:                 21         21
  Do log neighbor state changes (via global configuration)
  Default minimum time between advertisement runs is 30 seconds

 For address family: IPv4 Unicast
  Session: 10.20.5.1
  BGP table version 8, neighbor version 8/0
  Output queue size : 0
  Index 1, Advertise bit 0
  1 update-group member
  Slow-peer detection is disabled
  Slow-peer split-update-group dynamic is disabled
                                 Sent       Rcvd
  Prefix activity:               ----       ----
    Prefixes Current:               7          6 (Consumes 816 bytes)
    Prefixes Total:                 7          6
    Implicit Withdraw:              0          0
    Explicit Withdraw:              0          0
    Used as bestpath:             n/a          5
    Used as multipath:            n/a          0
    Used as secondary:            n/a          0

                                   Outbound    Inbound
  Local Policy Denied Prefixes:    --------    -------
    Total:                                0          0
  Number of NLRIs in the update sent: max 3, min 0
  Current session network count peaked at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.877 ago)
  Highest network count observed at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.877 ago)
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

  Address tracking is enabled, the RIB does have a route to 10.20.5.1
  Route to peer address reachability Up: 1; Down: 0
    Last notification 00:13:52
  Connections established 1; dropped 0
  Last reset never
  External BGP neighbor configured for connected checks (single-hop no-disable-connected-check)
  Interface associated: GigabitEthernet2 (peering address in same link)
  Transport(tcp) path-mtu-discovery is enabled
  Graceful-Restart is disabled
  SSO is disabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0            
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.20.5.2, Local port: 16014
Foreign host: 10.20.5.1, Foreign port: 179
Connection tableid (VRF): 0
Maximum output segment queue size: 50

Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

Event Timers (current time is 0xC2FBAEB):
Timer          Starts    Wakeups            Next
Retrans            18          1             0x0
TimeWait            0          0             0x0
AckHold            19         17             0x0
SendWnd             0          0             0x0
KeepAlive           0          0             0x0
GiveUp              0          0             0x0
PmtuAger          115        114       0xC2FBC5D
DeadWait            0          0             0x0
Linger              0          0             0x0
ProcessQ            0          0             0x0

iss: 2949343651  snduna: 2949344239  sndnxt: 2949344239
irs:  636085387  rcvnxt:  636086016

sndwnd:  32238  scale:      0  maxrcvwnd:  16384
rcvwnd:  15756  scale:      0  delrcvwnd:    628

SRTT: 882 ms, RTTO: 1768 ms, RTV: 886 ms, KRTT: 0 ms
minRTT: 6 ms, maxRTT: 1000 ms, ACK hold: 200 ms
uptime: 822139 ms, Sent idletime: 36642 ms, Receive idletime: 36436 ms 
Status Flags: active open
Option Flags: nagle, path mtu capable
IP Precedence value : 6

Datagrams (max data segment is 1460 bytes):
Rcvd: 34 (out of order: 0), with data: 18, total data bytes: 628
Sent: 36 (retransmit: 1, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 17, total data bytes: 587

 Packets received in fast path: 0, fast processed: 0, slow path: 0
 fast lock acquisition failures: 0, slow path: 0
TCP Semaphore      0x7FEDCF833618  FREE 

BGP neighbor is 10.20.6.1,  remote AS 200, external link
  BGP version 4, remote router ID 2.0.101.2
  BGP state = Established, up for 00:13:41
  Last read 00:00:10, last write 00:00:52, hold time is 180, keepalive interval is 60 seconds
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
    Updates:                5          7
    Keepalives:            15         15
    Route Refresh:          0          0
    Total:                 21         23
  Do log neighbor state changes (via global configuration)
  Default minimum time between advertisement runs is 30 seconds

 For address family: IPv4 Unicast
  Session: 10.20.6.1
  BGP table version 8, neighbor version 8/0
  Output queue size : 0
  Index 1, Advertise bit 0
  1 update-group member
  Slow-peer detection is disabled
  Slow-peer split-update-group dynamic is disabled
                                 Sent       Rcvd
  Prefix activity:               ----       ----
    Prefixes Current:               7          6 (Consumes 816 bytes)
    Prefixes Total:                 7          6
    Implicit Withdraw:              0          0
    Explicit Withdraw:              0          0
    Used as bestpath:             n/a          1
    Used as multipath:            n/a          0
    Used as secondary:            n/a          0

                                   Outbound    Inbound
  Local Policy Denied Prefixes:    --------    -------
    Total:                                0          0
  Number of NLRIs in the update sent: max 3, min 0
  Current session network count peaked at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.878 ago)
  Highest network count observed at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.878 ago)
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

  Address tracking is enabled, the RIB does have a route to 10.20.6.1
  Route to peer address reachability Up: 1; Down: 0
    Last notification 00:13:52
  Connections established 1; dropped 0
  Last reset never
  External BGP neighbor configured for connected checks (single-hop no-disable-connected-check)
  Interface associated: GigabitEthernet3 (peering address in same link)
  Transport(tcp) path-mtu-discovery is enabled
  Graceful-Restart is disabled
  SSO is disabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0            
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.20.6.2, Local port: 23886
Foreign host: 10.20.6.1, Foreign port: 179
Connection tableid (VRF): 0
Maximum output segment queue size: 50

Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

Event Timers (current time is 0xC2FBAEC):
Timer          Starts    Wakeups            Next
Retrans            18          1             0x0
TimeWait            0          0             0x0
AckHold            19         17             0x0
SendWnd             0          0             0x0
KeepAlive           0          0             0x0
GiveUp              0          0             0x0
PmtuAger          118        117       0xC2FBE09
DeadWait            0          0             0x0
Linger              0          0             0x0
ProcessQ            0          0             0x0

iss:   34554809  snduna:   34555397  sndnxt:   34555397
irs: 3960156455  rcvnxt: 3960157108

sndwnd:  32238  scale:      0  maxrcvwnd:  16384
rcvwnd:  15732  scale:      0  delrcvwnd:    652

SRTT: 882 ms, RTTO: 1768 ms, RTV: 886 ms, KRTT: 0 ms
minRTT: 9 ms, maxRTT: 1000 ms, ACK hold: 200 ms
uptime: 824141 ms, Sent idletime: 9830 ms, Receive idletime: 10030 ms 
Status Flags: active open
Option Flags: nagle, path mtu capable
IP Precedence value : 6

Datagrams (max data segment is 1460 bytes):
Rcvd: 35 (out of order: 0), with data: 18, total data bytes: 652
Sent: 36 (retransmit: 1, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 17, total data bytes: 587

 Packets received in fast path: 0, fast processed: 0, slow path: 0
 fast lock acquisition failures: 0, slow path: 0
TCP Semaphore      0x7FEDCF8336E8  FREE 

Y-CE-2#
```

## show bgp neighbor

```
show bgp neighbor
% Command accepted but obsolete, unreleased or unsupported; see documentation.

BGP neighbor is 10.20.5.1,  remote AS 200, external link
  BGP version 4, remote router ID 2.0.101.1
  BGP state = Established, up for 00:13:39
  Last read 00:00:37, last write 00:00:36, hold time is 180, keepalive interval is 60 seconds
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
    Updates:                5          7
    Keepalives:            15         13
    Route Refresh:          0          0
    Total:                 21         21
  Do log neighbor state changes (via global configuration)
  Default minimum time between advertisement runs is 30 seconds

 For address family: IPv4 Unicast
  Session: 10.20.5.1
  BGP table version 8, neighbor version 8/0
  Output queue size : 0
  Index 1, Advertise bit 0
  1 update-group member
  Slow-peer detection is disabled
  Slow-peer split-update-group dynamic is disabled
                                 Sent       Rcvd
  Prefix activity:               ----       ----
    Prefixes Current:               7          6 (Consumes 816 bytes)
    Prefixes Total:                 7          6
    Implicit Withdraw:              0          0
    Explicit Withdraw:              0          0
    Used as bestpath:             n/a          5
    Used as multipath:            n/a          0
    Used as secondary:            n/a          0

                                   Outbound    Inbound
  Local Policy Denied Prefixes:    --------    -------
    Total:                                0          0
  Number of NLRIs in the update sent: max 3, min 0
  Current session network count peaked at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.944 ago)
  Highest network count observed at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.944 ago)
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

  Address tracking is enabled, the RIB does have a route to 10.20.5.1
  Route to peer address reachability Up: 1; Down: 0
    Last notification 00:13:52
  Connections established 1; dropped 0
  Last reset never
  External BGP neighbor configured for connected checks (single-hop no-disable-connected-check)
  Interface associated: GigabitEthernet2 (peering address in same link)
  Transport(tcp) path-mtu-discovery is enabled
  Graceful-Restart is disabled
  SSO is disabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0            
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.20.5.2, Local port: 16014
Foreign host: 10.20.5.1, Foreign port: 179
Connection tableid (VRF): 0
Maximum output segment queue size: 50

Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

Event Timers (current time is 0xC2FBB2E):
Timer          Starts    Wakeups            Next
Retrans            18          1             0x0
TimeWait            0          0             0x0
AckHold            19         17             0x0
SendWnd             0          0             0x0
KeepAlive           0          0             0x0
GiveUp              0          0             0x0
PmtuAger          115        114       0xC2FBC5D
DeadWait            0          0             0x0
Linger              0          0             0x0
ProcessQ            0          0             0x0

iss: 2949343651  snduna: 2949344239  sndnxt: 2949344239
irs:  636085387  rcvnxt:  636086016

sndwnd:  32238  scale:      0  maxrcvwnd:  16384
rcvwnd:  15756  scale:      0  delrcvwnd:    628

SRTT: 882 ms, RTTO: 1768 ms, RTV: 886 ms, KRTT: 0 ms
minRTT: 6 ms, maxRTT: 1000 ms, ACK hold: 200 ms
uptime: 822206 ms, Sent idletime: 36709 ms, Receive idletime: 36503 ms 
Status Flags: active open
Option Flags: nagle, path mtu capable
IP Precedence value : 6

Datagrams (max data segment is 1460 bytes):
Rcvd: 34 (out of order: 0), with data: 18, total data bytes: 628
Sent: 36 (retransmit: 1, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 17, total data bytes: 587

 Packets received in fast path: 0, fast processed: 0, slow path: 0
 fast lock acquisition failures: 0, slow path: 0
TCP Semaphore      0x7FEDCF833618  FREE 

BGP neighbor is 10.20.6.1,  remote AS 200, external link
  BGP version 4, remote router ID 2.0.101.2
  BGP state = Established, up for 00:13:41
  Last read 00:00:10, last write 00:00:52, hold time is 180, keepalive interval is 60 seconds
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
    Updates:                5          7
    Keepalives:            15         15
    Route Refresh:          0          0
    Total:                 21         23
  Do log neighbor state changes (via global configuration)
  Default minimum time between advertisement runs is 30 seconds

 For address family: IPv4 Unicast
  Session: 10.20.6.1
  BGP table version 8, neighbor version 8/0
  Output queue size : 0
  Index 1, Advertise bit 0
  1 update-group member
  Slow-peer detection is disabled
  Slow-peer split-update-group dynamic is disabled
                                 Sent       Rcvd
  Prefix activity:               ----       ----
    Prefixes Current:               7          6 (Consumes 816 bytes)
    Prefixes Total:                 7          6
    Implicit Withdraw:              0          0
    Explicit Withdraw:              0          0
    Used as bestpath:             n/a          1
    Used as multipath:            n/a          0
    Used as secondary:            n/a          0

                                   Outbound    Inbound
  Local Policy Denied Prefixes:    --------    -------
    Total:                                0          0
  Number of NLRIs in the update sent: max 3, min 0
  Current session network count peaked at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.944 ago)
  Highest network count observed at 6 entries at 14:37:59 Aug 6 2025 UTC (00:13:10.944 ago)
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

  Address tracking is enabled, the RIB does have a route to 10.20.6.1
  Route to peer address reachability Up: 1; Down: 0
    Last notification 00:13:52
  Connections established 1; dropped 0
  Last reset never
  External BGP neighbor configured for connected checks (single-hop no-disable-connected-check)
  Interface associated: GigabitEthernet3 (peering address in same link)
  Transport(tcp) path-mtu-discovery is enabled
  Graceful-Restart is disabled
  SSO is disabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0            
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.20.6.2, Local port: 23886
Foreign host: 10.20.6.1, Foreign port: 179
Connection tableid (VRF): 0
Maximum output segment queue size: 50

Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

Event Timers (current time is 0xC2FBB2E):
Timer          Starts    Wakeups            Next
Retrans            18          1             0x0
TimeWait            0          0             0x0
AckHold            19         17             0x0
SendWnd             0          0             0x0
KeepAlive           0          0             0x0
GiveUp              0          0             0x0
PmtuAger          118        117       0xC2FBE09
DeadWait            0          0             0x0
Linger              0          0             0x0
ProcessQ            0          0             0x0

iss:   34554809  snduna:   34555397  sndnxt:   34555397
irs: 3960156455  rcvnxt: 3960157108

sndwnd:  32238  scale:      0  maxrcvwnd:  16384
rcvwnd:  15732  scale:      0  delrcvwnd:    652

SRTT: 882 ms, RTTO: 1768 ms, RTV: 886 ms, KRTT: 0 ms
minRTT: 9 ms, maxRTT: 1000 ms, ACK hold: 200 ms
uptime: 824207 ms, Sent idletime: 9896 ms, Receive idletime: 10096 ms 
Status Flags: active open
Option Flags: nagle, path mtu capable
IP Precedence value : 6

Datagrams (max data segment is 1460 bytes):
Rcvd: 35 (out of order: 0), with data: 18, total data bytes: 652
Sent: 36 (retransmit: 1, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 17, total data bytes: 587

 Packets received in fast path: 0, fast processed: 0, slow path: 0
 fast lock acquisition failures: 0, slow path: 0
TCP Semaphore      0x7FEDCF8336E8  FREE 

Y-CE-2#
```

