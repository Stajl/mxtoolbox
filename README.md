# mxtoolbox
mxtoolbox api, what check: is IP blacklisted on https://mxtoolbox.com/blacklists.aspx,
print in CLI output or send email only first listed output and Total Blacklists as counter 

### Usage
```
mxtoolbox.py
/usr/local/bin/mxtoolbox.py
/usr/local/bin/mxtoolbox.py --report >/dev/null
```
Options: --report - use sendmail to MAIL_TO, if listed_ips not empty

### EXAMPLE config.json
```
{
  "MAIL_TO": "YOUR_MAILTO",
  "MAIL_FROM": "YOUR_MAILFROM",
  "APIKEY": "YOUR_APIKEY",
  "ARRAY_IP": ["XXX.XXX.XXX.XXX","YYY.YYY.YYY.YYY"]
}
```

### API KEY mxtoolbox
https://mxtoolbox.com/user/api

Limit request per day to api in free account: 
Dns Requests Remaining Today: 64


https://api.mxtoolbox.com/api/v1/lookup/blacklist/188.119.120.35/
### EXAMPLE output
```
API Key: ********

Checking IP: 188.119.120.35

MX1: MXTOOLBOX IP Blacklist Report:

IP: 188.119.120.35
https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a188.119.120.35&run=toolpage#
Total Blacklists: 17
First Listed[0]:
{
  "Name": "Abusix Mail Intelligence Blacklist",
  "BlacklistReasonDescription": "Listed"
}
```
