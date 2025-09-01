# Grading Output for Task task-9.alpha.p1.l3vpn/
**Device:** A-RR-2 (192.168.100.112)
_Generated: 2025-08-06 03:40:39.407361_

## show bgp vpnv4 unicast all

```
show bgp vpnv4 unicast all
BGP table version is 19, local router ID is 1.0.101.12
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2
 *>i  10.1.1.2/32      1.0.101.2                0    100      0 4000 i
 * i                   1.0.101.2                0    100      0 4000 i
 *>i  10.1.1.4/32      1.0.101.3                2    100      0 ?
 * i                   1.0.101.3                2    100      0 ?
 * i  10.10.2.0/24     1.0.101.2                0    100      0 ?
 *>i                   1.0.101.2                0    100      0 ?
 *>i  10.10.4.0/24     1.0.101.3                0    100      0 ?
 * i                   1.0.101.3                0    100      0 ?
A-RR-2#
```

## show bgp vpnv6 unicast all

```
show bgp vpnv6 unicast all
BGP table version is 20, local router ID is 1.0.101.12
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 100:2
 * i  2620:FC7:10:102::/64
                      ::FFFF:1.0.101.2
                                                0    100      0 ?
 *>i                   ::FFFF:1.0.101.2
                                                0    100      0 ?
 *>i  2620:FC7:10:104::/64
                      ::FFFF:1.0.101.3
                                                0    100      0 ?
 * i                   ::FFFF:1.0.101.3
                                                0    100      0 ?
 *>i  2620:FC7:1011::2/128
                      ::FFFF:1.0.101.2
                                                0    100      0 4000 i
 * i                   ::FFFF:1.0.101.2
                                                0    100      0 4000 i
 * i  2620:FC7:1011::4/128
                      ::FFFF:1.0.101.3
                                                1    100      0 ?
 *>i                   ::FFFF:1.0.101.3
                                                1    100      0 ?
A-RR-2#
```

## show ip bgp summary

```
show ip bgp summary
BGP router identifier 1.0.101.12, local AS number 100
BGP table version is 43, main routing table version 43
10 network entries using 2480 bytes of memory
11 path entries using 1496 bytes of memory
10/10 BGP path/bestpath attribute entries using 2880 bytes of memory
9 BGP rrinfo entries using 360 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
3 BGP extended community entries using 104 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 7344 total bytes of memory
BGP activity 19/1 prefixes, 63/36 paths, scan interval 60 secs
10 networks peaked at 06:43:11 Aug 5 2025 UTC (1d00h ago)

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
1.0.101.5       4          100    1412    1577       43    0    0 23:01:52        2
1.0.101.6       4          100    1415    1575       43    0    0 23:01:51        3
1.0.101.7       4          100    1393    1575       43    0    0 23:01:51        3
1.0.101.8       4          100    1390    1573       43    0    0 23:01:58        3

A-RR-2#
```

