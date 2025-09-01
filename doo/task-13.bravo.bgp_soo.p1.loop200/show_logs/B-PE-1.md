# Full Output for Task task-13.bravo.bgp_soo.p1.loop200
**Device:** B-PE-1 (192.168.100.117)
_Generated: 2025-08-07 01:05:24.280292_

## show bgp vrf YELLOW ipv4 unicast advertised | begin .200/32

```
show bgp vrf YELLOW ipv4 unicast advertised | begin .200/32

Thu Aug  7 05:05:20.636 UTC
10.2.1.200/32 is advertised to 10.20.5.2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.2
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 26
  Attributes after inbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS LOCAL EXTCOMM 
    origin: IGP  neighbor as: 2000  metric: 0  local pref: 100  
    aspath: 2000
    extended community: RT:200:2 
    originator: 2.0.101.2    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 10.20.5.1
    ORG AS LOCAL 
    origin: IGP  neighbor as: 2000  local pref: 100  
    aspath: 200 2000

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 26
10.20.2.0/24 is advertised to 10.20.5.2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.3
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 13
  Attributes after inbound policy was applied:
    next hop: 2.0.101.3
    MET ORG AS LOCAL EXTCOMM 
    origin: incomplete  metric: 0  local pref: 100  
    aspath: 
    extended community: OSPF route-type:0:2:0x0 OSPF router-id:2.0.101.3 RT:200:2 
    originator: 2.0.101.3    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 10.20.5.1
    ORG AS LOCAL 
    origin: incomplete  local pref: 100  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 26
10.20.4.0/24 is advertised to 10.20.5.2
  Path info:
    neighbor: Local           neighbor router id: 2.0.101.1
    valid  redistributed  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 4
  Attributes after inbound policy was applied:
    next hop: 0.0.0.0
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: OSPF route-type:0:2:0x0 OSPF router-id:2.0.101.1 RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 10.20.5.1
    MET ORG AS 
    origin: incomplete  metric: 0  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 26
10.20.5.0/24 is advertised to 10.20.5.2
  Path info:
    neighbor: Local           neighbor router id: 2.0.101.1
    valid  redistributed  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 2
  Attributes after inbound policy was applied:
    next hop: 0.0.0.0
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 10.20.5.1
    MET ORG AS 
    origin: incomplete  metric: 0  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 26
10.20.6.0/24 is advertised to 10.20.5.2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.2
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 10
  Attributes after inbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS LOCAL EXTCOMM 
    origin: incomplete  metric: 0  local pref: 100  
    aspath: 
    extended community: RT:200:2 
    originator: 2.0.101.2    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 10.20.5.1
    ORG AS LOCAL 
    origin: incomplete  local pref: 100  
    aspath: 200

RP/0/RP0/CPU0:B-PE-1#
```

## show bgp vrf YELLOW ipv6 unicast advertised | begin .200/128

```
show bgp vrf YELLOW ipv6 unicast advertised | begin .200/128

Thu Aug  7 05:05:20.879 UTC
2620:fc7:2:1::200/128 is advertised to 2620:fc7:20:5::2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.2
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 21
  Attributes after inbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS LOCAL EXTCOMM 
    origin: IGP  neighbor as: 2000  metric: 0  local pref: 100  
    aspath: 2000
    extended community: RT:200:2 
    originator: 2.0.101.2    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 2620:fc7:20:5::1
    ORG AS LOCAL 
    origin: IGP  neighbor as: 2000  local pref: 100  
    aspath: 200 2000

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 21
2620:fc7:20:2::/64 is advertised to 2620:fc7:20:5::2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.3
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 10
  Attributes after inbound policy was applied:
    next hop: 2.0.101.3
    MET ORG AS LOCAL EXTCOMM 
    origin: incomplete  metric: 0  local pref: 100  
    aspath: 
    extended community: OSPF route-type:0:2:0x0 OSPF router-id:0.0.0.0 RT:200:2 
    originator: 2.0.101.3    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 2620:fc7:20:5::1
    ORG AS LOCAL 
    origin: incomplete  local pref: 100  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 21
2620:fc7:20:4::/64 is advertised to 2620:fc7:20:5::2
  Path info:
    neighbor: Local           neighbor router id: 2.0.101.1
    valid  redistributed  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 4
  Attributes after inbound policy was applied:
    next hop: ::
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: OSPF route-type:0:2:0x0 OSPF router-id:0.0.0.0 RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 2620:fc7:20:5::1
    MET ORG AS 
    origin: incomplete  metric: 0  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 21
2620:fc7:20:5::/64 is advertised to 2620:fc7:20:5::2
  Path info:
    neighbor: Local           neighbor router id: 2.0.101.1
    valid  redistributed  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 2
  Attributes after inbound policy was applied:
    next hop: ::
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 2620:fc7:20:5::1
    MET ORG AS 
    origin: incomplete  metric: 0  
    aspath: 200

Route Distinguisher: 200:2 (default for vrf YELLOW)
Route Distinguisher Version: 21
2620:fc7:20:6::/64 is advertised to 2620:fc7:20:5::2
  Path info:
    neighbor: 2.0.101.10      neighbor router id: 2.0.101.2
    valid  internal  best  import-candidate  imported  
Received Path ID 0, Local Path ID 1, version 8
  Attributes after inbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS LOCAL EXTCOMM 
    origin: incomplete  metric: 0  local pref: 100  
    aspath: 
    extended community: RT:200:2 
    originator: 2.0.101.2    cluster list: 2.0.101.10  
  Attributes after outbound policy was applied:
    next hop: 2620:fc7:20:5::1
    ORG AS LOCAL 
    origin: incomplete  local pref: 100  
    aspath: 200

RP/0/RP0/CPU0:B-PE-1#
```

