#!/bin/bash

# Copy the service file to systemd directory
sudo cp alte-service.service /etc/systemd/system/

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable alte-service.service

# Start the service immediately
sudo systemctl start alte-service.service

# Check the status of the service
sudo systemctl status alte-service.service