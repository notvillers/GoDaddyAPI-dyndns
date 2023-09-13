# IP change detect
## Detects if your IPV4 address changed and sends an email about it.

Your login.txt should look like this:

```
sender@mail.com
password
receiver@mail.com
smtp.mail.com
```

_(Gmail no longer supports sending mail with an unsecure solution like this.)_

## Running it with a daemon

If you want to run it with a more simple utility tool, like crontab, where you can not set a running/working directory, then you can run the bot.py with az argument which leads to the directory where the login.txt is stored, for example:

```
*/15 * * * * python3 {path_to_directroy}/bot.py {path_to_directroy}
```

In this instance the crontab runs the script every 15 mins.