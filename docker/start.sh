#!/bin/bash


# linha cron para artisan schedule
/bin/echo "0 0 * * * /usr/local/bin/python /usr/src/app/flowyt/cli.py -w servicenow -f chain -d true >> /dev/stdout 2>&1" >/tmp/jobs.cron
/bin/echo "0 1 * * * /usr/local/bin/python /usr/src/app/flowyt/cli.py -w sapi -f vulnerabilities -d true >> /dev/stdout 2>&1" >>/tmp/jobs.cron
/bin/echo "0 2 * * * /usr/local/bin/python /usr/src/app/flowyt/cli.py -w massification -f chain -d true >> /dev/stdout 2>&1" >>/tmp/jobs.cron

#inicia cron e adiciona script scheduler laravel
cron
crontab /tmp/jobs.cron

# .env Build
/bin/bash ./docker/varsenv.sh

service cron start

bash
