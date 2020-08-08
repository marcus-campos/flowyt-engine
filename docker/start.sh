#!/bin/bash

service cron start

croncmd="/usr/local/bin/python /usr/src/app/flowyt/cli.py -w servicenow -f contracts -d true > /tmp/debug.log 2>&1"
cronjob="0 0 * * * $croncmd"
( crontab -l | grep -v -F "$croncmd" ; echo "$cronjob" ) | crontab -

bash
