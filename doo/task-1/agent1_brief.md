# Agent-1 Summary for task-1

*Executive Summary:*
This task will configure ISIS on multiple devices within the network. 
The configuration aims to optimize routing efficiency, ensure network stability, 
and support seamless communication between devices.

*Engineering Summary:*
• A-ASBR-1 (Alpha ASBR):
   - Disable ISIS process AGG2
   - Configure ISIS with overload bit and level-2-only
   - Configure ISIS address families for IPv4 and IPv6 with wide metric style
   - Configure Loopback and GigabitEthernet interfaces for ISIS
   - Apply ISIS group ISIS-GRP to router process AGG2
   - Configure Loopback0, GigabitEthernet0/0/0/1, GigabitEthernet0/0/0/2 interfaces
• A-ASBR-2 (Beta ASBR):
   - Configure ISIS with overload bit and level-2-only
   - Configure wide metric style for IPv4 and IPv6
   - Configure Loopback and GigabitEthernet interfaces for ISIS
   - Apply ISIS group ISIS-GRP to router AGG2
• A-P-1, A-P-2, A-P-3, A-P-4 (Alpha Providers):
   - Configure ISIS with group ISIS-GRP, overload bit, and level-2-only
   - Configure ISIS address families with wide metric style
   - Configure Loopback and GigabitEthernet interfaces under ISIS
   - Configure ISIS router instances AGG1 and CORE with group ISIS-GRP
• A-PE-1, A-PE-2, A-PE-3, A-PE-4 (Alpha Provider-Edge):
   - Configure ISIS with group ISIS-GRP, overload bit, and level-2-only
   - Configure ISIS address families with wide metric style
   - Configure Loopback and GigabitEthernet interfaces for ISIS
   - Apply ISIS group ISIS-GRP to router AGG1 with specified network
• A-RR-1, A-RR-2 (Alpha Route-Reflectors):
   - Enable IPv6 unicast routing
   - Configure interfaces for ISIS with point-to-point
   - Set ISIS network type and disable hello padding
   - Configure ISIS router with network address and level-2-only
   - Set metric and passive interface for ISIS