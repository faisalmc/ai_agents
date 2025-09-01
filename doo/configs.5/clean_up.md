To clean up configs for EVPN, l2VPN on Charlie

# C-ASBR-x

no router isis CORE
no router bgp 300
no segment-routing

# C-PE-1
no router isis CORE
no evpn
no l2vpn
no router bgp 300
no segment-routing

# C-P-x

no router isis CORE
no router bgp 300
no segment-routing
