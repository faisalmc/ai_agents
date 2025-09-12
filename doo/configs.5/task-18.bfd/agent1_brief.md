# Agent-1 Summary for taREMOVED18.bfd

*Executive Summary:*
This task will configure BGP AS relationships and BFD settings on 2 ASBR devices for Beta and Charlie providers. 
The configuration aims to establish stable BGP peering and enhance network fault detection capabilities.

*Engineering Summary:*
• B-ASBR-1 (Beta Provider):
   - Establish BGP AS 200 with IPv4 and IPv6 unicast address families
   - Configure BFD for neighbor-group TO_C_ASBR with specific parameters
   - Expected state checks for BGP and BFD
• C-ASBR-1 (Charlie Provider):
   - Establish BGP AS 300 with IPv4 and IPv6 unicast address families
   - Configure BFD for neighbor-group TO_B_ASBR with specific parameters
   - Expected state checks for BGP and BFD

*Operational Checks:*
• Validation Commands for BGP and BFD:
   - Show BGP configuration
   - BGP neighbors summary
   - BFD sessions summary
   - Detailed BFD sessions
   - Show version information