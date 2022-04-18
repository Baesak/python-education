#! /usr/bin/env bash

date +"%d/%m/%y - %H:%M:%S" >> /home/$(whoami)/date.txt


# crontab: 
# 0 */1 * * * /home/bogdan/scripts/date.sh
