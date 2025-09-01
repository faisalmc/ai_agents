# Grading Output for Task task-9.alpha.p1.l3vpn/
**Device:** B-CE-2 (192.168.100.114)
_Generated: 2025-08-06 03:33:52.086343_


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
<span style="background-color:red">O E2     10.1.1.2/32 [110/1] via 10.10.4.1</span>, 00:12:39, GigabitEthernet2
C        10.1.1.4/32 is directly connected, Loopback0
O E2     10.10.2.0/24 [110/1] via 10.10.4.1, 22:54:01, GigabitEthernet2
C        10.10.4.0/24 is directly connected, GigabitEthernet2
L        10.10.4.2/32 is directly connected, GigabitEthernet2
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.114/32 is directly connected, GigabitEthernet1
B-CE-2#
```

## show ip ospf neighbor

```
show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
<span style="background-color:red">1.0.101.3</span>         1   FULL/BDR        00:00:31    10.10.4.1       GigabitEthernet2
B-CE-2#
```

