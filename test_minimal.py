#!/usr/bin/env python3
"""
Test the minimal Vibespan.ai version
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_minimal_app():
    """Test the minimal app"""
    print("🧪 Testing Minimal Vibespan.ai App")
    print("=" * 40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from fastapi import FastAPI
        print("✅ FastAPI import successful")
        
        # Test app creation
        print("2. Testing app creation...")
        app = FastAPI(title="Test App")
        print("✅ App creation successful")
        
        # Test route creation
        print("3. Testing route creation...")
        @app.get("/")
        async def root():
            return {"message": "test"}
        print("✅ Route creation successful")
        
        # Test main.py import
        print("4. Testing main.py import...")
        import main
        print("✅ main.py import successful")
        
        # Test app access
        print("5. Testing app access...")
        if hasattr(main, 'app'):
            print("✅ App accessible from main.py")
        else:
            print("❌ App not found in main.py")
            return False
        
        print("\n🎉 All tests passed! Ready for Vercel deployment.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_minimal_app()
    sys.exit(0 if success else 1)
