# Full Output for Task task-22.alpha.bgp_prefix
**Device:** B-CE-2 (192.168.100.114)
_Generated: 2025-08-07 04:52:48.735279_

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

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
O E2     10.1.1.2/32 [110/1] via 10.10.4.1, 1d01h, GigabitEthernet2
C        10.1.1.4/32 is directly connected, Loopback0
O E2     10.10.2.0/24 [110/1] via 10.10.4.1, 2d00h, GigabitEthernet2
C        10.10.4.0/24 is directly connected, GigabitEthernet2
L        10.10.4.2/32 is directly connected, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.114/32 is directly connected, GigabitEthernet1
B-CE-2#
```

## show ipv6 route

```
show ipv6 route
IPv6 Routing Table - default - 6 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
OE2 2620:FC7:10:102::/64 [110/1]
     via FE80::5054:FF:FE6E:BCD5, GigabitEthernet2
C   2620:FC7:10:104::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:10:104::2/128 [0/0]
     via GigabitEthernet2, receive
OE2 2620:FC7:1011::2/128 [110/1], tag 4000
     via FE80::5054:FF:FE6E:BCD5, GigabitEthernet2
LC  2620:FC7:1011::4/128 [0/0]
     via Loopback0, receive
L   FF00::/8 [0/0]
     via Null0, receive
B-CE-2#
```

