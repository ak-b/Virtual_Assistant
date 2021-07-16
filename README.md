# Awesom-o

Awesom-o (inspired by South Park) is a security bot to be used by the Customer Engagement Team to peek inside our infrastructure.




![Awesom-o](https://wwwin-github.cisco.com/webex-iaas/Awesom-o/blob/master/files/Awesomo-0.png)

Key Features that are supported :

+ Searching in customer DB to see if we are blocking legitimate traffic
+ Search ACL on ASAs and clusters
+ Search about IP reputation & Cisco Talos
+ Search Feed allow/deny list
+ Search Abuse DB
+ Search if a specific server port is open on the firewall
+ Check route path between source and destination IPs**
+ Check for ACL106 blocks
+ Fraud Escalation (**)
GitHub: https://wwwin-github.cisco.com/webex-iaas/Awesom-o

** This feature is not part of immediate delivery, will require further grooming and planning

The bot will be used by specific users of the team, we are decoupling external teams to use any tool or bot that can pose a security risk if hacked. Awesom-o will NOT make any changes or edits to the WebEx infrastructure or its endpoints. All changes to the network have to be recorded via a SNOW(Service Now ticket) and must be performed after an audit by a firewall team member and approval by management.

Usage Guide: 
https://wiki.cisco.com/display/AS13445/Awesom-o%27s+Usage+Guide



![Menu](https://wwwin-github.cisco.com/webex-iaas/Awesom-o/blob/master/files/feat.png)

Portfolio Request:
https://jira-eng-gpk2.cisco.com/jira/browse/EVS-3896
