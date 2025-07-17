#!/usr/bin/env python3
"""
Test script to investigate filter issue in ESAK calculator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../spekpy_release'))

from esak_calculator import ESAKCalculator
import numpy as np

def test_filter_changes():
    """Test that filter changes actually affect spectrum and dose"""
    
    print("=" * 60)
    print("Testing Filter Changes Impact on Spectrum and Dose")
    print("=" * 60)
    
    # Common parameters
    kvp = 120
    ma = 100
    time_s = 0.1
    
    # Test 1: No filtration
    print("\n1. Testing with no filtration:")
    calc1 = ESAKCalculator()
    calc1.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    
    # Generate spectrum without filters
    if calc1.generate_spectrum():
        energy1, fluence1 = calc1.get_spectrum_data()
        results1 = calc1.calculate_all_metrics()
        print(f"   ESAK: {results1.get('esak_mgy', 0):.3f} mGy")
        print(f"   HVL1 (Al): {results1.get('hvl1_al_mm', 0):.2f} mm")
        print(f"   Mean Energy: {results1.get('mean_energy_kev', 0):.1f} keV")
        print(f"   Total Fluence: {results1.get('total_fluence', 0):.2e} cm⁻²")
    
    # Test 2: Al 2.5mm filtration
    print("\n2. Testing with Al 2.5mm filtration:")
    calc2 = ESAKCalculator()
    calc2.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    calc2.add_filtration('Al', 2.5)
    
    if calc2.generate_spectrum():
        energy2, fluence2 = calc2.get_spectrum_data()
        results2 = calc2.calculate_all_metrics()
        print(f"   ESAK: {results2.get('esak_mgy', 0):.3f} mGy")
        print(f"   HVL1 (Al): {results2.get('hvl1_al_mm', 0):.2f} mm")
        print(f"   Mean Energy: {results2.get('mean_energy_kev', 0):.1f} keV")
        print(f"   Total Fluence: {results2.get('total_fluence', 0):.2e} cm⁻²")
    
    # Test 3: Al 5.0mm filtration
    print("\n3. Testing with Al 5.0mm filtration:")
    calc3 = ESAKCalculator()
    calc3.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    calc3.add_filtration('Al', 5.0)
    
    if calc3.generate_spectrum():
        energy3, fluence3 = calc3.get_spectrum_data()
        results3 = calc3.calculate_all_metrics()
        print(f"   ESAK: {results3.get('esak_mgy', 0):.3f} mGy")
        print(f"   HVL1 (Al): {results3.get('hvl1_al_mm', 0):.2f} mm")
        print(f"   Mean Energy: {results3.get('mean_energy_kev', 0):.1f} keV")
        print(f"   Total Fluence: {results3.get('total_fluence', 0):.2e} cm⁻²")
    
    # Test 4: Al 2.5mm + Cu 0.5mm filtration
    print("\n4. Testing with Al 2.5mm + Cu 0.5mm filtration:")
    calc4 = ESAKCalculator()
    calc4.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    calc4.add_filtration('Al', 2.5)
    calc4.add_filtration('Cu', 0.5)
    
    if calc4.generate_spectrum():
        energy4, fluence4 = calc4.get_spectrum_data()
        results4 = calc4.calculate_all_metrics()
        print(f"   ESAK: {results4.get('esak_mgy', 0):.3f} mGy")
        print(f"   HVL1 (Al): {results4.get('hvl1_al_mm', 0):.2f} mm")
        print(f"   Mean Energy: {results4.get('mean_energy_kev', 0):.1f} keV")
        print(f"   Total Fluence: {results4.get('total_fluence', 0):.2e} cm⁻²")
    
    # Analysis
    print("\n" + "=" * 60)
    print("Analysis:")
    print("=" * 60)
    
    if len(energy1) > 0 and len(energy2) > 0 and len(energy3) > 0:
        print(f"1→2 ESAK change: {results1.get('esak_mgy', 0):.3f} → {results2.get('esak_mgy', 0):.3f} mGy")
        print(f"1→2 HVL change: {results1.get('hvl1_al_mm', 0):.2f} → {results2.get('hvl1_al_mm', 0):.2f} mm")
        print(f"2→3 ESAK change: {results2.get('esak_mgy', 0):.3f} → {results3.get('esak_mgy', 0):.3f} mGy")
        print(f"2→3 HVL change: {results2.get('hvl1_al_mm', 0):.2f} → {results3.get('hvl1_al_mm', 0):.2f} mm")
        print(f"3→4 ESAK change: {results3.get('esak_mgy', 0):.3f} → {results4.get('esak_mgy', 0):.3f} mGy")
        print(f"3→4 HVL change: {results3.get('hvl1_al_mm', 0):.2f} → {results4.get('hvl1_al_mm', 0):.2f} mm")
        
        # Check if filters are actually working
        esak_decreasing = (results1.get('esak_mgy', 0) > results2.get('esak_mgy', 0) > results3.get('esak_mgy', 0) > results4.get('esak_mgy', 0))
        hvl_increasing = (results1.get('hvl1_al_mm', 0) < results2.get('hvl1_al_mm', 0) < results3.get('hvl1_al_mm', 0) < results4.get('hvl1_al_mm', 0))
        
        print(f"\nFilter effects are correct: ESAK decreasing={esak_decreasing}, HVL increasing={hvl_increasing}")
        
        if not esak_decreasing:
            print("❌ WARNING: ESAK should decrease with more filtration!")
        if not hvl_increasing:
            print("❌ WARNING: HVL should increase with more filtration!")
    else:
        print("❌ ERROR: Failed to generate spectrum data")

def test_parameter_persistence():
    """Test that parameter changes persist correctly"""
    
    print("\n" + "=" * 60)
    print("Testing Parameter Persistence")
    print("=" * 60)
    
    calc = ESAKCalculator()
    calc.set_clinical_parameters(kvp=120, ma=100, time_s=0.1)
    
    # Test adding filters one by one
    print("\n1. Adding first filter (Al 2.5mm):")
    calc.add_filtration('Al', 2.5)
    print(f"   Filters: {calc.parameters.get('filters', [])}")
    
    print("\n2. Adding second filter (Cu 0.5mm):")
    calc.add_filtration('Cu', 0.5)
    print(f"   Filters: {calc.parameters.get('filters', [])}")
    
    print("\n3. Generating spectrum:")
    if calc.generate_spectrum():
        print("   ✅ Spectrum generated successfully")
        results = calc.calculate_all_metrics()
        print(f"   ESAK: {results.get('esak_mgy', 0):.3f} mGy")
        print(f"   HVL1 (Al): {results.get('hvl1_al_mm', 0):.2f} mm")
    else:
        print("   ❌ Failed to generate spectrum")

def main():
    """Run all tests"""
    try:
        test_filter_changes()
        test_parameter_persistence()
        
        print("\n" + "=" * 60)
        print("Test completed. Check results above for filter effectiveness.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()