"""
Visualization module for X-ray spectrum and dosimetry results.

This module provides plotting functions to visualize X-ray spectra,
beam quality parameters, and dosimetric calculations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Tuple, Optional
import io
import base64


class XRayVisualizer:
    """
    A class to create visualizations for X-ray spectra and dosimetric calculations.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        """
        Initialize the visualizer.
        
        Args:
            style: Matplotlib style to use (default: 'seaborn-v0_8')
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        # Set default parameters for better plots
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16,
            'lines.linewidth': 2,
            'grid.alpha': 0.3
        })
    
    def plot_spectrum(self, 
                     energy: np.ndarray, 
                     fluence: np.ndarray,
                     title: str = "X-ray Spectrum",
                     show_characteristic_lines: bool = True,
                     target_material: str = 'W') -> plt.Figure:
        """
        Plot X-ray spectrum.
        
        Args:
            energy: Energy bins in keV
            fluence: Fluence values
            title: Plot title
            show_characteristic_lines: Whether to show characteristic X-ray lines
            target_material: Target material for characteristic lines
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot spectrum
        ax.plot(energy, fluence, 'b-', linewidth=2, label='X-ray spectrum')
        ax.fill_between(energy, fluence, alpha=0.3, color='blue')
        
        # Add characteristic X-ray lines if requested
        if show_characteristic_lines and target_material.upper() == 'W':
            # Tungsten characteristic lines (approximate energies in keV)
            w_lines = {'L𝛼₁': 8.4, 'L𝛼₂': 8.3, 'L𝛽₁': 9.7, 'L𝛽₂': 9.8, 
                      'K𝛼₁': 59.3, 'K𝛼₂': 57.9, 'K𝛽₁': 67.2}
            
            max_fluence = np.max(fluence)
            for line_name, line_energy in w_lines.items():
                if line_energy < np.max(energy):
                    ax.axvline(x=line_energy, color='red', linestyle='--', 
                              alpha=0.7, linewidth=1)
                    ax.text(line_energy, max_fluence * 0.8, line_name, 
                           rotation=90, ha='right', va='bottom', fontsize=8)
        
        ax.set_xlabel('Energy (keV)')
        ax.set_ylabel('Differential Fluence (cm⁻² keV⁻¹)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format axes
        ax.set_xlim(0, np.max(energy))
        ax.set_ylim(0, np.max(fluence) * 1.1)
        
        plt.tight_layout()
        return fig
    
    def plot_hvl_analysis(self, 
                         results: Dict,
                         materials: List[str] = ['Al', 'Cu']) -> plt.Figure:
        """
        Plot HVL analysis showing beam hardening.
        
        Args:
            results: Dictionary containing calculation results
            materials: List of materials to show HVLs for
            
        Returns:
            matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # HVL bar chart
        hvl_data = []
        material_labels = []
        
        for material in materials:
            hvl1_key = f'hvl1_{material.lower()}_mm'
            hvl2_key = f'hvl2_{material.lower()}_mm'
            
            if hvl1_key in results and hvl2_key in results:
                hvl_data.append([results[hvl1_key], results[hvl2_key]])
                material_labels.append(material)
        
        if hvl_data:
            x = np.arange(len(material_labels))
            width = 0.35
            
            hvl1_values = [data[0] for data in hvl_data]
            hvl2_values = [data[1] for data in hvl_data]
            
            bars1 = ax1.bar(x - width/2, hvl1_values, width, label='HVL1', alpha=0.8)
            bars2 = ax1.bar(x + width/2, hvl2_values, width, label='HVL2', alpha=0.8)
            
            ax1.set_xlabel('Material')
            ax1.set_ylabel('HVL (mm)')
            ax1.set_title('Half Value Layers')
            ax1.set_xticks(x)
            ax1.set_xticklabels(material_labels)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}', ha='center', va='bottom')
            
            for bar in bars2:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}', ha='center', va='bottom')
        
        # Beam quality parameters
        beam_params = ['mean_energy_kev', 'effective_energy_kev', 'homogeneity_coefficient']
        param_names = ['Mean Energy\n(keV)', 'Effective Energy\n(keV)', 'Homogeneity\nCoefficient']
        param_values = []
        
        for param in beam_params:
            if param in results:
                param_values.append(results[param])
            else:
                param_values.append(0)
        
        # Create normalized bar chart for beam quality
        # Normalize each parameter to 0-1 scale for display
        if param_values:
            colors = ['skyblue', 'lightcoral', 'lightgreen']
            bars = ax2.bar(param_names, param_values, color=colors, alpha=0.8)
            
            ax2.set_title('Beam Quality Parameters')
            ax2.set_ylabel('Parameter Value')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, param_values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def plot_dose_summary(self, results: Dict) -> plt.Figure:
        """
        Create a summary plot of dose calculations.
        
        Args:
            results: Dictionary containing calculation results
            
        Returns:
            matplotlib Figure object
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # ESAK visualization
        if 'esak_mgy' in results:
            esak_value = results['esak_mgy']
            
            # Create a gauge-style plot for ESAK
            theta = np.linspace(0, np.pi, 100)
            radius = 1
            
            ax1.plot(radius * np.cos(theta), radius * np.sin(theta), 'k-', linewidth=3)
            
            # Color code based on typical dose ranges
            if esak_value < 1.0:
                color = 'green'
                level = 'Low'
            elif esak_value < 5.0:
                color = 'orange'
                level = 'Moderate'
            else:
                color = 'red'
                level = 'High'
            
            # Add needle indicating dose level
            needle_angle = np.pi * (1 - min(esak_value / 10.0, 1.0))
            ax1.plot([0, np.cos(needle_angle)], [0, np.sin(needle_angle)], 
                    color=color, linewidth=4)
            
            ax1.set_xlim(-1.2, 1.2)
            ax1.set_ylim(-0.2, 1.2)
            ax1.set_aspect('equal')
            ax1.set_title(f'ESAK: {esak_value:.3f} mGy\n({level} Dose)')
            ax1.axis('off')
            
            # Add dose scale
            ax1.text(0, -0.15, '0 mGy', ha='center', fontsize=10)
            ax1.text(-1, 0.5, '5 mGy', ha='center', fontsize=10, rotation=90)
            ax1.text(1, 0.5, '10+ mGy', ha='center', fontsize=10, rotation=-90)
        
        # Parameters summary
        if 'parameters' in results:
            params = results['parameters']
            param_text = []
            param_text.append(f"Tube Voltage: {params.get('kvp', 'N/A')} kVp")
            param_text.append(f"mAs: {params.get('mas', 'N/A')}")
            param_text.append(f"SSD: {params.get('ssd_cm', 'N/A')} cm")
            
            if 'filters' in params:
                param_text.append("Filtration:")
                for f in params['filters']:
                    param_text.append(f"  {f['material']}: {f['thickness_mm']} mm")
            
            ax2.text(0.05, 0.95, '\n'.join(param_text), transform=ax2.transAxes,
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
            ax2.set_title('Exposure Parameters')
            ax2.axis('off')
        
        # Beam quality metrics
        quality_metrics = ['hvl1_al_mm', 'mean_energy_kev', 'effective_energy_kev']
        quality_labels = ['HVL1 (Al)', 'Mean Energy', 'Effective Energy']
        quality_units = ['mm', 'keV', 'keV']
        
        quality_values = []
        for metric in quality_metrics:
            quality_values.append(results.get(metric, 0))
        
        if any(quality_values):
            colors = ['lightcoral', 'lightgreen', 'lightskyblue']
            bars = ax3.barh(quality_labels, quality_values, color=colors, alpha=0.8)
            
            ax3.set_title('Beam Quality Metrics')
            ax3.set_xlabel('Value')
            ax3.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for i, (bar, value, unit) in enumerate(zip(bars, quality_values, quality_units)):
                width = bar.get_width()
                ax3.text(width, bar.get_y() + bar.get_height()/2,
                        f'{value:.1f} {unit}', ha='left', va='center')
        
        # Distance correction factor
        if 'distance_correction' in results:
            correction = results['distance_correction']
            reference_ssd = 100
            actual_ssd = results.get('parameters', {}).get('ssd_cm', 100)
            
            # Show inverse square law effect
            distances = np.linspace(50, 200, 100)
            correction_factors = (reference_ssd / distances) ** 2
            
            ax4.plot(distances, correction_factors, 'b-', linewidth=2)
            ax4.axvline(x=actual_ssd, color='red', linestyle='--', linewidth=2,
                       label=f'Actual SSD: {actual_ssd} cm')
            ax4.axhline(y=correction, color='red', linestyle='--', linewidth=2,
                       label=f'Correction: {correction:.3f}')
            
            ax4.set_xlabel('Source-to-Skin Distance (cm)')
            ax4.set_ylabel('Dose Correction Factor')
            ax4.set_title('Inverse Square Law Correction')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        return fig
    
    def create_comparison_plot(self, 
                              results_list: List[Dict],
                              labels: List[str]) -> plt.Figure:
        """
        Create comparison plots for multiple calculations.
        
        Args:
            results_list: List of result dictionaries
            labels: Labels for each result set
            
        Returns:
            matplotlib Figure object
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # ESAK comparison
        esak_values = [res.get('esak_mgy', 0) for res in results_list]
        bars1 = ax1.bar(labels, esak_values, alpha=0.8, color='skyblue')
        ax1.set_ylabel('ESAK (mGy)')
        ax1.set_title('ESAK Comparison')
        ax1.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars1, esak_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.3f}', ha='center', va='bottom')
        
        # HVL comparison
        hvl_values = [res.get('hvl1_al_mm', 0) for res in results_list]
        bars2 = ax2.bar(labels, hvl_values, alpha=0.8, color='lightcoral')
        ax2.set_ylabel('HVL1 (mm Al)')
        ax2.set_title('HVL Comparison')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars2, hvl_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2f}', ha='center', va='bottom')
        
        # Mean energy comparison
        energy_values = [res.get('mean_energy_kev', 0) for res in results_list]
        bars3 = ax3.bar(labels, energy_values, alpha=0.8, color='lightgreen')
        ax3.set_ylabel('Mean Energy (keV)')
        ax3.set_title('Mean Energy Comparison')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars3, energy_values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}', ha='center', va='bottom')
        
        # Parameters table
        param_data = []
        for i, (res, label) in enumerate(zip(results_list, labels)):
            params = res.get('parameters', {})
            param_data.append([
                label,
                f"{params.get('kvp', 'N/A')} kVp",
                f"{params.get('mas', 'N/A')} mAs",
                f"{params.get('ssd_cm', 'N/A')} cm"
            ])
        
        if param_data:
            table = ax4.table(cellText=param_data,
                            colLabels=['Case', 'kVp', 'mAs', 'SSD'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            
            ax4.set_title('Parameter Comparison')
            ax4.axis('off')
        
        plt.tight_layout()
        return fig
    
    def save_plots_to_buffer(self, fig: plt.Figure, format: str = 'png') -> io.BytesIO:
        """
        Save matplotlib figure to BytesIO buffer.
        
        Args:
            fig: matplotlib Figure object
            format: Image format ('png', 'pdf', 'svg')
            
        Returns:
            BytesIO buffer containing the image
        """
        buffer = io.BytesIO()
        fig.savefig(buffer, format=format, dpi=300, bbox_inches='tight')
        buffer.seek(0)
        return buffer
    
    def fig_to_base64(self, fig: plt.Figure) -> str:
        """
        Convert matplotlib figure to base64 string for web display.
        
        Args:
            fig: matplotlib Figure object
            
        Returns:
            Base64 encoded string
        """
        buffer = self.save_plots_to_buffer(fig, 'png')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"


def demo_visualization():
    """
    Demonstration of visualization capabilities.
    """
    # Create sample data
    energy = np.linspace(0, 120, 1000)
    fluence = np.exp(-(energy - 40)**2 / 500) * np.exp(-energy / 30) * 1e6
    
    # Sample results
    sample_results = {
        'esak_mgy': 2.5,
        'hvl1_al_mm': 3.2,
        'hvl2_al_mm': 4.1,
        'hvl1_cu_mm': 0.25,
        'mean_energy_kev': 45.2,
        'effective_energy_kev': 52.8,
        'homogeneity_coefficient': 0.78,
        'distance_correction': 1.0,
        'parameters': {
            'kvp': 120,
            'mas': 10,
            'ssd_cm': 100,
            'filters': [{'material': 'Al', 'thickness_mm': 2.5}]
        }
    }
    
    # Create visualizer
    visualizer = XRayVisualizer()
    
    # Create plots
    spectrum_fig = visualizer.plot_spectrum(energy, fluence, "Sample X-ray Spectrum")
    hvl_fig = visualizer.plot_hvl_analysis(sample_results)
    dose_fig = visualizer.plot_dose_summary(sample_results)
    
    # Display plots
    plt.show()


if __name__ == "__main__":
    demo_visualization()