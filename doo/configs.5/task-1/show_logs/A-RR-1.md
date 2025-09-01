# Full Output for Task task-1
**Device:** A-RR-1 (192.168.100.111)
_Generated: 2025-08-27 15:54:03.979005_

## show run | section router isis

```
show run | section router isis
 ip router isis 
 ipv6 router isis 
 ip router isis 
 ipv6 router isis 
router isis
 net 49.0001.0001.0000.0101.0011.00
 is-type level-2-only
 metric-style wide
 metric 100 level-2
 passive-interface Loopback0
 !
 address-family ipv6
  metric 200 level-2
 exit-address-family
A-RR-1#
```

## show isis neighbors

```
show isis neighbors

Tag null:
System Id       Type Interface     IP Address      State Holdtime Circuit Id
A-P-1           L2   Gi2           1.0.70.2        UP    22       00
A-RR-2          L2   Gi3           1.0.73.2        UP    24       03
A-RR-1#
```

## show ip route isis

```
show ip route isis
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

      1.0.0.0/8 is variably subnetted, 21 subnets, 2 masks
i L2     1.0.30.0/24 [115/200] via 1.0.70.2, 08:34:35, GigabitEthernet2
i L2     1.0.31.0/24 [115/300] via 1.0.70.2, 04:38:48, GigabitEthernet2
i L2     1.0.32.0/24 [115/300] via 1.0.73.2, 6d09h, GigabitEthernet3
                     [115/300] via 1.0.70.2, 6d09h, GigabitEthernet2
i L2     1.0.33.0/24 [115/200] via 1.0.70.2, 08:34:35, GigabitEthernet2
i L2     1.0.34.0/24 [115/300] via 1.0.73.2, 04:38:48, GigabitEthernet3
                     [115/300] via 1.0.70.2, 04:38:48, GigabitEthernet2
i L2     1.0.35.0/24 [115/200] via 1.0.70.2, 08:34:35, GigabitEthernet2
i L2     1.0.71.0/24 [115/200] via 1.0.73.2, 6d09h, GigabitEthernet3
i L2     1.0.101.6/32 [115/300] via 1.0.70.2, 6d09h, GigabitEthernet2
i L2     1.0.101.7/32 [115/300] via 1.0.73.2, 6d09h, GigabitEthernet3
                      [115/300] via 1.0.70.2, 6d09h, GigabitEthernet2
i L2     1.0.101.8/32 [115/300] via 1.0.70.2, 04:38:48, GigabitEthernet2
i L2     1.0.101.12/32 [115/100] via 1.0.73.2, 6d09h, GigabitEthernet3
A-RR-1#
```

## show ipv6 route isis

```
show ipv6 route isis
IPv6 Routing Table - default - 17 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, a - Application, m - OMP
I2  2620:FC7:1:30::/64 [115/300]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1:31::/64 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1:32::/64 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
     via FE80::5054:FF:FEE3:B580, GigabitEthernet3
I2  2620:FC7:1:33::/64 [115/300]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1:34::/64 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
     via FE80::5054:FF:FEE3:B580, GigabitEthernet3
I2  2620:FC7:1:35::/64 [115/300]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1:71::/64 [115/200]
     via FE80::5054:FF:FEE3:B580, GigabitEthernet3
I2  2620:FC7:1001::6/128 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1001::7/128 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
     via FE80::5054:FF:FEE3:B580, GigabitEthernet3
I2  2620:FC7:1001::8/128 [115/400]
     via FE80::5054:FF:FE62:BBC0, GigabitEthernet2
I2  2620:FC7:1001::12/128 [115/100]
     via FE80::5054:FF:FEE3:B580, GigabitEthernet3
A-RR-1#
```

