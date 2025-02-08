#!/bin/bash

# Source file location (assumed to be in the same directory as this script)
WPA_SUPPLICANT_SRC="./wpa_supplicant.conf"

# Destination path
WPA_SUPPLICANT_DEST="/etc/wpa_supplicant/wpa_supplicant.conf"

# Ensure script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo ./setup_wifi.sh)"
    exit 1
fi

# Check if the source file exists
if [ ! -f "$WPA_SUPPLICANT_SRC" ]; then
    echo "Error: wpa_supplicant.conf not found in the current directory!"
    exit 1
fi

# Copy wpa_supplicant.conf to the correct location
echo "Copying wpa_supplicant.conf to $WPA_SUPPLICANT_DEST..."
cp "$WPA_SUPPLICANT_SRC" "$WPA_SUPPLICANT_DEST"

# Set correct permissions
echo "Setting correct file permissions..."
chmod 600 "$WPA_SUPPLICANT_DEST"
chown root:root "$WPA_SUPPLICANT_DEST"

# Restart networking services
echo "Restarting networking services..."
systemctl restart networking
systemctl restart wpa_supplicant

echo "✅ Wi-Fi configuration updated successfully!"
exit 0
