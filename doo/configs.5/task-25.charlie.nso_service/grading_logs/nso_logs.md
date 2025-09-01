<div style="background-color:#ffcccc; padding:10px; font-family:monospace; white-space:pre">

admin@ncs# show running-config l3vpn
l3vpn site1
 ce                       [ M-CE-1 ]
 pe                       [ C-PE-3 ]
 ce-neighbor-ipv4         10.13.3.1
 ce-neighbor-ipv6         2620:fc7:13:3::1
 ce-ipv4-net-announce     10.3.1.3
 pe-neighbor-ipv4         10.13.3.2
 pe-neighbor-ipv6         2620:fc7:13:3::2
 pe-interface-gig-to-ce   0/0/0/5

l3vpn site2
 ce                       [ M-CE-2 ]
 pe                       [ C-PE-4 ]
 ce-neighbor-ipv4         10.13.4.1
 ce-neighbor-ipv6         2620:fc7:13:4::1
 ce-ipv4-net-announce     10.3.1.4
 pe-neighbor-ipv4         10.13.4.2
 pe-neighbor-ipv6         2620:fc7:13:4::2
 pe-interface-gig-to-ce   0/0/0/2
admin@ncs#

</div>
