#!/bin/bash
ln -s /root/Air-Monitoring-HAT/air-quality-monitor.service /etc/systemd/system/air-quality-monitor.service

systemctl daemon-reload
systemctl enable air-quality-monitor.service
systemctl restart air-quality-monitor.service