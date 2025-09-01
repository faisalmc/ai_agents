## A-ASBR-1.log

```
--- Config Push Log for A-ASBR-1 ---
Timestamp: 2025-08-21 06:33:16.462728

configure terminal

Thu Aug 21 06:33:12.248 UTC
RP/0/RP0/CPU0:A-ASBR-1(config)#no router isis AGG2

RP/0/RP0/CPU0:A-ASBR-1(config)#

RP/0/RP0/CPU0:A-ASBR-1(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-ASBR-1(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-1(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-ASBR-1(config)#!

RP/0/RP0/CPU0:A-ASBR-1(config)#router isis AGG2

RP/0/RP0/CPU0:A-ASBR-1(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-ASBR-1(config-isis)#net 49.0001.0001.0000.0101.0009.00

RP/0/RP0/CPU0:A-ASBR-1(config-isis)#!

RP/0/RP0/CPU0:A-ASBR-1(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#commit

Thu Aug 21 06:33:14.638 UTC
RP/0/RP0/CPU0:A-ASBR-1(config-isis-if)#
```

## A-ASBR-2.log

```
--- Config Push Log for A-ASBR-2 ---
Timestamp: 2025-08-21 06:33:20.612580

configure terminal

Thu Aug 21 06:33:16.162 UTC
RP/0/RP0/CPU0:A-ASBR-2(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-ASBR-2(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-ASBR-2(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-ASBR-2(config)#!

RP/0/RP0/CPU0:A-ASBR-2(config)#router isis AGG2

RP/0/RP0/CPU0:A-ASBR-2(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-ASBR-2(config-isis)#net 49.0001.0001.0000.0101.0010.00

RP/0/RP0/CPU0:A-ASBR-2(config-isis)#!

RP/0/RP0/CPU0:A-ASBR-2(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#!

RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#commit

Thu Aug 21 06:33:18.541 UTC
RP/0/RP0/CPU0:A-ASBR-2(config-isis-if)#
```

## A-P-1.log

```
--- Config Push Log for A-P-1 ---
Timestamp: 2025-08-21 06:32:54.038546

configure terminal

Thu Aug 21 06:32:48.941 UTC
RP/0/RP0/CPU0:A-P-1(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-P-1(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-P-1(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-P-1(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-P-1(config-GRP-isis)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-1(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-P-1(config)#!

RP/0/RP0/CPU0:A-P-1(config)#router isis AGG1

RP/0/RP0/CPU0:A-P-1(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-1(config-isis)#net 49.0001.0001.0000.0101.0005.00

RP/0/RP0/CPU0:A-P-1(config-isis)#!

RP/0/RP0/CPU0:A-P-1(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#root

RP/0/RP0/CPU0:A-P-1(config)#!

RP/0/RP0/CPU0:A-P-1(config)#router isis CORE

RP/0/RP0/CPU0:A-P-1(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-1(config-isis)#net 49.0001.0001.0000.0101.0005.00

RP/0/RP0/CPU0:A-P-1(config-isis)#!

RP/0/RP0/CPU0:A-P-1(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#interface GigabitEthernet0/0/0/3

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#interface GigabitEthernet0/0/0/4

RP/0/RP0/CPU0:A-P-1(config-isis-if)#!

RP/0/RP0/CPU0:A-P-1(config-isis-if)#commit

Thu Aug 21 06:32:51.978 UTC
RP/0/RP0/CPU0:A-P-1(config-isis-if)#
```

## A-P-2.log

