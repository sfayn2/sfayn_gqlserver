#!/bin/bash

# --- CONFIGURATION ---
KC_URL="http://localhost:8080"
REALM="TenantOMSAPI-Realm"
USR="pao"
PWD="${KC_PWD}"
CLIENT_ID="TenantOMSAPI-Client"
CLIENT_SECRET="${KC_CLIENT_SECRET}"

# Get from OS env, or exit if not set
if [ -z "$CLIENT_SECRET" ]; then
    echo "❌ Error: KC_CLIENT_SECRET environment variable is not set."
    exit 1
fi

if [ -z "$PWD" ]; then
    echo "❌ Error: KC_PWD environment variable is not set."
    exit 1
fi

echo "--- 1. Fetching Access Token ---"
RESPONSE=$(curl -s -X POST "$KC_URL/realms/$REALM/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "username=$USR" \
  --data-urlencode "password=$PWD" \
  --data-urlencode "scope=openid" \
  --data-urlencode "grant_type=password")

TKN=$(echo $RESPONSE | jq -r '.access_token')

if [ "$TKN" == "null" ] || [ -z "$TKN" ]; then
    echo "❌ Error: Could not get token."
    echo "$RESPONSE" | jq .
    exit 1
fi

echo "✅ Token acquired."
echo $TKN
echo ""
echo ""

echo "--- 2. Decoded Token Payload (Full JSON) ---"
# Decodes and prints the raw JSON structure of the JWT payload
echo $TKN | cut -d'.' -f2 | base64 --decode 2>/dev/null | jq .
echo ""

echo "--- 3. Live UserInfo (Full JSON) ---"
# Fetches data from the OIDC UserInfo endpoint
curl -s -X GET "$KC_URL/realms/$REALM/protocol/openid-connect/userinfo" \
  -H "Authorization: Bearer $TKN" | jq .
echo ""

echo "--- 4. Accessible Organizations ---"
# Lists organizations the user has permission to view
curl -s -X GET "$KC_URL/admin/realms/$REALM/organizations" \
  -H "Authorization: Bearer $TKN" \
  -H "Accept: application/json" | jq .

