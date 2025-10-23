# Agent-1 Summary for task-3

*Executive Summary:*
This initiative will configure BGP across 12 devices, including ASBRs, Providers, and Route Reflectors. 
The purpose is to enhance core network reachability and improve routing efficiency. 
By implementing these changes, the organization will benefit from increased network reliability, better traffic management, and improved scalability for future growth.

*Engineering Summary:*

**A-ASBR-1:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Run BGP AS 100 with Loopback0 as update-source
- Advertise 1.0.101.9/32 with label via route-policy

**A-ASBR-2:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Advertise 1.0.101.10/32 with label via route-policy
- Use Loopback0 as update-source for core neighbors

**A-P-1:**
- Enable BGP with AS 100 for IPv4 unicast routing
- Set up route policies for label allocation
- Configure route reflector clients for BGP neighbors

**A-P-2:**
- Enable BGP with AS 100 for IPv4 unicast routing
- Set up route policies for label allocation
- Configure route reflector clients for BGP

**A-P-3:**
- Enable BGP with AS 100 and enforce modifications for iBGP
- Advertise 1.0.101.7/32 with label via route-policy
- Configure neighbor groups for route reflection with next-hop-self

**A-P-4:**
- Enable BGP with AS 100 for IPv4 unicast routing
- Set up route policies for label allocation
- Configure route reflector groups for iBGP clients

**A-PE-1:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Advertise Loopback0 /32 via BGP with label using route-policy
- Configure neighbor-group for BGP peers with Loopback0 as update-source

**A-PE-2:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Advertise 1.0.101.2/32 with label via route-policy
- Use Loopback0 as update-source for core neighbors

**A-PE-3:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Advertise Loopback0 /32 via BGP with label using route-policy
- Use Loopback0 as update-source for core neighbors

**A-PE-4:**
- Enable BGP with IPv4 labeled-unicast for core reachability
- Advertise Loopback0 /32 via BGP with label using route-policy
- Use Loopback0 as update-source for core neighbors

**A-RR-1:**
- Configure BGP with AS 100 and set router ID
- Establish a peer group for route reflector clients
- Activate IPv4 unicast address family for clients

**A-RR-2:**
- Configure BGP with AS 100 and set router ID
- Establish a peer group for route reflector clients
- Activate IPv4 unicast address family for clients

**Operational Checks:**
- Show BGP configuration
- Show brief BGP neighbors
- Show BGP IPv4 labeled-unicast
- Show MPLS forwarding table
- Show BGP IPv4 labeled-unicast for specific neighbors (1.0.101.7, 1.0.101.9)