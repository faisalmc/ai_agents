# Full Output for Task task-22.alpha.bgp_prefix
**Device:** B-CE-1 (192.168.100.113)
_Generated: 2025-08-07 04:52:47.435487_

## show bgp ipv4 unicast

```
show bgp ipv4 unicast
BGP table version is 12, local router ID is 10.1.1.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   8.8.8.8/32       0.0.0.0                  0         32768 i
 *>   10.1.1.2/32      0.0.0.0                  0         32768 i
 *>   10.1.1.4/32      10.10.2.1                              0 100 ?
 r>   10.10.2.0/24     10.10.2.1                0             0 100 ?
 *>   10.10.4.0/24     10.10.2.1                              0 100 ?
B-CE-1#
```

## show bgp ipv6 unicast

```
show bgp ipv6 unicast
BGP table version is 11, local router ID is 10.1.1.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 r>   2620:FC7:10:102::/64
                      2620:FC7:10:102::1
                                                0             0 100 ?
 *>   2620:FC7:10:104::/64
                      2620:FC7:10:102::1
                                                              0 100 ?
 *>   2620:FC7:1011::2/128
                      ::                       0         32768 i
 *>   2620:FC7:1011::4/128
                      2620:FC7:10:102::1
                                                              0 100 ?
B-CE-1#
```

