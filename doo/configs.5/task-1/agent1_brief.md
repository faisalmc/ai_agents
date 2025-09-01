# Agent-1 Summary for task-1

*Executive Summary:*
This task will configure ISIS on multiple devices within the Alpha provider network. 
The configuration aims to enhance routing efficiency, ensure proper network convergence, 
and support scalable and reliable communication across the network.

*Engineering Summary:*
• A-ASBR-1:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback and GigabitEthernet interfaces with IPv4 and IPv6 metrics
• A-ASBR-2:
   - Configure ISIS with overload bit and level-2-only
   - Set metric-style wide for IPv4 and IPv6 unicast
   - Define Loopback interfaces with specific metrics
   - Apply ISIS group ISIS-GRP to router AGG2
• A-P-1:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback interfaces with IPv4 and IPv6 address families
   - Configure GigabitEthernet interfaces with IPv4 and IPv6 address families
• A-P-2:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback and GigabitEthernet interfaces with IPv4 and IPv6 metrics
   - Apply ISIS group ISIS-GRP to routers AGG1 and CORE
• A-P-3:
   - Configure ISIS with overload bit and level 2 only
   - Define wide metric style for IPv4 and IPv6 unicast
   - Assign metrics to Loopback and GigabitEthernet interfaces
• A-P-4:
   - Configure ISIS with overload bit and level-2-only
   - Define metric-style wide for IPv4 and IPv6 unicast
   - Configure Loopback interfaces with specific metrics
   - Apply ISIS group ISIS-GRP to routers AGG2 and CORE
• A-PE-1:
   - Configure ISIS with overload bit and metric-style wide
   - Define address families for IPv4 and IPv6 unicast with wide metric style
   - Configure Loopback interfaces with passive mode and specific metrics
   - Configure GigabitEthernet interfaces as point-to-point with specific metrics
   - Apply ISIS group 'ISIS-GRP' to router AGG1
• A-PE-2:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback and GigabitEthernet interfaces with IPv4 and IPv6 metrics
• A-PE-3:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback interfaces with specific metrics for IPv4 and IPv6 unicast
   - Apply ISIS group configuration to router AGG1
• A-PE-4:
   - Configure ISIS with overload bit and metric-style wide
   - Define Loopback and GigabitEthernet interfaces with IPv4 and IPv6 metrics
   - Apply ISIS group ISIS-GRP to router AGG2
• A-RR-1:
   - Configure ISIS for IPv4 and IPv6 with point-to-point network type
   - Set IS-IS NET and use level-2-only configuration with wide metric-style
• A-RR-2:
   - Configure ISIS for IPv4 and IPv6 with point-to-point network type
   - Set IS-IS NET and use level-2-only configuration with wide metric-style