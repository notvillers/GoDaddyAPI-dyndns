import datetime
import os

def insert(path, text):
    print(text)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(path):
        with open(path, 'w') as file: 
            file.write(current_time + ": " + path + " created \n")
    with open(path, 'a') as file: 
        file.write(current_time + ": " + text + "\n")