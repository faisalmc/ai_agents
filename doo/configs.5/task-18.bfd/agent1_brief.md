# Agent-1 Summary for task-18.bfd

*Executive Summary:*
This initiative will configure BGP and BFD on 2 ASBR routers from different providers (Beta and Charlie). 
The enhancements will facilitate improved routing capabilities and faster fault detection, 
leading to increased network reliability and performance for our operations.

*Engineering Summary:*
• B-ASBR-1 (Provider: Beta):
   - Enable BGP with AS 200 for IPv4 and IPv6 unicast
   - Configure BFD for fast detection with specified parameters
   - Establish neighbor relationships with remote AS 300
   - **Expected State:**
     - BGP process should be running
     - Neighbors to remote AS 300 should be Established
     - AFI/SAFI for both IPv4 and IPv6 unicast active
   - **Suggested Show Commands:**
     - `show bgp summary`
     - `show bgp ipv4 unicast summary`
     - `show bgp ipv6 unicast summary`
     - `show run | section ^router bgp` (candidate)

• C-ASBR-1 (Provider: Charlie):
   - Enable BGP with AS 300 for IPv4 and IPv6 unicast
   - Configure BFD for fast detection with minimum interval and multiplier
   - Establish neighbor relationships with specified remote AS
   - **Expected State:**
     - BGP process should be running
     - Neighbors should be Established
     - AFI/SAFI for both IPv4 and IPv6 unicast active
     - BFD settings applied correctly
   - **Suggested Show Commands:**
     - `show bgp summary`
     - `show bgp ipv4 unicast summary`
     - `show bgp ipv6 unicast summary`
     - `show run | section ^router bgp` (candidate)

• Operational Checks (Validation Commands):
   - Show BGP configuration: `show run router bgp`
   - Show brief BGP neighbor status: `show ip bgp neighbor brief`
   - Show BFD session status: `show bfd session`
   - Show detailed BFD session information: `show bfd session detail`
   - Show device version: `show version`