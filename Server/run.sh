#!/bin/bash

echo "Hi~~~"

python /home/docker/code/app/manage.py makemigrations

python /home/docker/code/app/manage.py migrate

/usr/bin/supervisord
exec /usr/sbin/sshd -D