# Grading Output for Task task-9.alpha.p1.l3vpn/
**Device:** B-CE-1 (192.168.100.113)
_Generated: 2025-08-06 03:40:32.394656_

## ping 10.1.1.4 source loopback 0

```
ping 10.1.1.4 source loopback 0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.1.1.4, timeout is 2 seconds:
Packet sent with a source address of 10.1.1.2 
!!!!!
<span style="background-color:red">Success rate is 100 percent</span> (5/5), round-trip min/avg/max = 5/6/8 ms
B-CE-1#
```

## ping ipv6 2620:FC7:1011::4 source lo0

```
ping ipv6 2620:FC7:1011::4 source lo0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 2620:FC7:1011::4, timeout is 2 seconds:
Packet sent with a source address of 2620:FC7:1011::2
!!!!!
<span style="background-color:red">Success rate is 100 percent</span> (5/5), round-trip min/avg/max = 4/4/5 ms
B-CE-1#
```

