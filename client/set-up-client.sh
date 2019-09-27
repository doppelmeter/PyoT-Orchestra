#!/bin/bash

sudo apt-get install subversion
mkdir ~/script
cd ~/script
svn checkout https://github.com/doppelmeter/HS2019-IoT/trunk/client
chmod u+x ~/script/client/client_on_startup.sh
