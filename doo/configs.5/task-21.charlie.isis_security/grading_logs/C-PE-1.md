# Grading Output for Task task-21.charlie.isis_security
**Device:** C-PE-1 (192.168.100.131)
_Generated: 2025-08-07 04:37:33.424719_

## show isis database detail

```
show isis database detail

Thu Aug  7 08:37:28.515 UTC

IS-IS CORE (Level-2) Link State Database
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd  ATT/P/OL
C-PE-1.00-00        * 0x000000ec   0xee04        911  /*            0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.1
  IP Address:     3.0.101.1
  IPv6 Address:   2620:fc7:3:101::1
  Hostname:       C-PE-1
  Router Cap:     3.0.101.1 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:1::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-2.00
  Metric: 10         IS-Extended C-P-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-1.00
  Metric: 0          IP-Extended 3.0.101.1/32
  Metric: 10         IP-Extended 3.3.8.0/24
  Metric: 10         IP-Extended 3.3.9.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:8::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:9::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::1/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:1::/48
C-PE-2.00-00          0x000000ed   0x0e8e        915  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.2
  IP Address:     3.0.101.2
  IPv6 Address:   2620:fc7:3:101::2
  Hostname:       C-PE-2
  Router Cap:     3.0.101.2 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:2::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-1.00
  Metric: 10         IS-Extended C-PE-3.00
  Metric: 10         IS-Extended C-P-1.00
  Metric: 10         IS-Extended C-P-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-3.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-2.00
  Metric: 0          IP-Extended 3.0.101.2/32
  Metric: 10         IP-Extended 3.3.5.0/24
  Metric: 10         IP-Extended 3.3.9.0/24
  Metric: 10         IP-Extended 3.3.10.0/24
  Metric: 10         IP-Extended 3.3.11.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:5::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:9::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:10::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:11::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::2/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:2::/48
C-PE-3.00-00          0x000000ed   0x4b71        919  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.3
  IP Address:     3.0.101.3
  IPv6 Address:   2620:fc7:3:101::3
  Hostname:       C-PE-3
  Router Cap:     3.0.101.3 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:3::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-2.00
  Metric: 10         IS-Extended C-PE-4.00
  Metric: 10         IS-Extended C-P-1.00
  Metric: 10         IS-Extended C-P-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-4.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-2.00
  Metric: 0          IP-Extended 3.0.101.3/32
  Metric: 10         IP-Extended 3.3.4.0/24
  Metric: 10         IP-Extended 3.3.7.0/24
  Metric: 10         IP-Extended 3.3.10.0/24
  Metric: 10         IP-Extended 3.3.12.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:4::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:7::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:10::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:12::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::3/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:3::/48
C-PE-4.00-00          0x000000ea   0x462e        922  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.4
  IP Address:     3.0.101.4
  IPv6 Address:   2620:fc7:3:101::4
  Hostname:       C-PE-4
  Router Cap:     3.0.101.4 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:4::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-3.00
  Metric: 10         IS-Extended C-P-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-3.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-2.00
  Metric: 0          IP-Extended 3.0.101.4/32
  Metric: 0          IP-Extended 3.0.101.66/32
  Metric: 10         IP-Extended 3.3.6.0/24
  Metric: 10         IP-Extended 3.3.12.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:6::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:12::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::4/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:4::/48
C-P-1.00-00           0x000000ec   0x6091        926  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.5
  IP Address:     3.0.101.5
  IPv6 Address:   2620:fc7:3:101::5
  Hostname:       C-P-1
  Router Cap:     3.0.101.5 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:5::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-1.00
  Metric: 10         IS-Extended C-PE-2.00
  Metric: 10         IS-Extended C-PE-3.00
  Metric: 10         IS-Extended C-P-2.00
  Metric: 10         IS-Extended C-ASBR-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-3.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-ASBR-1.00
  Metric: 0          IP-Extended 3.0.101.5/32
  Metric: 10         IP-Extended 3.3.1.0/24
  Metric: 10         IP-Extended 3.3.3.0/24
  Metric: 10         IP-Extended 3.3.4.0/24
  Metric: 10         IP-Extended 3.3.5.0/24
  Metric: 10         IP-Extended 3.3.8.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:1::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:3::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:4::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:5::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:8::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::5/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:5::/48
C-P-2.00-00           0x000000ea   0x9633        930  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  Router ID:      3.0.101.6
  IP Address:     3.0.101.6
  IPv6 Address:   2620:fc7:3:101::6
  Hostname:       C-P-2
  Router Cap:     3.0.101.6 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:6::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-PE-2.00
  Metric: 10         IS-Extended C-PE-3.00
  Metric: 10         IS-Extended C-PE-4.00
  Metric: 10         IS-Extended C-P-1.00
  Metric: 10         IS-Extended C-ASBR-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-3.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-PE-4.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-ASBR-2.00
  Metric: 0          IP-Extended 3.0.101.6/32
  Metric: 10         IP-Extended 3.3.2.0/24
  Metric: 10         IP-Extended 3.3.3.0/24
  Metric: 10         IP-Extended 3.3.6.0/24
  Metric: 10         IP-Extended 3.3.7.0/24
  Metric: 10         IP-Extended 3.3.11.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:2::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:3::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:6::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:7::/64
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:11::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::6/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:6::/48
C-ASBR-1.00-00        0x000000e8   0xcd1a        934  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  IP Address:     3.0.101.7
  IPv6 Address:   2620:fc7:3:101::7
  Hostname:       C-ASBR-1
  Router Cap:     3.0.101.7 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:7::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-P-1.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-1.00
  Metric: 0          IP-Extended 3.0.101.7/32
  Metric: 10         IP-Extended 3.3.1.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:1::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::7/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:7::/48
C-ASBR-2.00-00        0x000000eb   0x52fb        937  /1200         0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1001
  LSP MTU:        1492
  NLPID:          0xcc
  NLPID:          0x8e
  MT:             Standard (IPv4 Unicast)
  MT:             IPv6 Unicast                                 0/0/0
  IP Address:     3.0.101.8
  IPv6 Address:   2620:fc7:3:101::8
  Hostname:       C-ASBR-2
  Router Cap:     3.0.101.8 D:0 S:0
  SRv6 Locator:   MT (IPv6 Unicast) fc00:100:8::/48 D:0 Metric: 1 Algorithm: 0
  Metric: 10         IS-Extended C-P-2.00
  Metric: 10         MT (IPv6 Unicast) IS-Extended C-P-2.00
  Metric: 0          IP-Extended 3.0.101.8/32
  Metric: 10         IP-Extended 3.3.2.0/24
  Metric: 10         IP-Extended 3.3.14.0/24
  Metric: 10         MT (IPv6 Unicast) IPv6 2620:fc7:3:2::/64
  Metric: 0          MT (IPv6 Unicast) IPv6 2620:fc7:3:101::8/128
  Metric: 1          MT (IPv6 Unicast) IPv6 fc00:100:8::/48

 Total Level-2 LSP count: 8     Local Level-2 LSP count: 1
RP/0/RP0/CPU0:C-PE-1#
```

