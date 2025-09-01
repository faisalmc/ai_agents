# Grading Output for Task task-14.bravo.multicast_vpn/
**Device:** B-P-2 (192.168.100.123)
_Generated: 2025-07-14 08:59:43.648044_

## show ip pim neighbor

```
show ip pim neighbor

Mon Jul 14 12:59:41.134 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.8.1                      GigabitEthernet0/0/0/0 2d01h     00:01:34 1           B
2.2.8.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:26 1           (DR) B E
2.2.4.1                      GigabitEthernet0/0/0/2 2d01h     00:01:41 1           B
2.2.4.2*                     GigabitEthernet0/0/0/2 2d01h     00:01:43 1           (DR) B E
RP/0/RP0/CPU0:B-P-2#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Mon Jul 14 12:59:41.256 UTC
No neighbors found for VRF YELLOW.
RP/0/RP0/CPU0:B-P-2#
```

## show pim neighbor

```
show pim neighbor

Mon Jul 14 12:59:41.378 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.8.1                      GigabitEthernet0/0/0/0 2d01h     00:01:34 1           B
2.2.8.2*                     GigabitEthernet0/0/0/0 2d01h     00:01:25 1           (DR) B E
2.2.4.1                      GigabitEthernet0/0/0/2 2d01h     00:01:40 1           B
2.2.4.2*                     GigabitEthernet0/0/0/2 2d01h     00:01:42 1           (DR) B E
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn summary

```
show bgp ipv4 mvpn summary

Mon Jul 14 12:59:41.509 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn advertised summary

```
show bgp ipv4 mvpn advertised summary

Mon Jul 14 12:59:41.694 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

```
show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

Mon Jul 14 12:59:41.833 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-2#
```

## show pim vrf YELLOW mdt cache

```
show pim vrf YELLOW mdt cache

Mon Jul 14 12:59:41.983 UTC
No MDT Cache entries found.
RP/0/RP0/CPU0:B-P-2#
```

## show mrib vrf YELLOW route

```
show mrib vrf YELLOW route

Mon Jul 14 12:59:42.112 UTC
RP/0/RP0/CPU0:B-P-2#
```