```
--- Config Push Log for A-P-2 ---
Timestamp: 2025-08-21 06:32:59.171451

configure terminal

Thu Aug 21 06:32:53.694 UTC
RP/0/RP0/CPU0:A-P-2(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-P-2(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-P-2(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-P-2(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-P-2(config-GRP-isis)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-2(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-P-2(config)#!

RP/0/RP0/CPU0:A-P-2(config)#router isis AGG1

RP/0/RP0/CPU0:A-P-2(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-2(config-isis)#net 49.0001.0001.0000.0101.0006.00

RP/0/RP0/CPU0:A-P-2(config-isis)#!

RP/0/RP0/CPU0:A-P-2(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#interface GigabitEthernet0/0/0/4

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#root

RP/0/RP0/CPU0:A-P-2(config)#!

RP/0/RP0/CPU0:A-P-2(config)#router isis CORE

RP/0/RP0/CPU0:A-P-2(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-2(config-isis)#net 49.0001.0001.0000.0101.0006.00

RP/0/RP0/CPU0:A-P-2(config-isis)#!

RP/0/RP0/CPU0:A-P-2(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#interface GigabitEthernet0/0/0/3

RP/0/RP0/CPU0:A-P-2(config-isis-if)#!

RP/0/RP0/CPU0:A-P-2(config-isis-if)#commit

Thu Aug 21 06:32:56.692 UTC
RP/0/RP0/CPU0:A-P-2(config-isis-if)#
```

## A-P-3.log

```
--- Config Push Log for A-P-3 ---
Timestamp: 2025-08-21 06:33:04.051021

configure terminal

Thu Aug 21 06:32:59.070 UTC
RP/0/RP0/CPU0:A-P-3(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-P-3(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-P-3(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-P-3(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-P-3(config-GRP-isis)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-3(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-P-3(config)#!

RP/0/RP0/CPU0:A-P-3(config)#router isis AGG2

RP/0/RP0/CPU0:A-P-3(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-3(config-isis)#net 49.0001.0001.0000.0101.0007.00

RP/0/RP0/CPU0:A-P-3(config-isis)#!

RP/0/RP0/CPU0:A-P-3(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#root

RP/0/RP0/CPU0:A-P-3(config)#!

RP/0/RP0/CPU0:A-P-3(config)#router isis CORE

RP/0/RP0/CPU0:A-P-3(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-3(config-isis)#net 49.0001.0001.0000.0101.0007.00

RP/0/RP0/CPU0:A-P-3(config-isis)#!

RP/0/RP0/CPU0:A-P-3(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#interface GigabitEthernet0/0/0/3

RP/0/RP0/CPU0:A-P-3(config-isis-if)#!

RP/0/RP0/CPU0:A-P-3(config-isis-if)#interface GigabitEthernet0/0/0/4

RP/0/RP0/CPU0:A-P-3(config-isis-if)#commit

Thu Aug 21 06:33:02.068 UTC
RP/0/RP0/CPU0:A-P-3(config-isis-if)#
```

## A-P-4.log

```
--- Config Push Log for A-P-4 ---
Timestamp: 2025-08-21 06:33:09.054971

configure terminal

Thu Aug 21 06:33:03.886 UTC
RP/0/RP0/CPU0:A-P-4(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-P-4(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-P-4(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-P-4(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-P-4(config-GRP-isis)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-P-4(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-P-4(config)#!

RP/0/RP0/CPU0:A-P-4(config)#router isis AGG2

RP/0/RP0/CPU0:A-P-4(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-4(config-isis)#net 49.0001.0001.0000.0101.0008.00

RP/0/RP0/CPU0:A-P-4(config-isis)#!

RP/0/RP0/CPU0:A-P-4(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#interface GigabitEthernet0/0/0/4

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#root

RP/0/RP0/CPU0:A-P-4(config)#!

RP/0/RP0/CPU0:A-P-4(config)#router isis CORE

RP/0/RP0/CPU0:A-P-4(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-P-4(config-isis)#net 49.0001.0001.0000.0101.0008.00

RP/0/RP0/CPU0:A-P-4(config-isis)#!

RP/0/RP0/CPU0:A-P-4(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#interface GigabitEthernet0/0/0/1

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#interface GigabitEthernet0/0/0/3

RP/0/RP0/CPU0:A-P-4(config-isis-if)#!

RP/0/RP0/CPU0:A-P-4(config-isis-if)#commit

Thu Aug 21 06:33:06.954 UTC
RP/0/RP0/CPU0:A-P-4(config-isis-if)#
```

