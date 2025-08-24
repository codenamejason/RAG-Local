#!/bin/bash
# Make all shell scripts executable
# Run this on Mac/Linux to set proper permissions

echo "Setting executable permissions on all shell scripts..."

# Make all .sh files executable
chmod +x *.sh

# List the scripts
echo ""
echo "The following scripts are now executable:"
ls -la *.sh

echo ""
echo "You can now run any script with: ./script_name.sh"
