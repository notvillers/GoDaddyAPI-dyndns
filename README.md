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
You can use any amount of instances in the daddy_api.json.
> [!NOTE]
> You can validate your JSON [here](https://jsonlint.com/).

### Logging
On the first run, if you do not have the **log.txt** in the runnin/working directory, it will generate it.
When you are running it by yourself, it writes all of the logs to the cli too.

### Running it with a system daemon
If you want to run it with a more simple utility tool, like crontab, where you can not set a running/working directory, then you should run the **bot.py** with an argument which leads to the directory where the **login.txt** and **ip.txt** are stored, for example:
```
*/15 * * * * python3 {path_to_directory}/bot.py {path_to_directory}
```
where `{path_to_directory}` is the full path like `/home/user/bot/`
_In this instance the crontab runs the script every 15 mins._