## A-PE-1.log

```
--- Config Push Log for A-PE-1 ---
Timestamp: 2025-08-21 06:32:37.122867

configure terminal

Thu Aug 21 06:32:32.511 UTC
RP/0/RP0/CPU0:A-PE-1(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-PE-1(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if)#passive

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-1(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-PE-1(config)#!

RP/0/RP0/CPU0:A-PE-1(config)#router isis AGG1

RP/0/RP0/CPU0:A-PE-1(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-PE-1(config-isis)#net 49.0001.0001.0000.0101.0001.00

RP/0/RP0/CPU0:A-PE-1(config-isis)#!

RP/0/RP0/CPU0:A-PE-1(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-1(config-isis-if)#commit

Thu Aug 21 06:32:34.884 UTC
RP/0/RP0/CPU0:A-PE-1(config-isis-if)#
```

## A-PE-2.log

```
--- Config Push Log for A-PE-2 ---
Timestamp: 2025-08-21 06:32:41.101622

configure terminal

Thu Aug 21 06:32:37.055 UTC
RP/0/RP0/CPU0:A-PE-2(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-PE-2(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-2(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-PE-2(config)#!

RP/0/RP0/CPU0:A-PE-2(config)#router isis AGG1

RP/0/RP0/CPU0:A-PE-2(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-PE-2(config-isis)#net 49.0001.0001.0000.0101.0002.00

RP/0/RP0/CPU0:A-PE-2(config-isis)#!

RP/0/RP0/CPU0:A-PE-2(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#interface GigabitEthernet0/0/0/2

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#

RP/0/RP0/CPU0:A-PE-2(config-isis-if)#commit

Thu Aug 21 06:32:39.313 UTC
RP/0/RP0/CPU0:A-PE-2(config-isis-if)#
```

## A-PE-3.log

```
--- Config Push Log for A-PE-3 ---
Timestamp: 2025-08-21 06:32:45.082418

configure terminal

Thu Aug 21 06:32:40.864 UTC
RP/0/RP0/CPU0:A-PE-3(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-PE-3(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-3(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-PE-3(config)#!

RP/0/RP0/CPU0:A-PE-3(config)#router isis AGG1

RP/0/RP0/CPU0:A-PE-3(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-PE-3(config-isis)#net 49.0001.0001.0000.0101.0003.00

RP/0/RP0/CPU0:A-PE-3(config-isis)#!

RP/0/RP0/CPU0:A-PE-3(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-PE-3(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-3(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-PE-3(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-3(config-isis-if)#commit

Thu Aug 21 06:32:43.032 UTC
RP/0/RP0/CPU0:A-PE-3(config-isis-if)#
```

## A-PE-4.log

```
--- Config Push Log for A-PE-4 ---
Timestamp: 2025-08-21 06:32:49.062629

configure terminal

Thu Aug 21 06:32:44.704 UTC
RP/0/RP0/CPU0:A-PE-4(config)#group ISIS-GRP

RP/0/RP0/CPU0:A-PE-4(config-GRP)#router isis '.*'

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis)#set-overload-bit on-startup 180

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis)#is-type level-2-only

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#metric-style wide

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#single-topology

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-af)#interface 'Loopback.*'

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#interface 'GigabitEthernet.*'

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if)#point-to-point

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if)#address-family ipv4 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#metric 100 level 2

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#address-family ipv6 unicast

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#metric 200 level 2

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#!

RP/0/RP0/CPU0:A-PE-4(config-GRP-isis-if-af)#root

RP/0/RP0/CPU0:A-PE-4(config)#!

RP/0/RP0/CPU0:A-PE-4(config)#router isis AGG2

RP/0/RP0/CPU0:A-PE-4(config-isis)#apply-group ISIS-GRP

RP/0/RP0/CPU0:A-PE-4(config-isis)#net 49.0001.0001.0000.0101.0004.00

RP/0/RP0/CPU0:A-PE-4(config-isis)#!

RP/0/RP0/CPU0:A-PE-4(config-isis)#interface Loopback0

RP/0/RP0/CPU0:A-PE-4(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-4(config-isis-if)#interface GigabitEthernet0/0/0/0

RP/0/RP0/CPU0:A-PE-4(config-isis-if)#!

RP/0/RP0/CPU0:A-PE-4(config-isis-if)#

RP/0/RP0/CPU0:A-PE-4(config-isis-if)#commit

Thu Aug 21 06:32:46.932 UTC
RP/0/RP0/CPU0:A-PE-4(config-isis-if)#
```

