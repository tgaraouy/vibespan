#!/usr/bin/env python3
"""
Build Test for Vibespan.ai
Tests all necessary libraries and dependencies for deployment.
"""

import sys
import importlib
import traceback
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name, package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name}: {e}")
        return False

def test_core_dependencies():
    """Test core framework dependencies"""
    print("🧪 Testing Core Framework Dependencies")
    print("=" * 50)
    
    core_modules = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "python_dotenv",
        "requests"
    ]
    
    results = []
    for module in core_modules:
        results.append(test_import(module))
    
    return all(results)

def test_data_processing():
    """Test data processing dependencies"""
    print("\n📊 Testing Data Processing Dependencies")
    print("=" * 50)
    
    data_modules = [
        "pandas",
        "numpy"
    ]
    
    results = []
    for module in data_modules:
        results.append(test_import(module))
    
    return all(results)

def test_security():
    """Test security dependencies"""
    print("\n🔒 Testing Security Dependencies")
    print("=" * 50)
    
    security_modules = [
        "cryptography"
    ]
    
    results = []
    for module in security_modules:
        results.append(test_import(module))
    
    return all(results)

def test_llm_dependencies():
    """Test LLM dependencies (optional)"""
    print("\n🤖 Testing LLM Dependencies (Optional)")
    print("=" * 50)
    
    llm_modules = [
        "langchain",
        "langchain_openai",
        "langchain_anthropic", 
        "langchain_core"
    ]
    
    results = []
    for module in llm_modules:
        results.append(test_import(module))
    
    return all(results)

def test_application_modules():
    """Test our application modules"""
    print("\n🏥 Testing Application Modules")
    print("=" * 50)
    
    # Add src to path
    sys.path.append(str(Path(__file__).parent / "src"))
    
    app_modules = [
        ("src.auth.tenant_manager", "tenant_manager"),
        ("src.agents.core_agents", "BaseAgent"),
        ("src.agents.agent_orchestrator", "AgentOrchestrator"),
        ("src.data.data_importer", "data_importer"),
        ("src.data.realtime_ingestion", "RealTimeIngestion"),
        ("src.middleware.subdomain_middleware", "SubdomainMiddleware")
    ]
    
    results = []
    for module_path, class_name in app_modules:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, class_name):
                print(f"✅ {module_path}.{class_name}")
                results.append(True)
            else:
                print(f"❌ {module_path}.{class_name}: Class not found")
                results.append(False)
        except Exception as e:
            print(f"❌ {module_path}: {e}")
            results.append(False)
    
    return all(results)

def test_fastapi_app():
    """Test FastAPI application creation"""
    print("\n🚀 Testing FastAPI Application")
    print("=" * 50)
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Test basic app creation
        app = FastAPI(title="Test App")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        print("✅ FastAPI app creation")
        print("✅ CORS middleware")
        
        # Test route creation
        @app.get("/")
        async def root():
            return {"message": "test"}
        
        print("✅ Route creation")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        traceback.print_exc()
        return False

def test_vercel_compatibility():
    """Test Vercel-specific compatibility"""
    print("\n🌐 Testing Vercel Compatibility")
    print("=" * 50)
    
    try:
        # Test if we can import main module
        import main
        print("✅ main.py importable")
        
        # Test if app is accessible
        if hasattr(main, 'app'):
            print("✅ FastAPI app accessible")
        else:
            print("❌ FastAPI app not found in main.py")
            return False
        
        # Test environment variables
        import os
        print(f"✅ Environment variables accessible: {len(os.environ)} vars")
        
        return True
        
    except Exception as e:
        print(f"❌ Vercel compatibility test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all build tests"""
    print("🏗️  Vibespan.ai Build Test")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    # Run all tests
    tests = [
        ("Core Dependencies", test_core_dependencies),
        ("Data Processing", test_data_processing), 
        ("Security", test_security),
        ("LLM Dependencies", test_llm_dependencies),
        ("Application Modules", test_application_modules),
        ("FastAPI Application", test_fastapi_app),
        ("Vercel Compatibility", test_vercel_compatibility)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 BUILD TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment!")
        return True
    else:
        print("⚠️  Some tests failed. Check dependencies before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
