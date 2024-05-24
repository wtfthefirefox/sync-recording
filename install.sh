#! /bin/sh
sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh)
sudo apt update && sudo apt install python3-pip
pip3 install -r requirements.txt
