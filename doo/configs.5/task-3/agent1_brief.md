# Agent-1 Summary for task-3

*Executive Summary:*
This task will configure BGP AS 100 with IPv4 labeled-unicast on 6 devices (ASBRs, Providers, Provider-Edges, Route Reflectors). 
The configuration aims to enhance core reachability, establish BGP sessions, and optimize routing for efficient network operation.

*Engineering Summary:*
• A-ASBR-1, A-ASBR-2:
   - Configure BGP AS 100 with IPv4 labeled-unicast
   - Use Loopback0 as update-source for core neighbors
   - Advertise specific prefixes with labels
• A-P-1, A-P-2, A-P-3, A-P-4:
   - Configure BGP AS 100 with IPv4 unicast
   - Implement route-policy for SID labeling
   - Use Loopback0 as update-source for BGP neighbors
• A-PE-1, A-PE-2, A-PE-3, A-PE-4:
   - Define BGP AS 100 with IPv4 unicast
   - Apply route-policy for network advertisement
   - Allocate labels for prefixes
   - Use Loopback0 as update-source for core neighbors
• A-RR-1, A-RR-2:
   - Configure BGP AS 100 as Route Reflector
   - Use Loopback0 as update source for neighbors
   - Activate specific BGP neighbors
• Operational-Checks:
   - Various show commands for BGP and MPLS validation