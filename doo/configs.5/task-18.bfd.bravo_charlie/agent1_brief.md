# Agent-1 Summary for task-18.bfd.bravo_charlie

*Executive Summary:*
This task will configure BGP AS relationships and BFD settings on 2 ASBR devices for Beta and Charlie providers. 
The configuration aims to ensure proper BGP peering and enhance network reliability for the providers' services.

*Engineering Summary:*
• B-ASBR-1 (Beta Provider):
   - Establish BGP AS 200 with IPv4 and IPv6 unicast address families
   - Configure BFD for neighbor-group TO_C_ASBR with specific parameters
• C-ASBR-1 (Charlie Provider):
   - Establish BGP AS 300 with IPv4 and IPv6 unicast address families
   - Configure BFD for neighbor-group TO_B_ASBR with specific parameters

*Operational-Checks:*
• Show Commands for Validation:
   - Show BGP configuration
   - BGP neighbors summary
   - Show BFD sessions
   - Detailed BFD sessions
   - Show version information