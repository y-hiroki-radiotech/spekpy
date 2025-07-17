"""
Simple test script to verify basic functionality without external dependencies.
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Test that all modules can be imported."""
    print("Testing basic imports...")
    
    try:
        import esak_calculator
        print("✅ esak_calculator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import esak_calculator: {e}")
        return False
    
    try:
        import data_export
        print("✅ data_export imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import data_export: {e}")
        return False
    
    try:
        import visualization
        print("✅ visualization imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import visualization: {e}")
        return False
    
    return True

def test_esak_calculator_basic():
    """Test basic ESAKCalculator functionality."""
    print("\nTesting ESAKCalculator basic functionality...")
    
    try:
        from esak_calculator import ESAKCalculator
        
        # Initialize calculator
        calculator = ESAKCalculator()
        print("✅ Calculator initialized")
        
        # Set parameters
        calculator.set_clinical_parameters(
            kvp=120,
            ma=100,
            time_s=0.1,
            anode_angle=12.0,
            ssd_cm=100
        )
        print("✅ Parameters set successfully")
        
        # Check parameters
        assert calculator.parameters['kvp'] == 120
        assert calculator.parameters['mas'] == 10.0
        print("✅ Parameter validation passed")
        
        # Add filtration
        calculator.add_filtration('Al', 2.5)
        assert len(calculator.parameters['filters']) == 1
        print("✅ Filtration added successfully")
        
        # Test summary generation
        summary = calculator.get_summary_text()
        assert len(summary) > 100  # Should be a substantial text
        print("✅ Summary text generated")
        
        return True
        
    except Exception as e:
        print(f"❌ ESAKCalculator test failed: {e}")
        return False

def test_file_structure():
    """Test file structure."""
    print("\nTesting file structure...")
    
    required_files = [
        'esak_calculator.py',
        'data_export.py',
        'visualization.py',
        'app.py'
    ]
    
    for filename in required_files:
        if Path(filename).exists():
            print(f"✅ {filename} exists")
        else:
            print(f"❌ {filename} missing")
            return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    print("\nTesting basic functionality...")
    
    try:
        # Test JSON operations
        import json
        test_data = {"test": "value", "number": 42}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        assert parsed == test_data
        print("✅ JSON operations working")
        
        # Test date operations
        from datetime import datetime
        now = datetime.now()
        timestamp = now.isoformat()
        assert len(timestamp) > 10
        print("✅ DateTime operations working")
        
        # Test pathlib
        from pathlib import Path
        current_path = Path('.')
        assert current_path.exists()
        print("✅ Path operations working")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("=" * 60)
    print("CLINICAL X-RAY DOSIMETRY CALCULATOR - BASIC TESTS")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Basic Imports", test_basic_imports),
        ("Basic Functionality", test_basic_functionality),
        ("ESAKCalculator Basic", test_esak_calculator_basic),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: uv add spekpy streamlit matplotlib pandas numpy")
        print("2. Run the Streamlit app: streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)