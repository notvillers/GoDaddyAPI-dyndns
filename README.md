# Daddyndns
<img src="https://raw.githubusercontent.com/notvillers/GoDaddyAPI-dyndns/main/misc/godaddy_logo.png" alt="godaddy" width="75"/>

**Source problem:** You are running a server from home and if your public IP changes then you can not access it. A DynDNS service would help you but the free ones are slow and on low priority.

## Detects if your IPV4 address has been changed, sends an e-mail about it and updates the GoDaddy DNS record.
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
> [!IMPORTANT]
> You can validate your JSON [here](https://jsonlint.com/).

### Logging
On the first run, if you do not have the **log.txt**, it will generate it.
When you are running it by yourself, it writes out all of the logs to cli too.

### Running it with a system daemon
Example for running the bot with a simple utility tool like crontab:
```
*/15 * * * * python3 {path_to_directory}/bot.py
```
_(In this instance the script runs every 15 minutes.)_
A [helping hand](https://cron.help/) for the crontab syntax.

> [!NOTE]
> Removed the argument to add running/working directory, because I switched to `os.path.dirname(__file__)`.