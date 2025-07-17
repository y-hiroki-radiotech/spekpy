"""
ESAK (Entrance Surface Air Kerma) Calculator using SpekPy

This module provides functionality to calculate ESAK and other dosimetric
parameters for clinical X-ray conditions using the SpekPy library.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../spekpy_release'))

try:
    import spekpy as sp
    from scipy.interpolate import RegularGridInterpolator
except ImportError:
    print("Warning: SpekPy or SciPy not installed. Please install using 'uv add spekpy scipy'")
    sp = None
    RegularGridInterpolator = None

import numpy as np
from typing import Dict, Tuple, List, Optional
import json


class ESAKCalculator:
    """
    A class to calculate ESAK and related dosimetric parameters for clinical X-ray examinations.
    
    This class provides methods to:
    - Generate X-ray spectra based on clinical parameters
    - Calculate ESAK (Entrance Surface Air Kerma)
    - Compute Half Value Layers (HVL)
    - Calculate fluence and other beam quality parameters
    """
    
    def __init__(self):
        """Initialize the ESAK calculator."""
        self.spectrum = None
        self.parameters = {}
        self.results = {}
        
    def set_clinical_parameters(self,
                              kvp: float,
                              ma: float,
                              time_s: float,
                              anode_angle: float = 12.0,
                              target_material: str = 'W',
                              ssd_cm: float = 100.0) -> None:
        """
        Set clinical parameters for X-ray exposure.
        
        Args:
            kvp: Tube voltage in kilovolts peak
            ma: Tube current in milliamperes
            time_s: Exposure time in seconds
            anode_angle: Anode angle in degrees (default: 12.0)
            target_material: Target material ('W' for tungsten, 'Mo' for molybdenum)
            ssd_cm: Source-to-skin distance in cm (default: 100.0)
        """
        self.parameters = {
            'kvp': kvp,
            'ma': ma,
            'time_s': time_s,
            'mas': ma * time_s,
            'anode_angle': anode_angle,
            'target_material': target_material,
            'ssd_cm': ssd_cm
        }
        
    def add_filtration(self, material: str, thickness_mm: float) -> None:
        """
        Add filtration to the X-ray beam.
        
        Args:
            material: Filter material (e.g., 'Al', 'Cu', 'Be')
            thickness_mm: Filter thickness in millimeters
        """
        if 'filters' not in self.parameters:
            self.parameters['filters'] = []
        
        self.parameters['filters'].append({
            'material': material,
            'thickness_mm': thickness_mm
        })
    
    def set_field_parameters(self, field_size_cm: float = 10.0, 
                           phantom_material: str = 'water') -> None:
        """
        Set field size and phantom parameters for BSF calculation.
        
        Args:
            field_size_cm: Field size (diameter) in cm at SSD (default: 10.0)
            phantom_material: Phantom material for BSF calculation (default: 'water')
        """
        self.parameters.update({
            'field_size_cm': field_size_cm,
            'phantom_material': phantom_material
        })
        
    def generate_spectrum(self) -> bool:
        """
        Generate X-ray spectrum based on set parameters.
        
        Returns:
            True if spectrum generation was successful, False otherwise
        """
        if sp is None:
            print("Error: SpekPy not available")
            return False
            
        if not self.parameters:
            print("Error: Clinical parameters not set")
            return False
            
        try:
            # Create spectrum
            self.spectrum = sp.Spek(
                kvp=self.parameters['kvp'],
                th=self.parameters['anode_angle']
            )
            
            # Apply filtration if specified
            if 'filters' in self.parameters:
                for filter_config in self.parameters['filters']:
                    self.spectrum.filter(
                        filter_config['material'],
                        filter_config['thickness_mm']
                    )
            
            return True
            
        except Exception as e:
            print(f"Error generating spectrum: {e}")
            return False
    
    def calculate_esak(self) -> float:
        """
        Calculate ESAK (Entrance Surface Air Kerma) in mGy.
        
        Returns:
            ESAK value in mGy
        """
        if self.spectrum is None:
            if not self.generate_spectrum():
                return 0.0
        
        try:
            # Get air kerma per mAs at reference distance (typically 100 cm)
            kerma_per_mas = self.spectrum.get_kerma()  # µGy per mAs
            
            # Calculate total kerma for actual mAs
            total_kerma_ugy = kerma_per_mas * self.parameters['mas']
            
            # Apply inverse square law correction if SSD != 100 cm
            reference_distance = 100.0  # cm
            actual_distance = self.parameters['ssd_cm']
            distance_correction = (reference_distance / actual_distance) ** 2
            
            corrected_kerma_ugy = total_kerma_ugy * distance_correction
            
            # Convert µGy to mGy
            esak_mgy = corrected_kerma_ugy / 1000.0
            
            self.results['esak_mgy'] = esak_mgy
            self.results['kerma_per_mas_ugy'] = kerma_per_mas
            self.results['distance_correction'] = distance_correction
            
            return esak_mgy
            
        except Exception as e:
            print(f"Error calculating ESAK: {e}")
            import traceback
            traceback.print_exc()
            return 0.0
    
    def calculate_bsf(self) -> float:
        """
        Calculate Backscatter Factor (BSF) for water phantom.
        
        Returns:
            BSF value (typically 1.0-1.5)
        """
        print(f"Starting BSF calculation...")
        print(f"Parameters: {self.parameters}")
        
        if sp is None or RegularGridInterpolator is None:
            print("Warning: SpekPy or SciPy not available for BSF calculation")
            return 1.0  # Default to no backscatter correction
        
        if self.spectrum is None:
            print("Generating spectrum for BSF calculation...")
            if not self.generate_spectrum():
                print("Failed to generate spectrum")
                return 1.0
        
        try:
            # Get field parameters
            field_size = self.parameters.get('field_size_cm', 10.0)
            ssd = self.parameters.get('ssd_cm', 100.0)
            print(f"BSF parameters: field_size={field_size} cm, ssd={ssd} cm")
            
            # Load BSF data from SpekPy tutorial directory
            # Try multiple possible paths for the BSF data file
            possible_paths = [
                os.path.join(os.path.dirname(__file__), '../9_Kilovoltage x-ray beam dosimetry/monoBSFw.npz'),
                os.path.join(os.path.dirname(__file__), '../../9_Kilovoltage x-ray beam dosimetry/monoBSFw.npz'),
                '/Users/user/Desktop/SpekPy/9_Kilovoltage x-ray beam dosimetry/monoBSFw.npz'
            ]
            
            bsf_data_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    bsf_data_path = path
                    break
            
            print(f"Looking for BSF data at: {bsf_data_path}")
            if bsf_data_path is None:
                print(f"Warning: BSF data file not found in any of the searched locations")
                return 1.0
            
            # Import monoenergy backscatter factor data
            data = np.load(bsf_data_path)
            SSD_data = data['SSD']
            K_data = data['k']
            D_data = data['D']
            Bw_data = data['Bw']
            
            # Define an interpolation function for the backscatter factor
            points = (SSD_data, K_data, D_data)
            bsf_interpolator = RegularGridInterpolator(
                points, Bw_data, bounds_error=False, fill_value=1.0
            )
            
            # Get spectrum data
            k, phi_k = self.spectrum.get_spectrum()
            
            # Get mass energy absorption coefficient at energies k
            try:
                muen_data = sp.Spek().muen_air_data
                muen_over_rho = muen_data.get_muen_over_rho_air(k)
            except:
                # Fallback if mass energy absorption data not available
                muen_over_rho = np.ones_like(k)
            
            # Interpolate mono BSF values based on ssd, k, and field_size values
            # Use the same format as the official SpekPy example
            interpolation_points = np.column_stack([np.full_like(k, ssd), k, np.full_like(k, field_size)])
            bsf_mono = bsf_interpolator(interpolation_points)
            
            # Calculate spectrum-weighted backscatter factor using numpy.sum
            # This follows the exact method from the SpekPy BSFw.py example
            numerator = np.sum(k * phi_k * muen_over_rho * bsf_mono)
            denominator = np.sum(k * phi_k * muen_over_rho)
            
            if denominator > 0:
                bsf_spectrum = numerator / denominator
            else:
                bsf_spectrum = 1.0
            
            # Store BSF in results
            self.results['bsf'] = bsf_spectrum
            
            print(f"BSF calculation successful: field_size={field_size} cm, ssd={ssd} cm, bsf={bsf_spectrum:.3f}")
            print(f"BSF calculation details: numerator={numerator:.3e}, denominator={denominator:.3e}")
            
            return bsf_spectrum
            
        except Exception as e:
            print(f"Error calculating BSF: {e}")
            import traceback
            traceback.print_exc()
            return 1.0
    
    def calculate_beam_quality_parameters(self) -> Dict:
        """
        Calculate beam quality parameters including HVL, mean energy, etc.
        
        Returns:
            Dictionary containing beam quality parameters
        """
        if self.spectrum is None:
            if not self.generate_spectrum():
                return {}
        
        try:
            # Calculate various beam quality parameters
            hvl1_al = self.spectrum.get_hvl1()  # First HVL in mm Al
            hvl2_al = self.spectrum.get_hvl2()  # Second HVL in mm Al
            hvl1_cu = self.spectrum.get_hvl1(matl='Cu')  # First HVL in mm Cu
            mean_energy = self.spectrum.get_emean()  # Mean energy in keV
            effective_energy = self.spectrum.get_eeff()  # Effective energy in keV
            total_fluence = self.spectrum.get_flu()  # Total fluence
            energy_fluence = self.spectrum.get_eflu()  # Energy fluence
            homogeneity_coefficient = self.spectrum.get_hc()  # Homogeneity coefficient
            
            beam_quality = {
                'hvl1_al_mm': hvl1_al,
                'hvl2_al_mm': hvl2_al,
                'hvl1_cu_mm': hvl1_cu,
                'mean_energy_kev': mean_energy,
                'effective_energy_kev': effective_energy,
                'total_fluence': total_fluence,
                'energy_fluence_kev': energy_fluence,
                'homogeneity_coefficient': homogeneity_coefficient
            }
            
            self.results.update(beam_quality)
            return beam_quality
            
        except Exception as e:
            print(f"Error calculating beam quality parameters: {e}")
            return {}
    
    def get_spectrum_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get spectrum energy bins and fluence values.
        
        Returns:
            Tuple of (energy_bins_kev, fluence_values)
        """
        if self.spectrum is None:
            if not self.generate_spectrum():
                return np.array([]), np.array([])
        
        try:
            energy, fluence = self.spectrum.get_spectrum(edges=True)
            return energy, fluence
        except Exception as e:
            print(f"Error getting spectrum data: {e}")
            return np.array([]), np.array([])
    
    def calculate_esak_with_bsf(self) -> float:
        """
        Calculate ESAK with Backscatter Factor (BSF) correction.
        
        Returns:
            ESAK in mGy including BSF correction
        """
        # Calculate basic ESAK
        esak_basic = self.calculate_esak()
        
        # Calculate BSF if field size is specified
        if 'field_size_cm' in self.parameters:
            bsf = self.calculate_bsf()
            esak_with_bsf = esak_basic * bsf
            
            # Store the corrected ESAK
            self.results['esak_with_bsf_mgy'] = esak_with_bsf
            
            return esak_with_bsf
        else:
            return esak_basic
    
    def calculate_all_metrics(self) -> Dict:
        """
        Calculate all dosimetric and beam quality metrics.
        
        Returns:
            Dictionary containing all calculated results
        """
        # Calculate ESAK
        esak = self.calculate_esak()
        
        # Calculate BSF and ESAK with BSF if field size is specified
        esak_with_bsf = self.calculate_esak_with_bsf()
        
        # Calculate beam quality parameters
        beam_quality = self.calculate_beam_quality_parameters()
        
        # Combine all results
        all_results = {
            'parameters': self.parameters.copy(),
            'esak_mgy': esak,
            **beam_quality,
            'calculation_notes': {
                'reference_distance_cm': 100.0,
                'kerma_units': 'Air kerma per mAs at 100 cm',
                'esak_definition': 'Entrance Surface Air Kerma corrected for actual SSD'
            }
        }
        
        # Add BSF results - either calculated or default 1.0
        if 'field_size_cm' in self.parameters:
            all_results['esak_with_bsf_mgy'] = esak_with_bsf
            # BSF value should be stored in self.results during calculate_bsf()
            bsf_value = self.results.get('bsf', 1.0)
            all_results['bsf'] = bsf_value
            all_results['calculation_notes']['bsf_note'] = f'BSF correction applied for field size: {bsf_value:.3f}'
            print(f"BSF applied: {bsf_value:.3f}, ESAK: {esak:.3f} → {esak_with_bsf:.3f} mGy")
        else:
            # Set BSF to 1.0 when not calculated
            all_results['bsf'] = 1.0
            all_results['calculation_notes']['bsf_note'] = 'BSF = 1.0 (no field size specified)'
        
        self.results = all_results
        return all_results
    
    def get_summary_text(self) -> str:
        """
        Get a formatted summary of the calculation results.
        
        Returns:
            Formatted string summary
        """
        if not self.results:
            self.calculate_all_metrics()
        
        summary_lines = [
            "=== X-ray Dosimetry Calculation Results ===",
            "",
            "Clinical Parameters:",
            f"  Tube Voltage: {self.parameters.get('kvp', 'N/A')} kVp",
            f"  Tube Current: {self.parameters.get('ma', 'N/A')} mA",
            f"  Exposure Time: {self.parameters.get('time_s', 'N/A')} s",
            f"  mAs: {self.parameters.get('mas', 'N/A')}",
            f"  Anode Angle: {self.parameters.get('anode_angle', 'N/A')}°",
            f"  SSD: {self.parameters.get('ssd_cm', 'N/A')} cm",
            "",
            "Filtration:",
        ]
        
        if 'filters' in self.parameters:
            for filter_config in self.parameters['filters']:
                summary_lines.append(
                    f"  {filter_config['material']}: {filter_config['thickness_mm']} mm"
                )
        else:
            summary_lines.append("  None specified")
        
        # Helper function to format values safely
        def safe_format(value, format_spec):
            if isinstance(value, (int, float)):
                return f"{value:{format_spec}}"
            else:
                return str(value)
        
        summary_lines.extend([
            "",
            "Dosimetric Results:",
            f"  ESAK: {safe_format(self.results.get('esak_mgy', 'N/A'), '.3f')} mGy",
            f"  Air Kerma per mAs: {safe_format(self.results.get('kerma_per_mas_ugy', 'N/A'), '.2f')} µGy/mAs",
            "",
            "Beam Quality Parameters:",
            f"  HVL1 (Al): {safe_format(self.results.get('hvl1_al_mm', 'N/A'), '.2f')} mm",
            f"  HVL1 (Cu): {safe_format(self.results.get('hvl1_cu_mm', 'N/A'), '.3f')} mm",
            f"  Mean Energy: {safe_format(self.results.get('mean_energy_kev', 'N/A'), '.1f')} keV",
            f"  Effective Energy: {safe_format(self.results.get('effective_energy_kev', 'N/A'), '.1f')} keV",
            f"  Homogeneity Coefficient: {safe_format(self.results.get('homogeneity_coefficient', 'N/A'), '.3f')}",
        ])
        
        return "\n".join(summary_lines)


def example_clinical_calculation():
    """
    Example calculation for typical clinical X-ray examination.
    """
    calculator = ESAKCalculator()
    
    # Set typical chest X-ray parameters
    calculator.set_clinical_parameters(
        kvp=120,
        ma=100,
        time_s=0.1,  # 100 ms
        anode_angle=12.0,
        ssd_cm=180  # Typical chest X-ray distance
    )
    
    # Add typical filtration
    calculator.add_filtration('Al', 2.5)  # 2.5 mm Al total filtration
    
    # Calculate all metrics
    results = calculator.calculate_all_metrics()
    
    # Print summary
    print(calculator.get_summary_text())
    
    return results


if __name__ == "__main__":
    # Run example calculation
    example_clinical_calculation()