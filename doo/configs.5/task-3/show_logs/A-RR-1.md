# Full Output for Task task-3
**Device:** A-RR-1 (192.168.100.111)
_Generated: 2025-08-05 02:48:35.625801_

## show run | sec bgp

```
show run | sec bgp
router bgp 100
 bgp router-id 1.0.101.11
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor RR_CLIENT peer-group
 neighbor RR_CLIENT remote-as 100
 neighbor RR_CLIENT update-source Loopback0
 neighbor 1.0.101.5 peer-group RR_CLIENT
 neighbor 1.0.101.6 peer-group RR_CLIENT
 neighbor 1.0.101.7 peer-group RR_CLIENT
 neighbor 1.0.101.8 peer-group RR_CLIENT
 !
 address-family ipv4
  neighbor RR_CLIENT route-reflector-client
  neighbor RR_CLIENT send-label
  neighbor 1.0.101.5 activate
  neighbor 1.0.101.6 activate
  neighbor 1.0.101.7 activate
  neighbor 1.0.101.8 activate
 exit-address-family
A-RR-1#
```

