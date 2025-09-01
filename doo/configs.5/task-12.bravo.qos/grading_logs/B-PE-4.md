# Grading Output for Task task-12.bravo.qos
**Device:** B-PE-4 (192.168.100.121)
_Generated: 2025-08-07 00:57:49.678258_

## show policy-map interface gigabitE 0/0/0/1 output

```
show policy-map interface gigabitE 0/0/0/1 output

Thu Aug  7 04:57:45.504 UTC

GigabitEthernet0/0/0/1 output: OUTBOUND_QOS

Class class-default
  Classification statistics          (packets/bytes)     (rate - kbps)
    Matched             :                   0/0                    0
    Transmitted         :                   0/0                    0
    Total Dropped       :                   0/0                    0

  Policy VIDEO_POLICY Class VIDEO
    Classification statistics          (packets/bytes)     (rate - kbps)
      Matched             :                   0/0                    0
      Transmitted         :                   0/0                    0
      Total Dropped       :                   0/0                    0
    Policing statistics                (packets/bytes)     (rate - kbps) 
      Policed(conform)    :                   0/0                    0
      Policed(exceed)     :                   0/0                    0
      Policed(violate)    :                   0/0                    0
      Policed and dropped :                   0/0                  
      Policed and dropped(parent policer)  : N/A
    Queueing statistics
      Queue ID                             : 40 
      High watermark                       : N/A 
      Inst-queue-len                       : N/A 
      Avg-queue-len                        : N/A 
      Taildropped(packets/bytes)           : 0/0
      Queue(conform)      :                   0/0                    0
      RED random drops(packets/bytes)      : 0/0


  Policy VIDEO_POLICY Class class-default
    Classification statistics          (packets/bytes)     (rate - kbps)
      Matched             :                   0/0                    0
      Transmitted         :                   0/0                    0
      Total Dropped       :                   0/0                    0
    Queueing statistics
      Queue ID                             : 41 
      High watermark                       : N/A 
      Inst-queue-len                       : N/A 
      Avg-queue-len                        : N/A 
      Taildropped(packets/bytes)           : 0/0
      Queue(conform)      :                   0/0                    0
      RED random drops(packets/bytes)      : 0/0


    Policy TO_S_CE3 Class TO_S_CE3
      Classification statistics          (packets/bytes)     (rate - kbps)
        Matched             :                   0/0                    0
        Transmitted         :                   0/0                    0
        Total Dropped       :                   0/0                    0
      Policing statistics                (packets/bytes)     (rate - kbps) 
        Policed(conform)    :                   0/0                    0
        Policed(exceed)     :                   0/0                    0
        Policed(violate)    :                   0/0                    0
        Policed and dropped :                   0/0                  
        Policed and dropped(parent policer)  : N/A
      Queueing statistics
        Queue ID                             : 41 
        High watermark                       : N/A 
        Inst-queue-len                       : N/A 
        Avg-queue-len                        : N/A 
        Taildropped(packets/bytes)           : 0/0
        Queue(conform)      :                   0/0                    0
        RED random drops(packets/bytes)      : 0/0


    Policy TO_S_CE3 Class class-default
      Classification statistics          (packets/bytes)     (rate - kbps)
        Matched             :                   0/0                    0
        Transmitted         :                   0/0                    0
        Total Dropped       :                   0/0                    0
      Queueing statistics
        Queue ID                             : 41 
        High watermark                       : N/A 
        Inst-queue-len                       : N/A 
        Avg-queue-len                        : N/A 
        Taildropped(packets/bytes)           : 0/0
        Queue(conform)      :                   0/0                    0
        RED random drops(packets/bytes)      : 0/0

RP/0/RP0/CPU0:B-PE-4#
```

