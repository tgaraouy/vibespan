#!/usr/bin/env python3
"""
Setup localhost subdomain for Vibespan.ai development
Adds tgaraouy.localhost to your system's hosts file.
"""

import os
import sys
import subprocess
from pathlib import Path

def add_localhost_subdomain():
    """Add tgaraouy.localhost to hosts file"""
    
    print("🔧 Setting up localhost subdomain for Vibespan.ai")
    print("=" * 50)
    
    # Define the hosts entry
    hosts_entry = "127.0.0.1 tgaraouy.localhost"
    hosts_file = None
    
    # Determine hosts file location based on OS
    if os.name == 'nt':  # Windows
        hosts_file = Path("C:/Windows/System32/drivers/etc/hosts")
    else:  # Unix-like systems
        hosts_file = Path("/etc/hosts")
    
    print(f"📁 Hosts file location: {hosts_file}")
    
    # Check if entry already exists
    try:
        with open(hosts_file, 'r') as f:
            content = f.read()
        
        if "tgaraouy.localhost" in content:
            print("✅ tgaraouy.localhost already exists in hosts file")
            return True
    except Exception as e:
        print(f"⚠️ Could not read hosts file: {e}")
        print("   You may need to run this script as administrator")
        return False
    
    # Add the entry
    try:
        with open(hosts_file, 'a') as f:
            f.write(f"\n{hosts_entry}\n")
        
        print(f"✅ Added {hosts_entry} to hosts file")
        print("   You can now access: http://tgaraouy.localhost:8000")
        return True
        
    except PermissionError:
        print("❌ Permission denied - you need to run this as administrator")
        print("   Please run: python setup_localhost.py as administrator")
        return False
    except Exception as e:
        print(f"❌ Error adding to hosts file: {e}")
        return False

def test_subdomain():
    """Test if the subdomain is working"""
    print("\n🧪 Testing subdomain...")
    
    try:
        import requests
        response = requests.get("http://tgaraouy.localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Subdomain is working!")
            print("   You can now access your health dashboard")
            return True
        else:
            print(f"⚠️ Subdomain responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to tgaraouy.localhost:8000")
        print("   Make sure the server is running: python main.py")
        return False
    except ImportError:
        print("⚠️ requests library not available for testing")
        return False
    except Exception as e:
        print(f"❌ Error testing subdomain: {e}")
        return False

def main():
    """Main setup function"""
    
    # Add to hosts file
    success = add_localhost_subdomain()
    
    if success:
        print("\n📋 Next Steps:")
        print("1. Start the server: python main.py")
        print("2. Test onboarding: python test_localhost_onboarding.py")
        print("3. Access dashboard: http://tgaraouy.localhost:8000/dashboard")
        print("4. View API docs: http://tgaraouy.localhost:8000/docs")
        
        # Test if server is running
        test_subdomain()
    else:
        print("\n❌ Setup failed. Please run as administrator and try again.")

if __name__ == "__main__":
    main()
