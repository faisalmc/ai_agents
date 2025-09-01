# Full Output for Task task-13.bravo.bgp_soo.p2.soo
**Device:** Y-CE-2 (192.168.100.128)
_Generated: 2025-08-07 01:34:17.121158_

## show bgp ipv4 unicast 10.2.1.200/32 subnets

```
show bgp ipv4 unicast 10.2.1.200/32 subnets
BGP table version is 9, local router ID is 10.2.1.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.2.1.200/32    0.0.0.0                  0         32768 i
Y-CE-2#
```

## show bgp ipv6 unicast 2620:FC7:2:1::200/128 longer-prefixes

```
show bgp ipv6 unicast 2620:FC7:2:1::200/128 longer-prefixes
BGP table version is 9, local router ID is 10.2.1.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   2620:FC7:2:1::200/128
                      ::                       0         32768 i
Y-CE-2#
```

