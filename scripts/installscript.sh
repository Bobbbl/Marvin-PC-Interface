#!/bin/bash
wget -q --spider http://google.com

if [ $? -eq 0 ]
then echo "Internetconnection OK..."
else echo "Internet Connection Down...Fail"; return
fi




sudo apt-get update
sudo apt-get upgrade
sudo apt install python3
sudo apt install python3-pip
pip3 install pandas
pip3 install scipy
pip3 install pyserial
pip3 install pyinstaller
pip3 install PyQt5

pyinstaller ../main.py
