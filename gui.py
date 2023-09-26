#!/usr/bin/env python3

import tkinter as tk
from tkinter import font
import json
import funct.log_insert as log_insert
import funct.json_read as json_read
import skeleton
import os

file_path = os.path.dirname(__file__) + "/"

json_file = file_path + "daddy_api.json"
log_file = file_path + "log.txt"

summary_cli = "GUI started"
log_insert.insert(log_file, summary_cli, False)

def config_run():
    bot_run_button.pack()
    result_label.pack(pady=10)

def save_data_to_json():
    summary_cli = "save_button pressed"
    log_insert.insert(log_file, summary_cli, False)
    data_gui = [domain_entry.get(), type_entry.get(), name_entry.get(), api_key_entry.get(), api_secret_entry.get()]
    data = [
        {
            "domain": data_gui[0],
            "type": data_gui[0],
            "name": data_gui[0],
            "api_key": data_gui[0],
            "api_secret": data_gui[0]
        }
    ]

    json_input_gui_delete()

    isThereEmpty = False
    for line in data_gui:
        if line == "":
            isThereEmpty = True
            summary_cli = "Empty data found in " + json_file
            log_insert.insert(log_file, summary_cli, False)

    if json_file and isThereEmpty == False: # and empty_value_bool == False:
        with open(json_file, "w") as file:
            json.dump(data, file)
        summary_cli = "Data saved to " + json_file
        result_label.config(text=summary_cli, fg="Green")
        result_label.pack(pady=10)
        config_run()
    else:
        summary_cli = "An error occurred."
        result_label.config(text=summary_cli, fg="red")
        result_label.pack(pady=10)
    
    log_insert.insert(log_file, summary_cli, False)

def run_bot():
    def_log = skeleton.run()
    create_text_boxes(def_log)

def json_input_gui_delete():
    domain_label.pack_forget()
    domain_entry.pack_forget()
    type_entry.pack_forget()
    type_label.pack_forget()
    name_entry.pack_forget()
    name_label.pack_forget()
    api_key_entry.pack_forget()
    api_key_label.pack_forget()
    api_secret_entry.pack_forget()
    api_secret_label.pack_forget()
    save_button.pack_forget()

def create_text_boxes(list):
    num_boxes = len(list)

    # Remove existing text entry widgets
    widget_not_to_destroy = [bot_run_button]
    print(root.winfo_children())
    for widget in root.winfo_children():
        if widget != bot_run_button:
            widget.pack_forget()
    # Create new text entry widgets
    for line in list:
        cli_result = tk.Label(root, text= line, anchor="w", justify="left", padx=1, pady=1, width=80)
        cli_result.pack()

# Create the main window
root = tk.Tk()
root.minsize(800, 400)
root.title("DadDynDNS")

bold_font = font.Font(weight="bold")

# Create input fields for data collection
domain_label = tk.Label(root, width=30, text="Domain:", font=bold_font, anchor="w", justify="left")
domain_label.pack()
domain_entry = tk.Entry(root, width=30)
domain_entry.pack()

type_label = tk.Label(root, width=30, text="Type:", font=bold_font, anchor="w", justify="left")
type_label.pack()
type_entry = tk.Entry(root, width=30)
type_entry.pack()

name_label = tk.Label(root, width=30, text="Name:", font=bold_font, anchor="w", justify="left")
name_label.pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

api_key_label = tk.Label(root, width=30, text="API Key:", font=bold_font, anchor="w", justify="left")
api_key_label.pack()
api_key_entry = tk.Entry(root, width=30)
api_key_entry.pack()

api_secret_label = tk.Label(root, width=30, text="API Secret:", font=bold_font, anchor="w", justify="left")
api_secret_label.pack()
api_secret_entry = tk.Entry(root, width=30)
api_secret_entry.pack()

# Create a button to save data to a JSON file
save_button = tk.Button(root, text="Save", command= lambda : save_data_to_json(), font=bold_font)
save_button.pack()

# Create a label to display the result
result_label = tk.Label(root, text="", fg="black")

bot_run_button = tk.Button(root, text="Run the bot", font=bold_font, command= lambda: run_bot())

if os.path.exists(json_file):
    json_input_gui_delete()
    config_run()
    summary_cli = json_file + " found"
    result_label.config(text= summary_cli, fg="green")
    log_insert.insert(log_file, summary_cli, False)

root.mainloop()
