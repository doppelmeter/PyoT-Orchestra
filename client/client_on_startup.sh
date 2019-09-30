#!/bin/bash

# Save all shell and python scripts in ~/script/client
# Add script as cronjob @reboot

# Update from GitHub
git pull https://github.com/doppelmeter/PyoT-Orchestra

# Start Client Software
python3 ~/PyoT-Orchestra/client/show_ip_on_sensehat.py
python3 ~/PyoT-Orchestra/client/show_sample_text_on_sensehat.py
