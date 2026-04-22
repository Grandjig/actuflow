#!/bin/sh

# Replace port in nginx config if PORT env var is set (Railway requirement)
if [ -n "$PORT" ]; then
    sed -i "s/listen 80;/listen $PORT;/g" /etc/nginx/conf.d/default.conf
    sed -i "s/listen \[::\]:80;/listen [::]:$PORT;/g" /etc/nginx/conf.d/default.conf
fi

exec "$@"
