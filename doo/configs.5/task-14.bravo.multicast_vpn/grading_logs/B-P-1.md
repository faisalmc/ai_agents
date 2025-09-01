# Grading Output for Task task-14.bravo.multicast_vpn/
**Device:** B-P-1 (192.168.100.122)
_Generated: 2025-07-14 08:59:39.293687_


## show ip pim neighbor

```
show ip pim neighbor

Mon Jul 14 12:59:36.307 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.5.1                      GigabitEthernet0/0/0/4 2d01h     00:01:41 1           B
2.2.5.2*                     GigabitEthernet0/0/0/4 2d02h     00:01:25 1           (DR) B E
2.2.3.1                      GigabitEthernet0/0/0/2 2d01h     00:01:15 1           B
2.2.3.2*                     GigabitEthernet0/0/0/2 2d02h     00:01:19 1           (DR) B E
2.2.8.1*                     GigabitEthernet0/0/0/1 2d02h     00:01:38 1           B
2.2.8.2                      GigabitEthernet0/0/0/1 2d01h     00:01:30 1           (DR) B
RP/0/RP0/CPU0:B-P-1#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Mon Jul 14 12:59:36.507 UTC
No neighbors found for VRF YELLOW.
RP/0/RP0/CPU0:B-P-1#
```

## show pim neighbor

```
show pim neighbor

Mon Jul 14 12:59:36.635 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.5.1                      GigabitEthernet0/0/0/4 2d01h     00:01:41 1           B
2.2.5.2*                     GigabitEthernet0/0/0/4 2d02h     00:01:25 1           (DR) B E
2.2.3.1                      GigabitEthernet0/0/0/2 2d01h     00:01:15 1           B
2.2.3.2*                     GigabitEthernet0/0/0/2 2d02h     00:01:19 1           (DR) B E
2.2.8.1*                     GigabitEthernet0/0/0/1 2d02h     00:01:38 1           B
2.2.8.2                      GigabitEthernet0/0/0/1 2d01h     00:01:30 1           (DR) B
RP/0/RP0/CPU0:B-P-1#
```

## show bgp ipv4 mvpn summary

```
show bgp ipv4 mvpn summary

Mon Jul 14 12:59:36.763 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-1#
```

## show bgp ipv4 mvpn advertised summary

```
show bgp ipv4 mvpn advertised summary

Mon Jul 14 12:59:36.916 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-1#
```

## show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

```
show bgp ipv4 mvpn vrf YELLOW [1][2.0.101.1]/40

Mon Jul 14 12:59:37.079 UTC
% None of the requested address families are configured for instance 'default'(36210)
RP/0/RP0/CPU0:B-P-1#
```

## show pim vrf YELLOW mdt cache

```
show pim vrf YELLOW mdt cache

Mon Jul 14 12:59:37.244 UTC
No MDT Cache entries found.
RP/0/RP0/CPU0:B-P-1#
```

## show mrib vrf YELLOW route

```
show mrib vrf YELLOW route

Mon Jul 14 12:59:37.400 UTC
RP/0/RP0/CPU0:B-P-1#
```

## show pim neighbor

```
show pim neighbor

Mon Jul 14 12:59:37.528 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.5.1                      GigabitEthernet0/0/0/4 2d01h     00:01:40 1           B
2.2.5.2*                     GigabitEthernet0/0/0/4 2d02h     00:01:24 1           (DR) B E
2.2.3.1                      GigabitEthernet0/0/0/2 2d01h     00:01:44 1           B
2.2.3.2*                     GigabitEthernet0/0/0/2 2d02h     00:01:18 1           (DR) B E
2.2.8.1*                     GigabitEthernet0/0/0/1 2d02h     00:01:37 1           B
2.2.8.2                      GigabitEthernet0/0/0/1 2d01h     00:01:29 1           (DR) B
RP/0/RP0/CPU0:B-P-1#
```

