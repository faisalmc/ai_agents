# Grading Output for Task task-13.bravo.bgp_soo.p1.loop200
**Device:** B-PE-2 (192.168.100.118)
_Generated: 2025-08-07 01:05:26.340051_

## show bgp vpnv4 unicast vrf YELLOW advertised | begin .200/32

```
show bgp vpnv4 unicast vrf YELLOW advertised | begin .200/32

Thu Aug  7 05:05:21.865 UTC
10.2.1.200/32 is advertised to 2.0.101.10
  Path info:
    neighbor: 10.20.6.2       neighbor router id: 10.2.1.2
    valid  external  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 23
  Attributes after inbound policy was applied:
    next hop: 10.20.6.2
    MET ORG AS EXTCOMM 
    origin: IGP  neighbor as: 2000  metric: 0  
    aspath: 2000
    extended community: RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS EXTCOMM 
    origin: IGP  neighbor as: 2000  metric: 0  
    aspath: 2000
    extended community: RT:200:2 

Route Distinguisher: 200:2
Route Distinguisher Version: 25
10.20.6.0/24 is advertised to 2.0.101.10
  Path info:
    neighbor: Local           neighbor router id: 2.0.101.2
    valid  redistributed  best  import-candidate  
Received Path ID 0, Local Path ID 1, version 6
  Attributes after inbound policy was applied:
    next hop: 0.0.0.0
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: RT:200:2 
  Attributes after outbound policy was applied:
    next hop: 2.0.101.2
    MET ORG AS EXTCOMM 
    origin: incomplete  metric: 0  
    aspath: 
    extended community: RT:200:2 

RP/0/RP0/CPU0:B-PE-2#
```

