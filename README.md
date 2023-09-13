# IP change detect
## Detects if your IPV4 address changed and sends an email about it.

If you do not have or do not want to access any DynDNS service, this solution can help you survive.

> [!NOTE]
> GoDaddy DNS API integration is coming, so it will be able to work without any interference.

### login.txt
On the first run, if you do not have the **login.txt** in the running/working directory, The script will generate an empty one. It is necessary for the email sending and should look like this:

```
sender@example_mail.com
password
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