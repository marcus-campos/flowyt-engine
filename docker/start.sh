#!/bin/bash


# linha cron para artisan schedule
/bin/echo "0 0 * * * /usr/local/bin/python /usr/src/app/flowyt/cli.py -w servicenow -f contracts -d true > /tmp/debug.log 2>&1" >/tmp/jobs.cron

#inicia cron e adiciona script scheduler laravel
cron
crontab /tmp/jobs.cron

# .env Build
/bin/bash ./docker/varsenv.sh

service cron start

bash
