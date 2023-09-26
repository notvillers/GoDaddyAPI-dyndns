#!/usr/bin/env python3

import subprocess
import os
import sys
import time
import funct.log_insert as log_insert
import funct.get_ip as get_ip
import funct.dns_email as dns_email
import funct.json_read as json_read
import funct.dns_daddy as dns_daddy

def run(path):
    def_log = []

    file_path = path

    # Name of the file, which stores the IP (ipv4)
    ip_file = file_path + "ip.txt"
    login_file = file_path + "login.txt"
    daddy_api_json_file = file_path + "daddy_api.json"
    log_file = file_path + "log.txt"

    # If log.txt not found, then generating one
    summary_cli = "================== GO =================="
    def_log.append(log_insert.insert(log_file, summary_cli, True))

    # Some valuables for the script
    ip_ready = False
    ip_stored = ""
    ip_got = ""
    send_mail = True
    daddy_available = True
    api_available = True

    # If logint.txt is not found, then generating one
    if not os.path.exists(login_file):
        login_example = ["sender@example_mail.com", "password", "receiver@example_mail.com", "smtp.example_mail.com"]
        with open(login_file, 'w') as file:

            for line in login_example:
                file.write(line + "\n")
            summary_cli = login_file + " created and filled with example data."
            def_log.append(log_insert.insert(log_file, summary_cli, True))
        send_mail = False

    # If ip.txt is not found, then generating one, else stores it in ip_stored

    if os.path.exists(ip_file):
        file_ready = True

        with open(ip_file, 'r') as file:
            ip_stored = file.read().lstrip().rstrip()
            summary_cli = "IP found in " + ip_file + ": " + ip_stored + "."
            def_log.append(log_insert.insert(log_file, summary_cli, True))
            if ip_stored != "":
                ip_ready = True

    else:
        summary_cli = ip_file + " not found, generating..."
        def_log.append(log_insert.insert(log_file, summary_cli, True))

        with open(ip_file, 'w') as file:
            summary_cli = ip_file + " created."
            def_log.append(log_insert.insert(log_file, summary_cli, True))

    # Main
    try:
        # Getting IP
        ip_got = get_ip.get_ip()
        summary_cli = "IP got from 'icanhazip': " + ip_got + "."
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        # Starting of the IP compare

        if ip_ready:
            # If the 2 IPs are equal it does nothing

            if ip_stored != ip_got:

                with open(ip_file, 'w') as file:
                    file.write(ip_got)
                    summary_cli = "IP rewrote " + ip_stored + " -> " + ip_got + "."
                    def_log.append(log_insert.insert(log_file, summary_cli, True))
        # If file_name was empty or it was just created then writes the actual IP in it

        else:

            with open(ip_file, 'w') as file:
                file.write(ip_got)
                summary_cli = "no IP stored, storing " + ip_got
                def_log.append(log_insert.insert(log_file, summary_cli, True))

    except Exception as e:
        summary_cli = "Error (ip get): " + str(e)
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        sys.exit()

    # Summary for cli and log.txt
    summary_cli = "=============== SUMMARY ================"
    def_log.append(log_insert.insert(log_file, summary_cli, True))

    if ip_stored == ip_got:
        summary_cli = "IP not changed."
        def_log.append(log_insert.insert(log_file, summary_cli, True))

    else:
        summary_cli = "IP changed"
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        summary_cli = "IP got: " + ip_got
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        summary_cli = "IP stored: empty" if ip_stored == "" else "IP stored: " + ip_stored
        def_log.append(log_insert.insert(log_file, summary_cli, True))

    # If the IP changed, it sends a mail
    if (ip_stored != ip_got) and (send_mail is True):
        summary_cli = "================= EMAIL ================="
        def_log.append(log_insert.insert(log_file, summary_cli, True))

        # Reading login.txt
        with open(login_file, 'r') as login_data:
            login = [line.strip() for line in login_data.readlines()]
            summary_cli = login_file + " data read."
            def_log.append(log_insert.insert(log_file, summary_cli, True))

        # login.txt configuration check
        if login[0] == "sender@example_mail.com":
            summary_cli = login_file + " is not configured properly"
            def_log.append(log_insert.insert(log_file, summary_cli, True))

        else:
            # Gets hostname from cli
            process = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            hostname = stdout.decode('utf-8').lstrip().rstrip()
            summary_cli = "Hostname found: " + hostname
            def_log.append(log_insert.insert(log_file, summary_cli, True))

            # Sending mail
            summary_cli = dns_email.send_email(
                subject = "IP change on " + hostname, 
                body = "Your IP changed from " + ip_stored + " to " + ip_got + ".", 
                sender = login[0], 
                recipients = [login[2]], 
                password = login[1],
                smtp = login[3]
            )
            def_log.append(log_insert.insert(log_file, summary_cli, True))

    # If api_available then is gets the data(s) from the daddy_api.json
    if api_available is True:
        summary_cli = "================ GODADDY ================"
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        # daddy_api.json reader
        api_data_got = json_read.daddy_api(daddy_api_json_file)

        if api_data_got[1] == 0:
            summary_cli = daddy_api_json_file + " created and filled with example data."
            daddy_available = False

        elif api_data_got[1] == -1:
            summary_cli = daddy_api_json_file + " is not a valid JSON."
            daddy_available = False

        else:
            summary_cli = "Domains found in " + daddy_api_json_file + ": " + str(api_data_got[1])
        def_log.append(log_insert.insert(log_file, summary_cli, True))

    # If IP changed and api_available and daddy_available then runs the API call with the daddy_api.json's data(s)
    if (ip_stored != ip_got) and (api_available is True) and (daddy_available is True):
        summary_cli = "API call is available."
        def_log.append(log_insert.insert(log_file, summary_cli, True))
        # Calling GoDaddy's API
        
        for api_data in api_data_got[0]:

            if api_data[0] != "example.com":
                summary_cli = dns_daddy.daddy_api(
                    d_key = api_data[3], 
                    d_secret = api_data[4], 
                    d_domain = api_data[0], 
                    d_type = api_data[1], 
                    d_record = api_data[2], 
                    d_ip_got = ip_got
                )
                summary_cli = "(" + api_data[0] + ") " + summary_cli 
                def_log.append(log_insert.insert(log_file, summary_cli, True))

                if "name 'updateResult' is not defined" in summary_cli:
                    summary_cli = " ↳ Are you testing on ? This usually happens when no real IP change happened on."
                    def_log.append(log_insert.insert(log_file, summary_cli, True))

            else:
                summary_cli = daddy_api_json_file + " not configured properly, you are using the example data."
                def_log.append(log_insert.insert(log_file, summary_cli, True))

    # EOL
    summary_cli = "================= DONE =================\n"
    def_log.append(log_insert.insert(log_file, summary_cli, True))

    return def_log