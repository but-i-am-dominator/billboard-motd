#!/bin/bash

# Variables
SCRIPT_NAME="billboard_motd.py"
INSTALL_DIR="/usr/local/bin"
MOTD_SCRIPT="$INSTALL_DIR/$SCRIPT_NAME"
MOTD_DYNAMIC="/etc/update-motd.d/10-billboard"
REQ_FILE="requirements.txt"

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Step 1: Ensure Python3 and pip are installed
echo "Checking for Python3 and pip..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it and rerun the script."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing it now..."
    apt update && apt install -y python3-pip
fi

# Step 2: Install dependencies from requirements.txt
if [[ -f "$REQ_FILE" ]]; then
    echo "Installing dependencies from $REQ_FILE..."
    pip3 install -r "$REQ_FILE"
else
    echo "Warning: $REQ_FILE not found. Skipping dependency installation."
fi

# Step 3: Copy the Python script to /usr/local/bin
echo "Installing $SCRIPT_NAME to $INSTALL_DIR..."
cp "$SCRIPT_NAME" "$MOTD_SCRIPT"
chmod +x "$MOTD_SCRIPT"

# Step 4: Create an update-motd.d script to call the Python script
echo "Configuring MOTD..."
cat <<EOL > "$MOTD_DYNAMIC"
#!/bin/bash
# Dynamic MOTD script to display the Billboard Top 10
/usr/bin/env python3 "$MOTD_SCRIPT"
EOL

chmod +x "$MOTD_DYNAMIC"

# Step 5: Clean up old static MOTD (optional)
echo "Cleaning up old MOTD..."
rm -f /etc/motd
ln -sf /var/run/motd /etc/motd

# Step 6: Reload MOTD
echo "Updating MOTD..."
run-parts /etc/update-motd.d/ > /var/run/motd

echo "Installation complete! Log in to your terminal to see the MOTD."
