# Full Output for Task taREMOVED18.bfd.bravo_charlie/
**Device:** C-ASBR-1 (192.168.100.137)
_Generated: 2025-07-06 02:53:24.060926_

## show run router bgp

```
show run router bgp

Sun Jul  6 06:40:50.530 UTC
router bgp 300
 bgp router-id 3.0.101.7
 address-family ipv4 unicast
 !
 address-family vpnv4 unicast
 !
 address-family ipv6 unicast
 !
 address-family vpnv6 unicast
 !
 neighbor-group IBGP
  remote-as 300
  update-source Loopback0
  address-family ipv4 unicast
  !
  address-family vpnv4 unicast
  !
  address-family ipv6 unicast
  !
  address-family vpnv6 unicast
  !
 !
 neighbor-group TO_B_ASBR
  remote-as 200
  bfd fast-detect
  bfd multiplier 5
  bfd minimum-interval 500
  address-family ipv4 unicast
  !
  address-family ipv6 unicast
  !
 !
 neighbor 3.0.101.1
  use neighbor-group IBGP
 !
 neighbor 3.0.101.2
  use neighbor-group IBGP
 !
 neighbor 3.0.101.3
  use neighbor-group IBGP
 !
 neighbor 3.0.101.4
  use neighbor-group IBGP
 !
 neighbor 100.64.231.1
  use neighbor-group TO_B_ASBR
 !
 neighbor 2620:fc7:64:231::1
  use neighbor-group TO_B_ASBR
 !
!

RP/0/RP0/CPU0:C-ASBR-1#
```

## show ip bgp neighbor brief

```
show ip bgp neighbor brief

Sun Jul  6 06:40:50.802 UTC

Neighbor         Spk    AS  Description                         Up/Down  NBRState
3.0.101.1         0   300                                         2d19h Idle        
3.0.101.2         0   300                                         2d19h Idle        
3.0.101.3         0   300                                         2d19h Idle        
3.0.101.4         0   300                                         2d19h Idle        
100.64.231.1      0   200                                      00:00:32 Established 
2620:fc7:64:231::1
                  0   200                                      00:00:44 Established 
RP/0/RP0/CPU0:C-ASBR-1#
```

## show bfd session

```
show bfd session

Sun Jul  6 06:40:50.949 UTC
Interface           Dest Addr           Local det time(int*mult)      State     
                                    Echo             Async   H/W   NPU     
------------------- --------------- ---------------- ---------------- ----------
Gi0/0/0/1           100.64.231.1    2500ms(500ms*5)  10s(2s*5)        UP        
                                                             No    n/a            


RP/0/RP0/CPU0:C-ASBR-1#
```

## show bfd session detail

```
show bfd session detail

Sun Jul  6 06:40:51.073 UTC
I/f: GigabitEthernet0/0/0/1, Location: 0/0/CPU0
Dest: 100.64.231.1
Src: 100.64.231.2
 State: UP for 0d:0h:0m:30s, number of times UP: 1
 Session type: PR/V4/SH
Received parameters:
 Version: 1, desired tx interval: 2 s, required rx interval: 2 s
 Required echo rx interval: 1 ms, multiplier: 5, diag: None
 My discr: 2148532226, your discr: 2148532226, state UP, D/F/P/C/A: 0/0/0/1/0
Transmitted parameters:
 Version: 1, desired tx interval: 2 s, required rx interval: 2 s
 Required echo rx interval: 1 ms, multiplier: 5, diag: None
 My discr: 2148532226, your discr: 2148532226, state UP, D/F/P/C/A: 0/0/0/1/0
Timer Values:
 Local negotiated async tx interval: 2 s
 Remote negotiated async tx interval: 2 s
 Desired echo tx interval: 500 ms, local negotiated echo tx interval: 500 ms
 Echo detection time: 2500 ms(500 ms*5), async detection time: 10 s(2 s*5)
Local Stats:
 Intervals between async packets:
   Tx: Number of intervals=17, min=2 ms, max=1956 ms, avg=1719 ms
       Last packet transmitted 1147 ms ago
   Rx: Number of intervals=17, min=3 ms, max=1959 ms, avg=1712 ms
       Last packet received 1256 ms ago
 Intervals between echo packets:
   Tx: Number of intervals=0, min=0 s, max=0 s, avg=0 s
       Last packet transmitted 364 ms ago
   Rx: Number of intervals=0, min=0 s, max=0 s, avg=0 s
       Last packet received 363 ms ago
 Latency of echo packets (time between tx and rx):
   Number of packets: 0, min=0 ms, max=0 ms, avg=0 ms
Session owner information:
                            Desired               Adjusted
  Client               Interval   Multiplier Interval   Multiplier
  -------------------- --------------------- ---------------------
  bgp-default          500 ms     5          2 s        5         




RP/0/RP0/CPU0:C-ASBR-1#
```

