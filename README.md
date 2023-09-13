# Daddyndns
## Detects if your IPV4 address changed, sends an e-mail about it and updates the GoDaddy DNS record.

If you do not have or do not want to access any DynDNS service, this solution can help you survive.

> [!NOTE]
> GoDaddy DNS update is going live soon.

### login.txt
On the first run, if you do not have the **login.txt** in the running/working directory, The script will generate an empty one. It is necessary for the email sending and should look like this:

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
For this, you need to create and configure a **daddy_api.txt** like this:

```
example_domain.coms
example_type (A)
example_name (@)
api_key_example
api_secret_example
```

> [!IMPORTANT]
> At the moment, the code is not going to fill the **daddy.txt** with example and won't check if you modified it.