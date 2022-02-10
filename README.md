# vimeo_channel_update_checker
python app checking for update on a vimeo channel

## script to install on the remote server looking for vimeo changes
run :<br>
<code>sh install.sh</code>

## Docker commands 
if you plan to run it into a docker (for example alpine + python docker),to get the outputs of the python script you can add the following to your run command : <br>
<code>docker run --name <docker_name> -a stdin -a stdout -a stderr cron</code> 
to ssh into the docker et git pull the repo :
<code>ssh root@MachineB 'bash -s' < local_script.sh</code>
Avec local_script.sh :
<code>
#!/bin/sh
mkdir -p vimeo_channel_update_checker && cd cd vimeo_channel_update_checker

# kill all node processes
pkill -f node

# update repo
git pull remote origin https://github.com/goulchen/vimeo_channel_update_checker.git

# install if necessary python3 and add cron job if not already
sh install.sh
</code>