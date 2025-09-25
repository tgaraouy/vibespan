#!/usr/bin/env python3
"""Test WHOOP redirect URI"""

from dotenv import load_dotenv
import os
import sys
sys.path.append('.')

load_dotenv('.env')

from whoop_integration import get_whoop_integration

whoop = get_whoop_integration('tgaraouy')

base_url = os.getenv('BASE_URL', 'https://vibespan.ai')
redirect_uri = f"{base_url}/auth/whoop/callback"

print(f"Base URL: {base_url}")
print(f"Redirect URI: {redirect_uri}")
print(f"Client ID: {whoop.client_id}")
print(f"Auth URL: {whoop.get_authorization_url()[:200]}...")
