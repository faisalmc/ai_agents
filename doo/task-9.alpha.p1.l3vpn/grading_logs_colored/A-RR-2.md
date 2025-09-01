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
 <span style="background-color:red">*>i  10.1.1.2/32      1.0.101.2                0    100      0 4000 i</span>
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
 <span style="background-color:red">*>i  2620:FC7:1011::2/128
                      ::FFFF:1.0.101.2
                                                0    100      0 4000 i</span>
 * i                   ::FFFF:1.0.101.2
                                                0    100      0 4000 i
 * i  2620:FC7:1011::4/128
                      ::FFFF:1.0.101.3
                                                1    100      0 ?
 *>i                   ::FFFF:1.0.101.3
                                                1    100      0 ?
A-RR-2#
```



