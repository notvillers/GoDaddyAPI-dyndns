#!/usr/bin/env python3

import datetime
import os

# Inserts into the log.txt and writes out to the cli
def insert(log_file, summary_cli, cli):
    if cli == True:
        print(summary_cli)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    if not os.path.exists(log_file):
       
        with open(log_file, 'w') as file: 
            file.write(current_time + ": " + log_file + " created \n")
   
    with open(log_file, 'a') as file: 
        file.write(current_time + ": " + summary_cli + "\n")