## A-RR-1.log

```
--- Config Push Log for A-RR-1 ---
Timestamp: 2025-08-21 06:33:10.875227

configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
A-RR-1(config)#ipv6 unicast-routing
A-RR-1(config)#interface GigabitEthernet2
A-RR-1(config-if)#ip router isis
A-RR-1(config-if)#ipv6 router isis
A-RR-1(config-if)#isis network point-to-point
A-RR-1(config-if)#no isis hello padding always
A-RR-1(config-if)#!
A-RR-1(config-if)#interface GigabitEthernet3
A-RR-1(config-if)#ip router isis
A-RR-1(config-if)#ipv6 router isis
A-RR-1(config-if)#isis network point-to-point
A-RR-1(config-if)#no isis hello padding always
A-RR-1(config-if)#!
A-RR-1(config-if)#interface Loopback0
A-RR-1(config-if)#ip router isis
A-RR-1(config-if)#ipv6 router isis
A-RR-1(config-if)#!
A-RR-1(config-if)#router isis
A-RR-1(config-router)#net 49.0001.0001.0000.0101.0011.00
A-RR-1(config-router)#is-type level-2-only
A-RR-1(config-router)#metric-style wide
A-RR-1(config-router)#metric 100 level-2
A-RR-1(config-router)#passive-interface Loopback0
A-RR-1(config-router)#!
A-RR-1(config-router)#address-family ipv6
A-RR-1(config-router-af)#metric 200 level-2
A-RR-1(config-router-af)#exit-address-family
A-RR-1(config-router)#!
A-RR-1(config-router)#end
A-RR-1#
```

## A-RR-2.log

```
--- Config Push Log for A-RR-2 ---
Timestamp: 2025-08-21 06:33:12.533819

configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
A-RR-2(config)#ipv6 unicast-routing
A-RR-2(config)#interface GigabitEthernet2
A-RR-2(config-if)#ip router isis
A-RR-2(config-if)#ipv6 router isis
A-RR-2(config-if)#isis network point-to-point
A-RR-2(config-if)#no isis hello padding always
A-RR-2(config-if)#!
A-RR-2(config-if)#interface GigabitEthernet3
A-RR-2(config-if)#ip router isis
A-RR-2(config-if)#ipv6 router isis
A-RR-2(config-if)#isis network point-to-point
A-RR-2(config-if)#no isis hello padding always
A-RR-2(config-if)#!
A-RR-2(config-if)#interface Loopback0
A-RR-2(config-if)#ip router isis
A-RR-2(config-if)#ipv6 router isis
A-RR-2(config-if)#!
A-RR-2(config-if)#router isis
A-RR-2(config-router)#net 49.0001.0001.0000.0101.0012.00
A-RR-2(config-router)#is-type level-2-only
A-RR-2(config-router)#metric-style wide
A-RR-2(config-router)#metric 100 level-2
A-RR-2(config-router)#passive-interface Loopback0
A-RR-2(config-router)#!
A-RR-2(config-router)#address-family ipv6
A-RR-2(config-router-af)#metric 200 level-2
A-RR-2(config-router-af)#exit-address-family
A-RR-2(config-router)#!
A-RR-2(config-router)#end
A-RR-2#
```

