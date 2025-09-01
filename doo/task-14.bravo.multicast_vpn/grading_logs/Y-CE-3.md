# Grading Output for Task task-14.bravo.multicast_vpn/

# ping 224.1.1.1 source loopback0 repeat 1

```
Y-CE-3# ping 224.1.1.1 source loopback0 repeat 1
Type escape sequence to abort.
Sending 1, 100-byte ICMP Echos to 224.1.1.1, timeout is 2 seconds:
Packet sent with a source address of 10.2.1.3 

Reply to request 0 from 10.20.4.2, 7 ms
Reply to request 0 from 10.20.4.2, 7 ms

```
# show ip mroute

```
Y-CE-3#show ip mroute
IP Multicast Routing Table
Flags: D - Dense, S - Sparse, B - Bidir Group, s - SSM Group, C - Connected,
       L - Local, P - Pruned, R - RP-bit set, F - Register flag,
       T - SPT-bit set, J - Join SPT, M - MSDP created entry, E - Extranet,
       X - Proxy Join Timer Running, A - Candidate for MSDP Advertisement,
       U - URD, I - Received Source Specific Host Report, 
       Z - Multicast Tunnel, z - MDT-data group sender, 
       Y - Joined MDT-data group, y - Sending to MDT-data group, 
       G - Received BGP C-Mroute, g - Sent BGP C-Mroute, 
       N - Received BGP Shared-Tree Prune, n - BGP C-Mroute suppressed, 
       Q - Received BGP S-A Route, q - Sent BGP S-A Route, 
       V - RD & Vector, v - Vector, p - PIM Joins on route, 
       x - VxLAN group, c - PFP-SA cache created entry, 
       * - determined by Assert, # - iif-starg configured on rpf intf, 
       e - encap-helper tunnel flag, l - LISP Decap Refcnt Contributor
Outgoing interface flags: H - Hardware switched, A - Assert winner, p - PIM Join
 Timers: Uptime/Expires
 Interface state: Interface, Next-Hop or VCD, State/Mode

(*, 224.1.1.1), 00:04:23/00:03:07, RP 10.2.1.3, flags: SF
  Incoming interface: Null, RPF nbr 0.0.0.0
  Outgoing interface list:
    GigabitEthernet2, Forward/Sparse, 00:04:23/00:03:07
          
(10.2.1.3, 224.1.1.1), 00:00:46/00:02:52, flags: FT
  Incoming interface: Loopback0, RPF nbr 0.0.0.0
  Outgoing interface list:
    GigabitEthernet2, Forward/Sparse, 00:00:46/00:03:07, A

(*, 224.0.1.40), 00:06:26/00:02:41, RP 0.0.0.0, flags: DCL
  Incoming interface: Null, RPF nbr 0.0.0.0
  Outgoing interface list:
    GigabitEthernet2, Forward/Sparse, 00:06:24/00:02:41
    Loopback0, Forward/Sparse, 00:06:24/00:02:37
```

