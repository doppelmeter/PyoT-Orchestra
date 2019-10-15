#!/bin/bash

# install pip packages
pip3 install paho-mqtt
pip3 install sense-hat

# clone repository
cd ~
git clone https://github.com/doppelmeter/PyoT-Orchestra

# start scripts
bash helpers/musician_startup.sh
