# Daddyndns
## Detects if your IPV4 has address changed, sends an e-mail about it and updates the GoDaddy DNS record.

If you do not have or do not want to access any DynDNS service, this solution can help you survive.

### login.txt
On the first run, if you do not have the **login.txt** in the running/working directory, it will generate one with example data. It is necessary for the email sending and should look like this:

```
sender@example_mail.com
example_password
receiver@example_mail.com
smtp.example_mail.com
```

_(Gmail no longer supports sending mail with an 'unsecure' solution like this.)_

### Running it with a system daemon
If you want to run it with a more simple utility tool, like crontab, where you can not set a running/working directory, then you should run the **bot.py** with an argument which leads to the directory where the **login.txt** and **ip.txt** are stored, for example:

```
*/15 * * * * python3 {path_to_directory}/bot.py {path_to_directory}
```

where `{path_to_directory}` is the full path like `/home/user/bot/`

_In this instance the crontab runs the script every 15 mins._

### GoDaddy DNS update with API
On the first run, if you do not have the **daddy_api.json** in the running/working directory, it will generate one with example data. It is necessary for the GoDaddy API and should look like this:

```
[
    {
    "domain" : "example.com",
    "type": "A",
    "name": "@",
    "api_key": "Your_API_key",
    "api_secret": "Your_secret_API_key"
    },
    {
    "domain" : "second_example.com",
    "type": "A",
    "name": "@",
    "api_key": "Your_API_key",
    "api_secret": "Your_secret_API_key"
    },
]
```
> [!NOTE]
> You can use any amount of instances in the daddy_api.json.

### Logging
On the first run, if you do not have the **log.txt** in the runnin/working directory, it will generate it.

Example run in the **log.txt**
```
2023-09-18 17:04:42: ================== GO ==================
2023-09-18 17:04:42: stored ip: xxx.xxx.xxx.xxx
2023-09-18 17:04:42: ip got: yyy.yyy.yyy.yyy
2023-09-18 17:04:42: ip rewrote xxx.xxx.xxx.xxx -> yyy.yyy.yyy.yyy
2023-09-18 17:04:42: =============== SUMMARY ================
2023-09-18 17:04:42: IP changed
2023-09-18 17:04:42: Stored: xxx.xxx.xxx.xxx
2023-09-18 17:04:42: IP got: yyy.yyy.yyy.yyy
2023-09-18 17:04:42: ================= EMAIL =================
2023-09-18 17:04:43: Message sent!
2023-09-18 17:04:43: ================ GODADDY ================
2023-09-18 17:04:43: name 'updateResult' is not defined
2023-09-18 17:04:43:  ↳ Are you testing? This usually happens when no real IP change happened.
2023-09-18 17:04:43: ================= DONE =================
2023-09-18 17:06:39: ================== GO ==================
```
_Do not mind the GoDaddy error, I just did not want to update te DNS record. :shipit:_