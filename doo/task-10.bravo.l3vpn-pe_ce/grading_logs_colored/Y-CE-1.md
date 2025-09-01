# Grading Output for Task task-10.bravo.l3vpn-pe_ce
**Device:** Y-CE-1 (192.168.100.127)
_Generated: 2025-08-06 10:51:03.799963_

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

      10.0.0.0/8 is variably subnetted, 8 subnets, 2 masks
C        10.2.1.1/32 is directly connected, Loopback0
O E2     10.2.1.2/32 [110/1] via 10.20.4.1, 00:12:23, GigabitEthernet2
O IA     10.2.1.3/32 [110/3] via 10.20.4.1, 00:13:02, GigabitEthernet2
O IA     10.20.2.0/24 [110/2] via 10.20.4.1, 00:13:06, GigabitEthernet2
C        10.20.4.0/24 is directly connected, GigabitEthernet2
L        10.20.4.2/32 is directly connected, GigabitEthernet2
O E2     10.20.5.0/24 [110/20] via 10.20.4.1, 00:13:06, GigabitEthernet2
O E2     10.20.6.0/24 [110/1] via 10.20.4.1, 00:13:06, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.127/32 is directly connected, GigabitEthernet1
Y-CE-1#
```

## show ipv6 route

```
show ipv6 route
IPv6 Routing Table - default - 9 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
LC  2620:FC7:2:1::1/128 [0/0]
     via Loopback0, receive
OE2 2620:FC7:2:1::2/128 [110/1], tag 2000
     via FE80::5054:FF:FE3B:173B, GigabitEthernet2
OI  2620:FC7:2:1::3/128 [110/2]
     via FE80::5054:FF:FE3B:173B, GigabitEthernet2
OI  2620:FC7:20:2::/64 [110/2]
     via FE80::5054:FF:FE3B:173B, GigabitEthernet2
C   2620:FC7:20:4::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:20:4::2/128 [0/0]
     via GigabitEthernet2, receive
OE2 2620:FC7:20:5::/64 [110/20]
     via FE80::5054:FF:FE3B:173B, GigabitEthernet2
OE2 2620:FC7:20:6::/64 [110/1]
     via FE80::5054:FF:FE3B:173B, GigabitEthernet2
L   FF00::/8 [0/0]
     via Null0, receive
Y-CE-1#
```

## ping ip 10.2.1.3 source Loopback0 repeat 5 timeout 2

```
ping ip 10.2.1.3 source Loopback0 repeat 5 timeout 2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.2.1.3, timeout is 2 seconds:
Packet sent with a source address of 10.2.1.1 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 8/9/12 ms
Y-CE-1#
```

## ping 2620:fc7:20:2::2 source loopback0

```
ping 2620:fc7:20:2::2 source loopback0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 2620:FC7:20:2::2, timeout is 2 seconds:
Packet sent with a source address of 2620:FC7:2:1::1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 9/13/22 ms
Y-CE-1#
```

## ping 2620:fc7:20:5::2 source loopback0

```
ping 2620:fc7:20:5::2 source loopback0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 2620:FC7:20:5::2, timeout is 2 seconds:
Packet sent with a source address of 2620:FC7:2:1::1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 3/3/5 ms
Y-CE-1#
```

## show ip ospf neighbor

```
show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.0.101.1         1   FULL/BDR        00:00:36    10.20.4.1       GigabitEthernet2
Y-CE-1#
```

