# IP change detect
## Detects if your IPV4 address changed and sends an email about it.

### login.txt
On the first run, if you do not have the **login.txt** in the running/working directory, The script will generate an empty one.
It is necessary for the email sending and should look like this:
```
sender@mail.com
password
receiver@mail.com
smtp.mail.com
```
_(Gmail no longer supports sending mail with an 'unsecure' solution like this.)_

### Running it with a system daemon
If you want to run it with a more simple utility tool, like crontab, where you can not set a running/working directory, then you can run the **bot.py** with az argument which leads to the directory where the login.txt and ip.txt are stored, for example:
```
*/15 * * * * python3 {path_to_directroy}/bot.py {path_to_directroy}
```
_In this instance the crontab runs the script every 15 mins._