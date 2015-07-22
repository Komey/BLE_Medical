#!/bin/bash

echo "Hi~~~"

/usr/bin/supervisord
exec /usr/sbin/sshd -D