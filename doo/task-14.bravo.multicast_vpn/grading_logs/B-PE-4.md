# Grading Output for Task task-11.bravo.multicast_vpn
**Device:** B-PE-4 (192.168.100.120)
_Generated: 2025-06-29 03:18:38.717027_

## show ip pim neighbor

```
show ip pim neighbor

Sun Jun 29 07:18:24.148 UTC

PIM neighbors in VRF default
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

2.2.6.1*                     GigabitEthernet0/0/0/0 00:34:12  00:01:29 1           B E
2.2.6.2                      GigabitEthernet0/0/0/0 00:34:04  00:01:20 1           (DR) B
2.2.2.1                      GigabitEthernet0/0/0/2 00:34:12  00:01:25 1           B
2.2.2.2*                     GigabitEthernet0/0/0/2 00:34:12  00:01:42 1           (DR) B E
RP/0/RP0/CPU0:B-PE-4#
```

## show ip pim vrf YELLOW neighbor

```
show ip pim vrf YELLOW neighbor

Sun Jun 29 07:18:24.274 UTC

PIM neighbors in VRF YELLOW
Flag: B - Bidir capable, P - Proxy capable, DR - Designated Router,
      E - ECMP Redirect capable, S - Sticky DR Neighbor
      * indicates the neighbor created for this router

Neighbor Address             Interface              Uptime    Expires  DR pri      Flags

10.20.3.1*                   GigabitEthernet0/0/0/1 00:34:12  00:01:37 1           B E
10.20.3.2                    GigabitEthernet0/0/0/1 00:34:09  00:01:31 1           (DR) P
RP/0/RP0/CPU0:B-PE-4#
```

