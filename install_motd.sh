#!/bin/bash

# Variables
SCRIPT_NAME="billboard_motd.py"
INSTALL_DIR="/usr/local/bin"
MOTD_SCRIPT="$INSTALL_DIR/$SCRIPT_NAME"
MOTD_DYNAMIC="/etc/update-motd.d/10-billboard"

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Step 1: Copy the Python script to /usr/local/bin
echo "Installing $SCRIPT_NAME to $INSTALL_DIR..."
cp "$SCRIPT_NAME" "$MOTD_SCRIPT"
chmod +x "$MOTD_SCRIPT"

# Step 2: Create an update-motd.d script to call the Python script
echo "Configuring MOTD..."
cat <<EOL > "$MOTD_DYNAMIC"
#!/bin/bash
# Dynamic MOTD script to display the Billboard Top 10
/usr/bin/env python3 "$MOTD_SCRIPT"
EOL

chmod +x "$MOTD_DYNAMIC"

# Step 3: Clean up old static MOTD (optional)
echo "Cleaning up old MOTD..."
rm -f /etc/motd
ln -sf /var/run/motd /etc/motd

# Step 4: Reload MOTD
echo "Updating MOTD..."
run-parts /etc/update-motd.d/ > /var/run/motd

echo "Installation complete! Log in to your terminal to see the MOTD."


'''
Steps to Use the Install Script
Save the install script as install_motd.sh.
Place your Python script (billboard_motd.py) in the same directory as the install script.
Run the following commands to install:
chmod +x install_motd.sh
sudo ./install_motd.sh
'''