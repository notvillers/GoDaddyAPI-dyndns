import subprocess
import os
import smtplib, ssl
from email.mime.text import MIMEText
import sys
import time

# Command to send to the CLI
command = "curl ipv4.icanhazip.com"

# Location argument
argument1 = ""
if len(sys.argv) > 1:
    argument1 = str(sys.argv[1])

# Name of the file, which stores the IP (ipv4)
ip_file = argument1 + "ip.txt"
login_file = argument1 + "login.txt"

# Some valuables for the script
file_ready = False
ip_ready = False
ip_changed = False
ip_stored = ""
ip_got = ""
send_mail = True

# If logint.txt is not found, then generating one
if not os.path.exists(login_file) and send_mail:
    print("login.txt not found, generating...")
    login_example = ["sender@example_mail.com", "password", "receiver@example_mail.com", "smtp.example_mail.com"]
    with open(login_file, 'w') as file:
        for line in login_example:
            file.write(line + "\n")
    print("login.txt created and filled with example data! \nExiting...")
    send_mail = False

# Check if ip.txt exists
if os.path.exists(ip_file):
    file_ready = True
    # Read ip.txt
    with open(ip_file, 'r') as file:
        ip_stored = file.read().lstrip().rstrip()
        # Check if it has anything stored inside
        if ip_stored != "":
            ip_ready = True
# If ip.txt not found then it creates it
else:
    print(ip_file + " not found, generating...")
    with open(ip_file, 'w'):
        print(ip_file + " created")

# Getting IP
try:
    # Run the command in the shell and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the command to complete and capture the output
    stdout, stderr = process.communicate()
    # Check if the command was successful (return code 0)
    if process.returncode == 0:
        # Starting of the IP compare
        ip_got = stdout.decode('utf-8').lstrip().rstrip()
        # If we got IP stored in ip.txt (or anything stored in it)
        if ip_ready:
            # If the 2 IPs are equal it does nothing
            if ip_stored != ip_got:
                with open(ip_file, 'w') as file:
                    file.write(ip_got)
                ip_changed = True
        # If file_name was empty or it was just created then writes the actual IP in it
        else:
            with open(ip_file, 'w') as file:
                file.write(ip_got)
            ip_changed = True
    else:
        # Print any error messages
        print("Error (cli):", stderr.decode('utf-8'))
        time.sleep(5)
        sys.exit()
except Exception as e:
    print("Error (ip get):", str(e))
    time.sleep(5)
    sys.exit()

# Summary for CLI
print("\n=============== SUMMARY ================")
print("IP changed" if ip_changed else "IP not changed")
print("IP stored: empty" if ip_stored == "" else "Stored: " + ip_stored)
print("IP got: " + ip_got)

# If the IP changed, it sends a mail
if ip_changed and send_mail:

    print("\n================= EMAIL =================")
    # Email configuration
    print("Configuring e-mail service")
    # Reading login.txt
    with open(argument1 + "login.txt", 'r') as login_data:
        login = [line.strip() for line in login_data.readlines()]
    smtp = login[3]

    if login[0] == "sender@example_mail.com":
        print("login.txt is not configured properly.\nExiting...")
        time.sleep(5)
        sys.exit()

    # Gets hostname from cli
    process = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    hostname = stdout.decode('utf-8').lstrip().rstrip()

    print("Calling send_email")

    # DEF: send mail
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

    send_email("IP change on " + hostname, "Your IP changed from " + ip_stored + " to " + ip_got + ".", login[0], [login[2]], login[1])