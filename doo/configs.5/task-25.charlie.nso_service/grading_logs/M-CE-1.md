M-CE-1#show ip route
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
C        10.3.1.3/32 is directly connected, Loopback0
<span style="background-color: #fdd">B        10.3.1.4/32 [20/0] via 10.13.3.1</span>, 02:21:10  
C        10.13.3.0/24 is directly connected, GigabitEthernet2
L        10.13.3.2/32 is directly connected, GigabitEthernet2
<span style="background-color: #fdd">B        10.13.4.0/24 [20/0] via 10.13.3.1</span>, 02:22:51  
      192.168.100.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.100.0/24 is directly connected, GigabitEthernet1
L        192.168.100.141/32 is directly connected, GigabitEthernet1
M-CE-1#
M-CE-1#
M-CE-1#ping 10.3.1.4
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.1.4, timeout is 2 seconds:
!!!!!
<span style="background-color: #fdd">Success rate is 100 percent (5/5)</span>, round-trip min/avg/max = 3/3/4 ms
M-CE-1#traceroute 10.3.1.4
Type escape sequence to abort.
Tracing the route to 10.3.1.4
VRF info: (vrf in name/id, vrf out name/id)
  1 10.13.3.1 [AS 300] 8 msec 7 msec 2 msec
  2 3.3.12.2 [MPLS: Label 24006 Exp 0] 6 msec 6 msec 6 msec
  3 10.13.4.2 [AS 300] 5 msec 4 msec * 
M-CE-1#


