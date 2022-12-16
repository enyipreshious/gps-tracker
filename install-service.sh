#!/bin/bash

# Requires root access

chmod 777 /etc/systemd/system

echo -e "[Unit]
Description=GPS Tracker

[Service]
Type=simple
ExecStart=/bin/bash -c \"cd ~/.projects && source .venv/bin/activate && python3 main.py\"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/gps-tracker.service

systemctl enable gps-tracker
systemctl start gps-tracker

chmod 751 /etc/systemd/system
