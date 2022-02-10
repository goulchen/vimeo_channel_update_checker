#!/bin/sh
#### This file installs the necessary python libraries and also starts the cron job that will run the python script every minute
sudo apt-get update
installed=`python3 --version`

if test -z "$installed" 
then
      echo "installing Python"
      sudo apt-get install python3.6 && python -m ensurepip --upgrade && pip install
else
      echo "Python is installed"
fi
pip install -r requirements.txt
# get curr directory

#setup cron job 
crontab -l | { cat; echo "* * * * * $PWD/cron_script.sh >> /var/log/script.log/"; } | crontab -

