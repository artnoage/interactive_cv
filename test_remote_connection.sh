#!/bin/bash

# Test script for chronicle remote sync setup

echo "Testing Chronicle Remote Sync Setup"
echo "=================================="

# Test Tailscale connection
echo -n "1. Testing Tailscale connection to portfolio-ts54... "
if ping -c 1 -W 2 portfolio-ts54 &> /dev/null; then
    echo "✓ Connected"
else
    echo "✗ Failed - Check Tailscale is running"
    exit 1
fi

# Test SSH connection
echo -n "2. Testing SSH connection... "
if ssh -o BatchMode=yes -o ConnectTimeout=5 portfolio-ts54 "exit" 2>/dev/null; then
    echo "✓ SSH key authentication working"
else
    echo "✗ Failed - Run: ssh-copy-id portfolio-ts54"
    exit 1
fi

# Test remote directory creation
echo -n "3. Creating remote chronicle directory... "
if ssh portfolio-ts54 "mkdir -p ~/chronicle && echo 'done'" &> /dev/null; then
    echo "✓ Directory created"
else
    echo "✗ Failed to create directory"
    exit 1
fi

# Test rsync
echo -n "4. Testing rsync... "
if rsync --dry-run -av ~/.bashrc portfolio-ts54:~/test_rsync_delete_me &> /dev/null; then
    echo "✓ Rsync works"
    ssh portfolio-ts54 "rm -f ~/test_rsync_delete_me" 2>/dev/null
else
    echo "✗ Rsync failed"
    exit 1
fi

echo ""
echo "✅ All tests passed! You can now run:"
echo "   ./sync_chronicle_with_remote.sh"