# Grading Output for Task taREMOVED7.charlie.srv6
**Device:** C-PE-3 (192.168.100.133)
_Generated: 2025-08-05 04:14:20.043277_

## show segment-routing srv6 manager

```
show segment-routing srv6 manager

Tue Aug  5 08:14:16.955 UTC
Parameters:
  SRv6 Enabled: Yes
  SRv6 Operational Mode: 
    Micro-segment:
      SID Base Block: fc00:100::/24
  Encapsulation:
    Source Address:
      Configured: 2620:fc7:3:101::3
      Default: 2620:fc7:3:101::3
    Hop-Limit: Default 
    Traffic-class: Default 
  SID Formats:
    f3216 <32B/16NFA> (2)
      uSID LIB Range:
        LIB Start   : 0xe000
        ELIB Start  : 0xfe00
      uSID WLIB Range:
        EWLIB Start : 0xfff7
Summary:
  Number of Locators: 1 (1 operational)
  Number of SIDs: 8 (0 stale)
  Max SID resources: 64000
  Number of free SID resources: 63992
  OOR:
    Thresholds (resources): Green 3200, Warning 1920
    Status: Resource Available
        History: (0 cleared, 0 warnings, 0 full)
    Block fc00:100::/32:
        Number of SIDs free: 7672
        Max SIDs: 7680
        Thresholds: Green 384, Warning 231
        Status: Resource Available
            History: (0 cleared, 0 warnings, 0 full)
    Block fc00:1ff::/32:
        Number of SIDs free: 7680
        Max SIDs: 7680
        Thresholds: Green 384, Warning 231
        Status: Resource Available
            History: (0 cleared, 0 warnings, 0 full)
Platform Capabilities:
  SRv6: Yes
  TILFA: Yes
  Microloop-Avoidance: Yes
  Endpoint behaviors: 
    End.DX6
    End.DX4
    End.DT6
    End.DT4
    End.DT46
    End.DX2
    End (PSP/USD)
    End.X (PSP/USD)
    uN (PSP/USD)
    uA (PSP/USD)
    uDT6
    uDT4
    uDT46
    uDX2
    uDT2U
    uDT2M
    uB6 (Insert.Red)
  Headend behaviors: 
    T
    H.Insert.Red
    H.Encaps.Red
    H.Encaps.L2.Red
  Security rules: 
    SEC-1
    SEC-2
    SEC-3
  Counters: 
    CNT-1
    CNT-3
  Signaled parameters: 
    Max-SL          : 3
    Max-End-Pop-SRH : 3
    Max-H-Insert    : 3 sids
    Max-H-Encap     : 3 sids
    Max-End-D       : 4
  Configurable parameters (under srv6): 
    Ranges: 
      LIB           : Yes
      WLIB          : Yes
    Encapsulation: 
      Source Address: Yes
      Hop-Limit     : value=Yes, propagate=No
      Traffic-class : value=Yes, propagate=Yes
  Default parameters (under srv6): 
    Encapsulation: 
      Hop-Limit     : value=0, propagate=No
      Traffic-class : value=0, propagate=No
  Max Locators: 16
  Max SIDs: 64000
  SID Holdtime: 3 mins
RP/0/RP0/CPU0:C-PE-3#
```

## show segment-routing srv6 manager | inc "Enabled|Configured|Base"

```
show segment-routing srv6 manager | inc "Enabled|Configured|Base"

Tue Aug  5 08:14:17.108 UTC
  SRv6 Enabled: Yes
      SID Base Block: fc00:100::/24
      Configured: 2620:fc7:3:101::3
RP/0/RP0/CPU0:C-PE-3#
```

## show isis segment-routing srv6 locators detail

```
show isis segment-routing srv6 locators detail

Tue Aug  5 08:14:17.235 UTC

IS-IS CORE SRv6 Locators
Name                  ID       Algo  Prefix                    Status
------                ----     ----  ------                    ------
CCIE_ALGO_0           1        0     fc00:100:3::/48           Active
  Advertised Level: level-1-2   
  Level: level-2-only Metric: 1        Administrative Tag: 300       
  SID behavior: uN (PSP/USD)
  SID value:    fc00:100:3::
  Block Length: 32, Node Length: 16, Func Length: 0, Args Length: 80

RP/0/RP0/CPU0:C-PE-3#
```

## show isis ipv6 route | inc "fc00|tag"

```
show isis ipv6 route | inc "fc00|tag"

Tue Aug  5 08:14:17.359 UTC
L2 fc00:100:1::/48 [21/115]
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2 tag 300, SRGB Base: 16000, Weight: 0
L2 fc00:100:2::/48 [11/115]
     via fe80::5054:ff:fe56:4116, GigabitEthernet0/0/0/2, C-PE-2 tag 300, SRGB Base: 16000, Weight: 0
C  fc00:100:3::/48
L2 fc00:100:4::/48 [11/115]
     via fe80::5054:ff:fe8b:19b8, GigabitEthernet0/0/0/1, C-PE-4 tag 300, SRGB Base: 16000, Weight: 0
L2 fc00:100:5::/48 [11/115]
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
L2 fc00:100:6::/48 [11/115]
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2 tag 300, SRGB Base: 16000, Weight: 0
L2 fc00:100:7::/48 [21/115]
     via fe80::5054:ff:fe91:6a26, GigabitEthernet0/0/0/3, C-P-1 tag 300, SRGB Base: 16000, Weight: 0
L2 fc00:100:8::/48 [21/115]
     via fe80::5054:ff:fec8:e10c, GigabitEthernet0/0/0/0, C-P-2 tag 300, SRGB Base: 16000, Weight: 0
RP/0/RP0/CPU0:C-PE-3#
```