## show isis neighbor

```
show isis neighbor

Thu Aug  7 08:37:28.653 UTC

IS-IS CORE neighbors:
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
C-PE-2         Gi0/0/0/1        *PtoP*         Up    25       L2   Capable 
C-P-1          Gi0/0/0/0        *PtoP*         Up    22       L2   Capable 

Total neighbor count: 2
RP/0/RP0/CPU0:C-PE-1#
```

## show ip route isis

```
show ip route isis

Thu Aug  7 08:37:28.818 UTC

i L2 3.0.101.2/32 [115/10] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0 (!)
i L2 3.0.101.3/32 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.4/32 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.5/32 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1 (!)
                  [115/10] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.6/32 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                  [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.7/32 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1 (!)
                  [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.8/32 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                  [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.0.101.66/32 [115/30] via 3.0.101.4, 2d01h, srte_c_66_ep_3.0.101.4
i L2 3.3.1.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.2.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.3.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.4.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1 (!)
                [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.5.0/24 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                [115/20] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.6.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.7.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.10.0/24 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0 (!)
i L2 3.3.11.0/24 [115/20] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0 (!)
i L2 3.3.12.0/24 [115/30] via 3.3.9.2, 2d00h, GigabitEthernet0/0/0/1
                 [115/30] via 3.3.8.2, 2d00h, GigabitEthernet0/0/0/0
i L2 3.3.14.0/24 [115/40] via 3.3.9.2, 01:24:52, GigabitEthernet0/0/0/1
                 [115/40] via 3.3.8.2, 01:24:52, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-1#
```

## show route ipv6 isis

```
show route ipv6 isis

Thu Aug  7 08:37:29.089 UTC

i L2 2620:fc7:3:1::/64 
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:2::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:3::/64 
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:4::/64 
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:5::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:6::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:7::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:10::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:11::/64 
      [115/20] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:12::/64 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::2/128 
      [115/10] via fe80::5054:ff:fe39:b02f, 00:19:07, GigabitEthernet0/0/0/1
i L2 2620:fc7:3:101::3/128 
      [115/20] via fe80::5054:ff:fe39:b02f, 00:19:07, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::4/128 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:07, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::5/128 
      [115/10] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::6/128 
      [115/20] via fe80::5054:ff:fe39:b02f, 00:19:07, GigabitEthernet0/0/0/1
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::7/128 
      [115/20] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 2620:fc7:3:101::8/128 
      [115/30] via fe80::5054:ff:fe39:b02f, 00:19:07, GigabitEthernet0/0/0/1
      [115/30] via fe80::5054:ff:fea5:ba01, 00:19:07, GigabitEthernet0/0/0/0
i L2 fc00:100:2::/48 
      [115/11] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0 (!)
i L2 fc00:100:3::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 fc00:100:4::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/31] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 fc00:100:5::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1 (!)
      [115/11] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 fc00:100:6::/48 
      [115/21] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/21] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 fc00:100:7::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1 (!)
      [115/21] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
i L2 fc00:100:8::/48 
      [115/31] via fe80::5054:ff:fe39:b02f, 00:19:06, GigabitEthernet0/0/0/1
      [115/31] via fe80::5054:ff:fea5:ba01, 00:19:06, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:C-PE-1#
```

