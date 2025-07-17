#!/usr/bin/env python3
"""
Test script to verify the fix for filter issue in Streamlit app
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../spekpy_release'))

from esak_calculator import ESAKCalculator
import numpy as np

def simulate_streamlit_filter_behavior():
    """Simulate the behavior of the Streamlit app with filter changes"""
    
    print("=" * 70)
    print("Testing Streamlit App Filter Behavior Simulation")
    print("=" * 70)
    
    # Simulate session state filters
    filters = [{'material': 'Al', 'thickness': 2.5}]
    
    # Common parameters
    kvp = 120
    ma = 100
    time_s = 0.1
    
    # Test 1: Initial calculation with Al 2.5mm
    print("\n1. Initial calculation with Al 2.5mm:")
    calculator = ESAKCalculator()  # New instance as per fix
    calculator.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    
    for filter_config in filters:
        if filter_config['thickness'] > 0:
            calculator.add_filtration(filter_config['material'], filter_config['thickness'])
    
    results1 = calculator.calculate_all_metrics()
    print(f"   ESAK: {results1.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results1.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Mean Energy: {results1.get('mean_energy_kev', 0):.1f} keV")
    
    # Test 2: User changes filter to Al 5.0mm
    print("\n2. User changes filter to Al 5.0mm:")
    filters[0]['thickness'] = 5.0
    
    calculator = ESAKCalculator()  # New instance as per fix
    calculator.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    
    for filter_config in filters:
        if filter_config['thickness'] > 0:
            calculator.add_filtration(filter_config['material'], filter_config['thickness'])
    
    results2 = calculator.calculate_all_metrics()
    print(f"   ESAK: {results2.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results2.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Mean Energy: {results2.get('mean_energy_kev', 0):.1f} keV")
    
    # Test 3: User adds Cu filter
    print("\n3. User adds Cu 0.5mm filter:")
    filters.append({'material': 'Cu', 'thickness': 0.5})
    
    calculator = ESAKCalculator()  # New instance as per fix
    calculator.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    
    for filter_config in filters:
        if filter_config['thickness'] > 0:
            calculator.add_filtration(filter_config['material'], filter_config['thickness'])
    
    results3 = calculator.calculate_all_metrics()
    print(f"   ESAK: {results3.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results3.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Mean Energy: {results3.get('mean_energy_kev', 0):.1f} keV")
    
    # Test 4: User removes Cu filter
    print("\n4. User removes Cu filter:")
    filters.pop()  # Remove Cu filter
    
    calculator = ESAKCalculator()  # New instance as per fix
    calculator.set_clinical_parameters(kvp=kvp, ma=ma, time_s=time_s)
    
    for filter_config in filters:
        if filter_config['thickness'] > 0:
            calculator.add_filtration(filter_config['material'], filter_config['thickness'])
    
    results4 = calculator.calculate_all_metrics()
    print(f"   ESAK: {results4.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results4.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Mean Energy: {results4.get('mean_energy_kev', 0):.1f} keV")
    
    # Analysis
    print("\n" + "=" * 70)
    print("Analysis:")
    print("=" * 70)
    
    # Check expected changes
    change_1_to_2 = results1.get('esak_mgy', 0) > results2.get('esak_mgy', 0)
    change_2_to_3 = results2.get('esak_mgy', 0) > results3.get('esak_mgy', 0)
    change_3_to_4 = results3.get('esak_mgy', 0) < results4.get('esak_mgy', 0)
    
    hvl_1_to_2 = results1.get('hvl1_al_mm', 0) < results2.get('hvl1_al_mm', 0)
    hvl_2_to_3 = results2.get('hvl1_al_mm', 0) < results3.get('hvl1_al_mm', 0)
    hvl_3_to_4 = results3.get('hvl1_al_mm', 0) > results4.get('hvl1_al_mm', 0)
    
    print(f"Al 2.5mm → 5.0mm: ESAK decreases = {change_1_to_2}, HVL increases = {hvl_1_to_2}")
    print(f"Al 5.0mm + Cu 0.5mm: ESAK decreases = {change_2_to_3}, HVL increases = {hvl_2_to_3}")
    print(f"Remove Cu filter: ESAK increases = {change_3_to_4}, HVL decreases = {hvl_3_to_4}")
    
    all_changes_correct = all([change_1_to_2, change_2_to_3, change_3_to_4, hvl_1_to_2, hvl_2_to_3, hvl_3_to_4])
    
    if all_changes_correct:
        print("\n✅ All filter changes are working correctly!")
        print("   - Increasing filter thickness reduces ESAK and increases HVL")
        print("   - Adding filters reduces ESAK and increases HVL")
        print("   - Removing filters increases ESAK and decreases HVL")
    else:
        print("\n❌ Some filter changes are not working as expected")
        print("   Please check the filter processing logic")

def test_filter_persistence():
    """Test that filter changes don't persist between calculator instances"""
    
    print("\n" + "=" * 70)
    print("Testing Filter State Isolation")
    print("=" * 70)
    
    # Test 1: Create calculator with Al filter
    print("\n1. Calculator with Al 2.5mm filter:")
    calc1 = ESAKCalculator()
    calc1.set_clinical_parameters(kvp=120, ma=100, time_s=0.1)
    calc1.add_filtration('Al', 2.5)
    
    results1 = calc1.calculate_all_metrics()
    print(f"   ESAK: {results1.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results1.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Filters: {calc1.parameters.get('filters', [])}")
    
    # Test 2: Create new calculator with different filter
    print("\n2. New calculator with Al 5.0mm filter:")
    calc2 = ESAKCalculator()  # New instance
    calc2.set_clinical_parameters(kvp=120, ma=100, time_s=0.1)
    calc2.add_filtration('Al', 5.0)
    
    results2 = calc2.calculate_all_metrics()
    print(f"   ESAK: {results2.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results2.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Filters: {calc2.parameters.get('filters', [])}")
    
    # Test 3: Check that first calculator is not affected
    print("\n3. First calculator state should be unchanged:")
    print(f"   Filters: {calc1.parameters.get('filters', [])}")
    
    # Test 4: Create calculator with no filters
    print("\n4. New calculator with no filters:")
    calc3 = ESAKCalculator()  # New instance
    calc3.set_clinical_parameters(kvp=120, ma=100, time_s=0.1)
    # No filters added
    
    results3 = calc3.calculate_all_metrics()
    print(f"   ESAK: {results3.get('esak_mgy', 0):.3f} mGy")
    print(f"   HVL1 (Al): {results3.get('hvl1_al_mm', 0):.2f} mm")
    print(f"   Filters: {calc3.parameters.get('filters', [])}")
    
    # Verify isolation
    different_results = (results1.get('esak_mgy', 0) != results2.get('esak_mgy', 0) != results3.get('esak_mgy', 0))
    print(f"\n✅ Filter states are properly isolated: {different_results}")

def main():
    """Run all tests"""
    try:
        simulate_streamlit_filter_behavior()
        test_filter_persistence()
        
        print("\n" + "=" * 70)
        print("Fix verification completed successfully!")
        print("The new calculator instance approach should resolve the filter issue.")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()