#!/bin/bash
config="userbot.cfg"
echo ""
echo "Enter API_ID and API_HASH"
echo "You can get it here: https://my.telegram.org/apps"
echo ""
read -r -p "Enter your API_ID: " api_id
read -r -p "Enter your API_HASH: " api_hash
echo ""
sed -i "s/^api_id\s*=\s*.*/api_id = $api_id/" $config
sed -i "s/^api_hash\s*=\s*.*/api_hash = $api_hash/" $config
