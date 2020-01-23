#!/bin/bash

# To install the latest stable release:
# sudo apt-get install -y apt-transport-https
# sudo apt-get install -y software-properties-common wget
# wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
# sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
# sudo apt-get update
# sudo apt-get install grafana

#get updates
echo -e "${Colour}Checking for updates \n\n${Color_Off}"
sudo apt-get update
sudo apt-get upgrade

#install Grafana
echo -e "${Colour}Installing Grafana \n${Color_Off}"
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_6.5.3_amd64.deb -O grafana_6.5.3_amd64.deb
sudo dpkg -i grafana_6.5.3_amd64.deb
rm grafana_6.5.3_amd64.deb

#install Grafana plugins
echo -e "${Colour}Installing Grafana plugins \n${Color_Off}"

sudo grafana-cli plugins install alexanderzobnin-zabbix-app
sudo grafana-cli plugins install grafana-worldmap-panel

# Restart the server for the plugins
sudo service grafana-server restart

# Install Grafana Python API
pip install grafana-api
pip install lxml
# Download Python script for updating grafana

# /JUMPING-JIVE-Geodetic-Observatory-Wettzell/data/scripts/install_grafana.sh
# https://raw.githubusercontent.com/IslamAlam/JUMPING-JIVE-Geodetic-Observatory-Wettzell/master/data/scripts/install_grafana.sh

# wget "https://raw.githubusercontent.com/IslamAlam/JUMPING-JIVE-Geodetic-Observatory-Wettzell/master/data/scripts/install_grafana.sh" -O install_grafana.sh && chmod +x install_grafana.sh && ./install_grafana.sh

wget "https://raw.githubusercontent.com/IslamAlam/JUMPING-JIVE-Geodetic-Observatory-Wettzell/master/data/scripts/update_grafana.py" -O update_grafana.py && python update_grafana.py

