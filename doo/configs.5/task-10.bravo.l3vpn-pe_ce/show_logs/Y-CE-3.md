# Full Output for Task task-10.bravo.l3vpn-pe_ce
**Device:** Y-CE-3 (192.168.100.129)
_Generated: 2025-08-06 10:51:13.441352_

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
O IA     10.2.1.1/32 [110/3] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.2.1.2/32 [110/1] via 10.20.2.1, 00:12:33, GigabitEthernet2
C        10.2.1.3/32 is directly connected, Loopback0
C        10.20.2.0/24 is directly connected, GigabitEthernet2
L        10.20.2.2/32 is directly connected, GigabitEthernet2
O IA     10.20.4.0/24 [110/2] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.20.5.0/24 [110/1] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.20.6.0/24 [110/1] via 10.20.2.1, 00:13:11, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.129/32 is directly connected, GigabitEthernet1
Y-CE-3#
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
OI  2620:FC7:2:1::1/128 [110/2]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:2:1::2/128 [110/1], tag 2000
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
LC  2620:FC7:2:1::3/128 [0/0]
     via Loopback0, receive
C   2620:FC7:20:2::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:20:2::2/128 [0/0]
     via GigabitEthernet2, receive
OI  2620:FC7:20:4::/64 [110/2]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:20:5::/64 [110/1]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:20:6::/64 [110/1]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
L   FF00::/8 [0/0]
     via Null0, receive
Y-CE-3#
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

      10.0.0.0/8 is variably subnetted, 8 subnets, 2 masks
O IA     10.2.1.1/32 [110/3] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.2.1.2/32 [110/1] via 10.20.2.1, 00:12:33, GigabitEthernet2
C        10.2.1.3/32 is directly connected, Loopback0
C        10.20.2.0/24 is directly connected, GigabitEthernet2
L        10.20.2.2/32 is directly connected, GigabitEthernet2
O IA     10.20.4.0/24 [110/2] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.20.5.0/24 [110/1] via 10.20.2.1, 00:13:11, GigabitEthernet2
O E2     10.20.6.0/24 [110/1] via 10.20.2.1, 00:13:11, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.129/32 is directly connected, GigabitEthernet1
Y-CE-3#
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
OI  2620:FC7:2:1::1/128 [110/2]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:2:1::2/128 [110/1], tag 2000
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
LC  2620:FC7:2:1::3/128 [0/0]
     via Loopback0, receive
C   2620:FC7:20:2::/64 [0/0]
     via GigabitEthernet2, directly connected
L   2620:FC7:20:2::2/128 [0/0]
     via GigabitEthernet2, receive
OI  2620:FC7:20:4::/64 [110/2]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:20:5::/64 [110/1]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
OE2 2620:FC7:20:6::/64 [110/1]
     via FE80::5054:FF:FEA3:8B13, GigabitEthernet2
L   FF00::/8 [0/0]
     via Null0, receive
Y-CE-3#
```

## show ip ospf neighbor

```
show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.0.101.3         1   FULL/BDR        00:00:36    10.20.2.1       GigabitEthernet2
Y-CE-3#
```

