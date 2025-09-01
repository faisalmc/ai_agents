# ERROR for Y-CE-3
_Time: 2025-08-07 01:49:23.798162_

```


Pattern not detected: 'show\\ ip\\ mroute' in output.

Things you might try to fix this:
1. Adjust the regex pattern to better identify the terminating string. Note, in
many situations the pattern is automatically based on the network device's prompt.
2. Increase the read_timeout to a larger value.

You can also look at the Netmiko session_log or debug log for more information.


```