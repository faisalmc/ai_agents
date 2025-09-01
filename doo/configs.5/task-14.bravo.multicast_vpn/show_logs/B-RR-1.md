# Full Output for Task task-14.bravo.multicast_vpn/
**Device:** B-RR-1 (192.168.100.126)
_Generated: 2025-07-14 08:59:45.625402_

## show run | sec router bgp

```
show run | sec router bgp
router bgp 200
 bgp router-id 2.0.101.10
 bgp log-neighbor-changes
 neighbor IBGPV4 peer-group
 neighbor IBGPV4 remote-as 200
 neighbor IBGPV4 update-source Loopback0
 neighbor 2.0.101.1 peer-group IBGPV4
 neighbor 2.0.101.2 peer-group IBGPV4
 neighbor 2.0.101.3 peer-group IBGPV4
 neighbor 2.0.101.4 peer-group IBGPV4
 neighbor 2.0.101.5 peer-group IBGPV4
 neighbor 2.0.101.6 peer-group IBGPV4
 neighbor 2.0.101.7 peer-group IBGPV4
 neighbor 2.0.101.8 peer-group IBGPV4
 neighbor 2.0.101.9 peer-group IBGPV4
 !
 address-family ipv4
  neighbor IBGPV4 send-community extended
  neighbor IBGPV4 route-reflector-client
  no neighbor 2.0.101.1 activate
  no neighbor 2.0.101.2 activate
  no neighbor 2.0.101.3 activate
  no neighbor 2.0.101.4 activate
  no neighbor 2.0.101.5 activate
  no neighbor 2.0.101.6 activate
  no neighbor 2.0.101.7 activate
  no neighbor 2.0.101.8 activate
  no neighbor 2.0.101.9 activate
 exit-address-family
 !
 address-family ipv4 mvpn
  neighbor IBGPV4 send-community extended
  neighbor IBGPV4 route-reflector-client
  neighbor 2.0.101.1 activate
  neighbor 2.0.101.2 activate
  neighbor 2.0.101.3 activate
 exit-address-family
 !
 address-family vpnv4
  neighbor IBGPV4 send-community extended
  neighbor IBGPV4 route-reflector-client
  neighbor 2.0.101.1 activate
  neighbor 2.0.101.2 activate
  neighbor 2.0.101.3 activate
  neighbor 2.0.101.4 activate
  neighbor 2.0.101.5 activate
  neighbor 2.0.101.6 activate
  neighbor 2.0.101.7 activate
  neighbor 2.0.101.8 activate
  neighbor 2.0.101.9 activate
 exit-address-family
 !
 address-family vpnv6
  neighbor IBGPV4 send-community extended
  neighbor IBGPV4 route-reflector-client
  neighbor 2.0.101.1 activate
  neighbor 2.0.101.2 activate
  neighbor 2.0.101.3 activate
  neighbor 2.0.101.4 activate
  neighbor 2.0.101.5 activate
  neighbor 2.0.101.6 activate
  neighbor 2.0.101.7 activate
  neighbor 2.0.101.8 activate
  neighbor 2.0.101.9 activate
 exit-address-family
B-RR-1#
```

