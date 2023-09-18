#!/usr/bin/env python3

import subprocess
import os
import sys
import time
import funct.log_insert as log_insert
import funct.get_ip as get_ip
import funct.dns_email as dns_email
import funct.dns_daddy as dns_daddy

# Location argument
argument1 = ""
if len(sys.argv) > 1:
    argument1 = str(sys.argv[1])

# Name of the file, which stores the IP (ipv4)
ip_file = argument1 + "ip.txt"
login_file = argument1 + "login.txt"
daddy_api_file = argument1 + "daddy_api.txt"
log_file = argument1 + "log.txt"

# If log.txt not found, then generating one
summary_cli = "================== GO =================="
log_insert.insert(log_file, summary_cli)

# Some valuables for the script
file_ready = False
ip_ready = False
ip_stored = ""
ip_got = ""
send_mail = True
daddy_available = False
api_available = False

# If daddy_api.txt not found, then generating one
if os.path.exists(daddy_api_file):
    api_available = True
    daddy_available = True
else:
    log_insert.insert(log_file, daddy_api_file + " not found, generating")
    daddy_api_example = ["example_domain.com", "example_type (A)", "example_name (@)", "api_key_example", "api_secret_example"]
    with open(daddy_api_file, 'w') as file:
        for line in daddy_api_example:
            file.write(line + "\n")
    log_insert.insert(log_file, daddy_api_file + " created and filled with example data!")

# If logint.txt is not found, then generating one
if not os.path.exists(login_file):
    log_insert.insert(log_file, daddy_api_file + " created and filled with example data!")
    login_example = ["sender@example_mail.com", "password", "receiver@example_mail.com", "smtp.example_mail.com"]
    with open(login_file, 'w') as file:
        for line in login_example:
            file.write(line + "\n")
    log_insert.insert(log_file, login_file + " created and filled with example data!")
    send_mail = False

# If ip.txt is not found, then generating one, else stores it in ip_stored
if os.path.exists(ip_file):
    file_ready = True
    with open(ip_file, 'r') as file:
        ip_stored = file.read().lstrip().rstrip()
        log_insert.insert(log_file, "IP found in " + ip_file + ": " + ip_stored)
        if ip_stored != "":
            ip_ready = True
else:
    print(ip_file + " not found, generating...")
    log_insert.insert(log_file, ip_file + " not found, generating...")
    with open(ip_file, 'w') as file:
        log_insert.insert(log_file, ip_file + " created")

try:
    # Getting IP
    ip_got = get_ip.get_ip()
    log_insert.insert(log_file, "IP got from 'icanhazip': " + ip_got)
    # Starting of the IP compare
    if ip_ready:
        # If the 2 IPs are equal it does nothing
        if ip_stored != ip_got:
            with open(ip_file, 'w') as file:
                file.write(ip_got)
                log_insert.insert(log_file, "IP rewrote " + ip_stored + " -> " + ip_got)
    # If file_name was empty or it was just created then writes the actual IP in it
    else:
        with open(ip_file, 'w') as file:
            file.write(ip_got)
            log_insert.insert(log_file, "no IP stored, storing " + ip_got)
except Exception as e:
    print("Error (ip get):", str(e))
    time.sleep(5)
    sys.exit()

# Summary for CLI
summary_cli = "=============== SUMMARY ================"
log_insert.insert(log_file, summary_cli)
summary_cli = "IP changed" if ip_stored != ip_got else "IP not changed"
log_insert.insert(log_file, summary_cli)
summary_cli = "IP stored: empty" if ip_stored == "" else "Stored: " + ip_stored
log_insert.insert(log_file, summary_cli)
summary_cli = "IP got: " + ip_got
log_insert.insert(log_file, summary_cli)

# If the IP changed, it sends a mail
if (ip_stored != ip_got) and (send_mail is True):
    summary_cli = "================= EMAIL ================="
    log_insert.insert(log_file, summary_cli)
    # Reading login.txt
    with open(login_file, 'r') as login_data:
        login = [line.strip() for line in login_data.readlines()]

    # login.txt configuration check
    if login[0] == "sender@example_mail.com":
        summary_cli = login_file + " is not configured properly, GoDaddy API not available.\nExiting..."
        log_insert.insert(log_file, summary_cli)
    else:
        # Gets hostname from cli
        process = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        hostname = stdout.decode('utf-8').lstrip().rstrip()

        # Sending mail
        summary_cli = dns_email.send_email(
            subject = "IP change on " + hostname, 
            body = "Your IP changed from " + ip_stored + " to " + ip_got + ".", 
            sender = login[0], 
            recipients = [login[2]], 
            password = login[1],
            smtp = login[3]
        )
        log_insert.insert(log_file, summary_cli)

if (ip_stored != ip_got) and (api_available is True) and (daddy_available is True):
    summary_cli = "================ GODADDY ================"
    log_insert.insert(log_file, summary_cli)
    # Reading api.txt
    with open(daddy_api_file, 'r') as file:
        api_data = [line.strip() for line in file.readlines()]

    # Sending API call
    if "example_domain.com" not in api_data[0]:
        summary_cli = dns_daddy.daddy_api(
            d_key = api_data[3], 
            d_secret = api_data[4], 
            d_domain = api_data[0], 
            d_type = api_data[1], 
            d_record = api_data[2], 
            d_ip_got = ip_got
        )
        log_insert.insert(log_file, summary_cli)
        if "name 'updateResult' is not defined" in summary_cli:
            summary_cli = " ↳ Are you testing? This usually happens when no real IP change happened."
            log_insert.insert(log_file, summary_cli)
    else:
        summary_cli = "daddy_api.txt not configured properly"
        log_insert.insert(log_file, summary_cli)

summary_cli = "================= DONE ================="
log_insert.insert(log_file, summary_cli)