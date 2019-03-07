#!/bin/bash

echo "Current Operating System:"
echo  "$OSTYPE"

platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   platform='linux'
elif [[ "$unamestr" == 'FreeBSD' ]]; then
   platform='freebsd'
fi


if [[ "$OSTYPE" != "msys" ]] 
then
	wget -q --spider http://google.com
	if [ $? -eq 0 ]
	then 
		echo "Internetconnection OK..." 
		sudo apt-get update 
		sudo apt-get upgrade 
		sudo apt install python3 
		sudo apt install python3-pip &
		pip3 install pandas 
		pip3 install scipy 
		pip3 install pyserial 
		pip3 install pyinstaller 
		pip3 install PyQt5 
		pyinstaller ../main.py
	else 
		echo "Internet Connection Down...Fail" && exit
	fi
else
	echo "Do Windows Install"
	pip install -U pandas
	pip install -U pyinstaller
	pip install -U scipy
	pip install -U numpy
	pip install -U pyserial
	pip install -U py2exe
	pip install -U PyQt5
	pyinstaller main.py
fi


