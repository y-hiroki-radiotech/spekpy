"""
Data export functionality for X-ray dosimetry calculations.

This module provides functions to export calculation results and spectrum data
in various formats including CSV, JSON, and Excel.
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from pathlib import Path


class DataExporter:
    """
    A class to handle exporting X-ray dosimetry data in various formats.
    """
    
    def __init__(self, output_dir: str = "exports"):
        """
        Initialize the data exporter.
        
        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def export_results_json(self, 
                           results: Dict, 
                           filename: Optional[str] = None,
                           include_timestamp: bool = True) -> str:
        """
        Export calculation results to JSON format.
        
        Args:
            results: Dictionary containing calculation results
            filename: Output filename (auto-generated if None)
            include_timestamp: Whether to include timestamp in filename
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else ""
            filename = f"xray_results_{timestamp}.json" if timestamp else "xray_results.json"
        
        filepath = self.output_dir / filename
        
        # Prepare data for JSON export (handle numpy arrays)
        exportable_results = self._prepare_for_json(results)
        
        # Add metadata including device info if available
        metadata = {
            "export_timestamp": datetime.now().isoformat(),
            "software": "Clinical X-ray Dosimetry Calculator",
            "version": "1.0.0",
            "description": "X-ray spectrum and dosimetry calculation results"
        }
        
        # Include device information if available
        if 'device_info' in results:
            device_info = results['device_info']
            metadata.update({
                "device_name": device_info.get('device_name', ''),
                "protocol_name": device_info.get('protocol_name', ''),
                "measurement_timestamp": device_info.get('timestamp', '')
            })
        
        export_data = {
            "metadata": metadata,
            "results": exportable_results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_spectrum_csv(self, 
                           energy: np.ndarray, 
                           fluence: np.ndarray,
                           filename: Optional[str] = None,
                           include_metadata: bool = True) -> str:
        """
        Export spectrum data to CSV format.
        
        Args:
            energy: Energy bins in keV
            fluence: Fluence values
            filename: Output filename (auto-generated if None)
            include_metadata: Whether to include metadata in the file
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xray_spectrum_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Create DataFrame
        df = pd.DataFrame({
            'Energy_keV': energy,
            'Fluence_cm2_keV': fluence
        })
        
        # Write with metadata if requested
        if include_metadata:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                # Write metadata as comments
                f.write(f"# X-ray Spectrum Data\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n")
                f.write(f"# Energy bins: {len(energy)}\n")
                f.write(f"# Energy range: {np.min(energy):.1f} - {np.max(energy):.1f} keV\n")
                total_fluence = np.trapz(fluence, energy) if hasattr(np, 'trapz') else 0.0 if hasattr(np, 'trapz') else 0.0
                f.write(f"# Total fluence: {total_fluence:.2e} cm^-2\n")
                f.write(f"#\n")
                
                # Write CSV data
                df.to_csv(f, index=False)
        else:
            df.to_csv(filepath, index=False)
        
        return str(filepath)
    
    def export_summary_csv(self, 
                          results: Dict,
                          filename: Optional[str] = None) -> str:
        """
        Export calculation summary to CSV format.
        
        Args:
            results: Dictionary containing calculation results
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xray_summary_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Extract key parameters and results
        summary_data = []
        
        # Parameters
        if 'parameters' in results:
            params = results['parameters']
            summary_data.extend([
                ['Parameter', 'Tube Voltage', f"{params.get('kvp', 'N/A')} kVp"],
                ['Parameter', 'Tube Current', f"{params.get('ma', 'N/A')} mA"],
                ['Parameter', 'Exposure Time', f"{params.get('time_s', 'N/A')} s"],
                ['Parameter', 'mAs', f"{params.get('mas', 'N/A')}"],
                ['Parameter', 'Anode Angle', f"{params.get('anode_angle', 'N/A')}°"],
                ['Parameter', 'SSD', f"{params.get('ssd_cm', 'N/A')} cm"],
            ])
            
            # Filtration
            if 'filters' in params:
                for i, filter_config in enumerate(params['filters']):
                    summary_data.append([
                        'Parameter', 
                        f'Filter {i+1}', 
                        f"{filter_config['material']} {filter_config['thickness_mm']} mm"
                    ])
        
        # Results
        result_mappings = [
            ('esak_mgy', 'ESAK (or IAK)', 'mGy'),
            ('bsf', 'BSF', ''),
            ('esak_with_bsf_mgy', 'ESAK (BSF corrected)', 'mGy'),
            ('kerma_per_mas_ugy', 'Air Kerma per mAs', 'µGy/mAs'),
            ('hvl1_al_mm', 'HVL1 (Al)', 'mm'),
            ('hvl2_al_mm', 'HVL2 (Al)', 'mm'),
            ('hvl1_cu_mm', 'HVL1 (Cu)', 'mm'),
            ('mean_energy_kev', 'Mean Energy', 'keV'),
            ('effective_energy_kev', 'Effective Energy', 'keV'),
            ('homogeneity_coefficient', 'Homogeneity Coefficient', ''),
            ('total_fluence', 'Total Fluence', 'cm^-2'),
            ('energy_fluence_kev', 'Energy Fluence', 'keV·cm^-2'),
        ]
        
        for key, name, unit in result_mappings:
            if key in results:
                value = results[key]
                if isinstance(value, (int, float)):
                    if unit:
                        summary_data.append(['Result', name, f"{value:.4g} {unit}"])
                    else:
                        summary_data.append(['Result', name, f"{value:.4g}"])
        
        # Create DataFrame and save
        df = pd.DataFrame(summary_data, columns=['Category', 'Parameter', 'Value'])
        
        # Add metadata header
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(f"# X-ray Dosimetry Calculation Summary\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"#\n")
            df.to_csv(f, index=False)
        
        return str(filepath)
    
    def export_comparison_csv(self, 
                             results_list: List[Dict],
                             case_names: List[str],
                             filename: Optional[str] = None) -> str:
        """
        Export comparison of multiple calculations to CSV.
        
        Args:
            results_list: List of result dictionaries
            case_names: Names for each case
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xray_comparison_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Define parameters and results to compare
        comparison_items = [
            # Parameters
            ('parameters.kvp', 'Tube Voltage (kVp)', 'parameter'),
            ('parameters.mas', 'mAs', 'parameter'),
            ('parameters.ssd_cm', 'SSD (cm)', 'parameter'),
            # Results
            ('esak_mgy', 'ESAK (mGy)', 'result'),
            ('hvl1_al_mm', 'HVL1 Al (mm)', 'result'),
            ('hvl1_cu_mm', 'HVL1 Cu (mm)', 'result'),
            ('mean_energy_kev', 'Mean Energy (keV)', 'result'),
            ('effective_energy_kev', 'Effective Energy (keV)', 'result'),
            ('homogeneity_coefficient', 'Homogeneity Coefficient', 'result'),
        ]
        
        # Build comparison table
        comparison_data = []
        
        for key_path, label, category in comparison_items:
            row = [category.title(), label]
            
            for results in results_list:
                value = self._get_nested_value(results, key_path)
                if value is not None:
                    if isinstance(value, (int, float)):
                        row.append(f"{value:.4g}")
                    else:
                        row.append(str(value))
                else:
                    row.append('N/A')
            
            comparison_data.append(row)
        
        # Create DataFrame
        columns = ['Category', 'Parameter'] + case_names
        df = pd.DataFrame(comparison_data, columns=columns)
        
        # Save with metadata
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(f"# X-ray Dosimetry Comparison\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Cases compared: {len(case_names)}\n")
            f.write(f"#\n")
            df.to_csv(f, index=False)
        
        return str(filepath)
    
    def export_configuration(self, 
                           results: Dict,
                           filename: Optional[str] = None) -> str:
        """
        Export calculation configuration for later reuse.
        
        Args:
            results: Dictionary containing calculation results
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xray_config_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Extract only parameters for configuration
        config_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "description": "X-ray calculation configuration",
                "version": "1.0.0"
            },
            "parameters": results.get('parameters', {}),
            "notes": "This configuration can be loaded to reproduce the calculation"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_configuration(self, filepath: str) -> Dict:
        """
        Load calculation configuration from file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            Dictionary containing parameters
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return config_data.get('parameters', {})
    
    def export_all_formats(self, 
                          results: Dict,
                          energy: Optional[np.ndarray] = None,
                          fluence: Optional[np.ndarray] = None,
                          prefix: str = "xray_export") -> Dict[str, str]:
        """
        Export results in all available formats.
        
        Args:
            results: Dictionary containing calculation results
            energy: Energy bins for spectrum export
            fluence: Fluence values for spectrum export
            prefix: Filename prefix
            
        Returns:
            Dictionary mapping format names to file paths
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exported_files = {}
        
        # JSON results
        exported_files['json'] = self.export_results_json(
            results, f"{prefix}_{timestamp}.json"
        )
        
        # CSV summary
        exported_files['summary_csv'] = self.export_summary_csv(
            results, f"{prefix}_summary_{timestamp}.csv"
        )
        
        # Configuration
        exported_files['config'] = self.export_configuration(
            results, f"{prefix}_config_{timestamp}.json"
        )
        
        # Spectrum data if available
        if energy is not None and fluence is not None:
            exported_files['spectrum_csv'] = self.export_spectrum_csv(
                energy, fluence, f"{prefix}_spectrum_{timestamp}.csv"
            )
        
        return exported_files
    
    def _prepare_for_json(self, data: Any) -> Any:
        """
        Prepare data for JSON serialization by converting numpy arrays to lists.
        
        Args:
            data: Data to prepare
            
        Returns:
            JSON-serializable data
        """
        if isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, np.floating):
            return float(data)
        elif isinstance(data, np.integer):
            return int(data)
        elif isinstance(data, dict):
            return {key: self._prepare_for_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._prepare_for_json(item) for item in data]
        else:
            return data
    
    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """
        Get value from nested dictionary using dot notation.
        
        Args:
            data: Dictionary to search
            key_path: Dot-separated key path (e.g., 'parameters.kvp')
            
        Returns:
            Value if found, None otherwise
        """
        keys = key_path.split('.')
        current = data
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return None


def create_report_template(results: Dict, 
                         energy: Optional[np.ndarray] = None,
                         fluence: Optional[np.ndarray] = None) -> str:
    """
    Create a formatted text report template.
    
    Args:
        results: Dictionary containing calculation results
        energy: Energy bins for spectrum
        fluence: Fluence values for spectrum
        
    Returns:
        Formatted report string
    """
    report_lines = [
        "=" * 60,
        "X-RAY DOSIMETRY CALCULATION REPORT",
        "=" * 60,
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    
    # Add device and protocol information if available
    if 'device_info' in results:
        device_info = results['device_info']
        report_lines.extend([
            "DEVICE & PROTOCOL INFORMATION:",
            "-" * 32,
            f"Device Name:      {device_info.get('device_name', 'N/A')}",
            f"Protocol Name:    {device_info.get('protocol_name', 'N/A')}",
            f"Measurement Time: {device_info.get('timestamp', 'N/A')}",
            "",
        ])
    
    report_lines.extend([
        "CLINICAL PARAMETERS:",
        "-" * 20,
    ])
    
    # Parameters
    if 'parameters' in results:
        params = results['parameters']
        report_lines.extend([
            f"Tube Voltage:     {params.get('kvp', 'N/A')} kVp",
            f"Tube Current:     {params.get('ma', 'N/A')} mA",
            f"Exposure Time:    {params.get('time_s', 'N/A')} s",
            f"mAs:              {params.get('mas', 'N/A')}",
            f"Anode Angle:      {params.get('anode_angle', 'N/A')}°",
            f"SSD:              {params.get('ssd_cm', 'N/A')} cm",
            "",
            "FILTRATION:",
            "-" * 12,
        ])
        
        if 'filters' in params and params['filters']:
            for filter_config in params['filters']:
                report_lines.append(
                    f"{filter_config['material']:>8}: {filter_config['thickness_mm']} mm"
                )
        else:
            report_lines.append("None specified")
    
    # Results
    has_bsf = 'field_size_cm' in results.get('parameters', {})
    
    if has_bsf:
        report_lines.extend([
            "",
            "DOSIMETRIC RESULTS:",
            "-" * 19,
            f"IAK:              {results.get('esak_mgy', 'N/A'):.3f} mGy",
            f"BSF:              {results.get('bsf', 'N/A'):.3f}",
            f"ESAK (BSF corr.): {results.get('esak_with_bsf_mgy', 'N/A'):.3f} mGy",
            f"Air Kerma/mAs:    {results.get('kerma_per_mas_ugy', 'N/A'):.2f} µGy/mAs",
            f"Field Size:       {results.get('parameters', {}).get('field_size_cm', 'N/A')} cm",
            "",
        ])
    else:
        report_lines.extend([
            "",
            "DOSIMETRIC RESULTS:",
            "-" * 19,
            f"ESAK:             {results.get('esak_mgy', 'N/A'):.3f} mGy",
            f"BSF:              {results.get('bsf', 1.0):.3f}",
            f"Air Kerma/mAs:    {results.get('kerma_per_mas_ugy', 'N/A'):.2f} µGy/mAs",
            "",
        ])
    
    report_lines.extend([
        "BEAM QUALITY PARAMETERS:",
        "-" * 25,
        f"HVL1 (Al):        {results.get('hvl1_al_mm', 'N/A'):.2f} mm",
        f"HVL2 (Al):        {results.get('hvl2_al_mm', 'N/A'):.2f} mm",
        f"HVL1 (Cu):        {results.get('hvl1_cu_mm', 'N/A'):.3f} mm",
        f"Mean Energy:      {results.get('mean_energy_kev', 'N/A'):.1f} keV",
        f"Effective Energy: {results.get('effective_energy_kev', 'N/A'):.1f} keV",
        f"Homog. Coeff.:    {results.get('homogeneity_coefficient', 'N/A'):.3f}",
        "",
    ])
    
    # Spectrum summary if available
    if energy is not None and fluence is not None:
        mean_energy_spectrum = np.average(energy, weights=fluence)
        total_fluence = np.trapz(fluence, energy) if hasattr(np, 'trapz') else 0.0
        
        report_lines.extend([
            "SPECTRUM SUMMARY:",
            "-" * 17,
            f"Energy Bins:      {len(energy)}",
            f"Energy Range:     {np.min(energy):.1f} - {np.max(energy):.1f} keV",
            f"Total Fluence:    {total_fluence:.2e} cm⁻²",
            f"Weighted Mean:    {mean_energy_spectrum:.1f} keV",
        ])
    
    report_lines.extend([
        "",
        "=" * 60,
        "End of Report",
        "=" * 60
    ])
    
    return "\n".join(report_lines)


def demo_export():
    """
    Demonstration of export functionality.
    """
    # Sample results
    sample_results = {
        'esak_mgy': 2.456,
        'kerma_per_mas_ugy': 245.6,
        'hvl1_al_mm': 3.2,
        'hvl2_al_mm': 4.1,
        'hvl1_cu_mm': 0.25,
        'mean_energy_kev': 45.2,
        'effective_energy_kev': 52.8,
        'homogeneity_coefficient': 0.78,
        'distance_correction': 1.0,
        'parameters': {
            'kvp': 120,
            'ma': 100,
            'time_s': 0.1,
            'mas': 10,
            'anode_angle': 12.0,
            'ssd_cm': 100,
            'filters': [{'material': 'Al', 'thickness_mm': 2.5}]
        }
    }
    
    # Sample spectrum data
    energy = np.linspace(0, 120, 1000)
    fluence = np.exp(-(energy - 40)**2 / 500) * np.exp(-energy / 30) * 1e6
    
    # Create exporter
    exporter = DataExporter("demo_exports")
    
    # Export in all formats
    exported_files = exporter.export_all_formats(sample_results, energy, fluence)
    
    print("Export demonstration completed!")
    print("Exported files:")
    for format_name, filepath in exported_files.items():
        print(f"  {format_name}: {filepath}")
    
    # Create text report
    report = create_report_template(sample_results, energy, fluence)
    print("\nText Report:")
    print(report)


if __name__ == "__main__":
    demo_export()