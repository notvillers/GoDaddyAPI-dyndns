#!/usr/bin/env python3
import funct.skeleton as skeleton
import os
import funct.log_insert as log_insert

file_path = os.path.dirname(__file__) + "/"

log_file = file_path + "log.txt"

summary_cly = "bot.py started"

log_insert.insert(log_file, summary_cly, True)

skeleton.run()