import subprocess
import os
import smtplib, ssl
from email.mime.text import MIMEText
import sys

# Command to send to the CLI
command = "curl ipv4.icanhazip.com"
# Location argument
argument1 = ""
if len(sys.argv) > 1:
    argument1 = str(sys.argv[1])

if argument1 != "":
    print("bot.py location: " + argument1)
# Name of the file, which stores the IP (ipv4)
file_name = argument1 + "ip.txt"
# Some valuables for the script
file_ready = False
ip_ready = False
ip_changed = False
ip_stored = ""
ip_got = ""
send_mail = True

if os.path.exists(argument1+"login.txt"):
    print("login.txt found")
else:
    print("login.txt not found, exiting...")
    sys.exit()

# Check if file_name exists
if os.path.exists(file_name):
    print("ip.txt found")
    file_ready = True
    # Read file_name
    with open(file_name, 'r') as file:
        ip_stored = file.read().lstrip().rstrip()
        # Check if it has anything stored inside
        if ip_stored == "":
            print("IP stored: empty")
            ip_ready = False
        else:
            print("IP stored: " + ip_stored)
            ip_ready = True
# If file_name not found then it creates it
else:
    print(file_name + " not found")
    try:
        print("creating " + file_name)
        with open(file_name, 'w'):
            print(file_name + " created")
    except Exception as e:
        print("Error: {str(e)}")

try:
    # Run the command in the shell and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the command to complete and capture the output
    stdout, stderr = process.communicate()
    # Check if the command was successful (return code 0)
    if process.returncode == 0:
        # Starting of the IP compare
        print("Getting IP")
        ip_got = stdout.decode('utf-8').lstrip().rstrip()
        print("IP got: " + ip_got)
        # If we got IP stored in file_name (or anything stored in it)
        if ip_ready:
            # If the 2 IPs are equal it does nothing
            if ip_stored == ip_got:
                print("IP did not change (stored: " + ip_stored + ", got: " + ip_got + ")")
            # If they are not, then it rewrites the file_name with the new IP
            else:
                print("Your IP changed (stored: " + ip_stored + ", got: " + ip_got + ")")
                print("Storing IP")
                with open(file_name, 'w') as file:
                    file.write(ip_got)
                print("IP stored: " + ip_got)
                ip_changed = True
        # If file_name was empty or it was just created then writes the actual IP in it
        else:
            print("Storing IP")
            with open(file_name, 'w') as file:
                file.write(ip_got)
            print("IP stored: " + ip_got)
            ip_changed = True
    else:
        # Print any error messages
        print("Error:", stderr.decode('utf-8'))
except Exception as e:
    print("An error occurred:", str(e))

# Summary for CLI
print("\n=============== SUMMARY ================")
print("IP changed" if ip_changed else "IP not changed")
print("IP stored: empty" if ip_stored == "" else "Stored: " + ip_stored)
print("IP got: " + ip_got)

# If the IP changed, it sends a mail
if ip_changed and send_mail:
    print("\n================= EMAIL =================")
    # Gets the hostname of the computer for the mail subject
    process = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    hostname = stdout.decode('utf-8').lstrip().rstrip()
    print("Hostname found: " + hostname)
    # Email configuration
    print("Configuring e-mail service")
    # Reading login.txt
    with open(argument1 + "login.txt", 'r') as login_data:
        login = [line.strip() for line in login_data.readlines()]
    # Mail subject
    subject = "IP Changed (" + hostname + ")"
    print("Subject: " + subject)
    # Mail body
    body = "Your IP changed from " + ip_stored + " to " + ip_got + "."
    print("Body: " + body)
    # Mail sender
    sender = login[0]
    print("Sender: " + sender)
    # Mail password
    password = login[1]
    pw_hidden = ""
    for char in password: pw_hidden += "*"
    print("Password: " + pw_hidden)
    # Mail recipient
    recipients = [login[2]]
    print("Recipient: " + login[2])
    # Mail SMTP
    smtp = login[3]
    print("SMTP: " + smtp)

    # Send mail
    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp, 465, context=context) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")
    
    print("Sending mail")
    send_email(subject, body, sender, recipients, password)