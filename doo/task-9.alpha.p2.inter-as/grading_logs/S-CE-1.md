# Grading Output for Task task-9.alpha.p2.inter-as
**Device:** S-CE-1 (192.168.100.115)
_Generated: 2025-08-06 04:07:03.071947_

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
C        10.1.1.1/32 is directly connected, Loopback0
B        10.1.1.3/32 [20/0] via 10.10.1.1, 00:01:47
B        10.2.1.4/32 [20/0] via 10.10.1.1, 00:01:47
C        10.10.1.0/24 is directly connected, GigabitEthernet2
L        10.10.1.2/32 is directly connected, GigabitEthernet2
B        10.10.3.0/24 [20/0] via 10.10.1.1, 00:01:47
B        10.20.1.0/24 [20/0] via 10.10.1.1, 00:00:59
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.115/32 is directly connected, GigabitEthernet1
S-CE-1#
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
B   2620:FC7:2:1::4/128 [20/0], tag 100
     via FE80::5054:FF:FE56:818F, GigabitEthernet2
C   2620:FC7:10:101::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:10:101::2/128 [0/0]
     via GigabitEthernet2, receive
B   2620:FC7:10:103::/64 [20/0], tag 100
     via FE80::5054:FF:FE56:818F, GigabitEthernet2
B   2620:FC7:10:201::/64 [20/0], tag 100
     via FE80::5054:FF:FE56:818F, GigabitEthernet2
LC  2620:FC7:1011::1/128 [0/0]
     via Loopback0, receive
B   2620:FC7:1011::3/128 [20/0], tag 100
     via FE80::5054:FF:FE56:818F, GigabitEthernet2
L   FF00::/8 [0/0]
     via Null0, receive
S-CE-1#
```

## ping 10.2.1.4 source loopback 0

```
ping 10.2.1.4 source loopback 0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.2.1.4, timeout is 2 seconds:
Packet sent with a source address of 10.1.1.1 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 12/16/22 ms
S-CE-1#
```

