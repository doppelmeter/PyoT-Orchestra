#!/bin/bash

# Add script as cronjob @reboot

# Update from GitHub
cd ~/PyoT-Orchestra/
git pull --progress https://github.com/doppelmeter/PyoT-Orchestra.git &> ../git_log.txt

# Start Client Software
python3 ~/PyoT-Orchestra/client/utils/scripts/show_ip_on_sensehat.py
python3 ~/PyoT-Orchestra/client/utils/scripts/show_sample_text_on_sensehat.py
python3 ~/PyoT-Orchestra/client/musician_pi.py
