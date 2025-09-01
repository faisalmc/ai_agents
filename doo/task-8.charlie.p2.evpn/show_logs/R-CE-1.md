# Full Output for Task task-8.charlie.p2.evpn/
**Device:** R-CE-1 (192.168.100.139)
_Generated: 2025-08-06 03:09:17.116135_

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

      10.0.0.0/8 is variably subnetted, 6 subnets, 2 masks
C        10.1.123.0/24 is directly connected, GigabitEthernet2.20
L        10.1.123.1/32 is directly connected, GigabitEthernet2.20
C        10.3.1.1/32 is directly connected, Loopback0
O E2     10.3.1.2/32 [110/20] via 10.1.123.2, 00:02:51, GigabitEthernet2.20
C        10.13.1.0/24 is directly connected, GigabitEthernet2
L        10.13.1.2/32 is directly connected, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.139/32 is directly connected, GigabitEthernet1
R-CE-1#
```

## show ip ospf neighbor

```
show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
3.0.101.10        1   FULL/BDR        00:00:35    10.1.123.2      GigabitEthernet2.20
R-CE-1#
```

## ping 10.3.1.2

```
ping 10.3.1.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.1.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 6/6/8 ms
R-CE-1#
```

