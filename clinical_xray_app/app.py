"""
Streamlit Web Application for Clinical X-ray Dosimetry Calculator

This application provides a user-friendly interface for calculating ESAK
and other dosimetric parameters for clinical X-ray examinations.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import json
from datetime import datetime
from pathlib import Path

# Import our custom modules
from esak_calculator import ESAKCalculator
from visualization import XRayVisualizer
from data_export import DataExporter, create_report_template

# Page configuration
st.set_page_config(
    page_title="Clinical X-ray Dosimetry Calculator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e7d32;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculator' not in st.session_state:
    st.session_state.calculator = ESAKCalculator()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = XRayVisualizer()
if 'exporter' not in st.session_state:
    st.session_state.exporter = DataExporter()
if 'results' not in st.session_state:
    st.session_state.results = None
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Clinical X-ray Dosimetry Calculator</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    This application calculates **ESAK (Entrance Surface Air Kerma)** and other dosimetric 
    parameters for clinical X-ray examinations using the SpekPy spectral modeling toolkit.
    """)
    
    # Sidebar for parameters
    with st.sidebar:
        st.markdown('<h2 class="section-header">📋 Input Parameters</h2>', 
                    unsafe_allow_html=True)
        
        # Device and Protocol Information
        st.subheader("🏥 装置・プロトコール情報")
        
        device_name = st.text_input("装置名", 
                                    placeholder="例: SIEMENS Ysio Max",
                                    help="X線装置の製造会社・型番")
        
        protocol_name = st.text_input("プロトコール名", 
                                      placeholder="例: 胸部正面立位",
                                      help="検査プロトコールの名称")
        
        # Clinical parameters
        st.subheader("📊 Clinical Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            kvp = st.number_input("Tube Voltage (kVp)", 
                                  min_value=40, max_value=150, value=120, step=1)
            ma = st.number_input("Tube Current (mA)", 
                                 min_value=1, max_value=1000, value=100, step=1)
        
        with col2:
            time_s = st.number_input("Exposure Time (s)", 
                                     min_value=0.001, max_value=10.0, value=0.1, step=0.001, format="%.3f")
            anode_angle = st.number_input("Anode Angle (°)", 
                                          min_value=5.0, max_value=20.0, value=12.0, step=0.5)
        
        mas = ma * time_s
        st.info(f"**mAs**: {mas:.2f}")
        
        # Distance settings
        st.subheader("Geometry")
        ssd_cm = st.number_input("Source-to-Skin Distance (cm)", 
                                 min_value=50, max_value=300, value=100, step=1)
        
        # Target material
        target_material = st.selectbox("Target Material", 
                                       options=['W', 'Mo'], 
                                       index=0,
                                       help="W = Tungsten, Mo = Molybdenum")
        
        # Filtration
        st.subheader("Filtration")
        
        # Dynamic filter addition
        if 'filters' not in st.session_state:
            st.session_state.filters = [{'material': 'Al', 'thickness': 2.5}]
        
        # Display current filters
        for i, filter_config in enumerate(st.session_state.filters):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                material = st.selectbox(f"Filter {i+1} Material", 
                                        options=['Al', 'Cu', 'Be', 'Air'], 
                                        index=['Al', 'Cu', 'Be', 'Air'].index(filter_config['material']),
                                        key=f"filter_material_{i}")
            
            with col2:
                thickness = st.number_input(f"Thickness (mm)", 
                                            min_value=0.0, max_value=50.0, 
                                            value=filter_config['thickness'], 
                                            step=0.1, format="%.1f",
                                            key=f"filter_thickness_{i}")
            
            with col3:
                if st.button("🗑️", key=f"remove_filter_{i}", help="Remove filter"):
                    st.session_state.filters.pop(i)
                    st.rerun()
            
            # Update filter in session state
            st.session_state.filters[i] = {'material': material, 'thickness': thickness}
        
        # Add new filter button
        if st.button("➕ Add Filter"):
            st.session_state.filters.append({'material': 'Al', 'thickness': 1.0})
            st.rerun()
        
        # Calculation button
        st.markdown("---")
        calculate_button = st.button("🧮 Calculate ESAK", type="primary", use_container_width=True)
        
        # Quick presets
        st.subheader("Quick Presets")
        if st.button("Chest X-ray"):
            set_preset_chest()
        if st.button("Abdominal X-ray"):
            set_preset_abdomen()
        if st.button("Mammography"):
            set_preset_mammography()
    
    # Main content area
    if calculate_button:
        perform_calculation(kvp, ma, time_s, anode_angle, target_material, ssd_cm,
                          device_name, protocol_name)
    
    # Display results if available
    if st.session_state.results is not None:
        display_results()
    
    # Footer with additional options
    display_footer()

def set_preset_chest():
    """Set parameters for chest X-ray examination."""
    st.session_state.filters = [{'material': 'Al', 'thickness': 2.5}]
    st.rerun()

def set_preset_abdomen():
    """Set parameters for abdominal X-ray examination."""
    st.session_state.filters = [{'material': 'Al', 'thickness': 3.0}]
    st.rerun()

def set_preset_mammography():
    """Set parameters for mammography examination."""
    st.session_state.filters = [{'material': 'Be', 'thickness': 0.5}, 
                                {'material': 'Al', 'thickness': 0.1}]
    st.rerun()

def perform_calculation(kvp, ma, time_s, anode_angle, target_material, ssd_cm,
                       device_name, protocol_name):
    """Perform the ESAK calculation."""
    
    with st.spinner("Calculating X-ray spectrum and dosimetric parameters..."):
        try:
            # Set up calculator
            calculator = st.session_state.calculator
            calculator.set_clinical_parameters(
                kvp=kvp,
                ma=ma,
                time_s=time_s,
                anode_angle=anode_angle,
                target_material=target_material,
                ssd_cm=ssd_cm
            )
            
            # Add filtration
            for filter_config in st.session_state.filters:
                if filter_config['thickness'] > 0:
                    calculator.add_filtration(
                        filter_config['material'], 
                        filter_config['thickness']
                    )
            
            # Calculate all metrics
            results = calculator.calculate_all_metrics()
            
            if results:
                # Add device and protocol information to results
                results['device_info'] = {
                    'device_name': device_name,
                    'protocol_name': protocol_name,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.session_state.results = results
                
                # Add to history
                history_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'device_name': device_name,
                    'protocol_name': protocol_name,
                    'kvp': kvp,
                    'mas': ma * time_s,
                    'esak_mgy': results.get('esak_mgy', 0),
                    'hvl1_al_mm': results.get('hvl1_al_mm', 0)
                }
                st.session_state.calculation_history.append(history_entry)
                
                st.success("✅ Calculation completed successfully!")
            else:
                st.error("❌ Calculation failed. Please check your parameters.")
                
        except Exception as e:
            st.error(f"❌ Error during calculation: {str(e)}")
            st.info("💡 This might be due to missing SpekPy installation. Please run 'uv add spekpy' to install dependencies.")

def display_results():
    """Display calculation results."""
    
    results = st.session_state.results
    
    # Key results overview
    st.markdown('<h2 class="section-header">📊 Calculation Results</h2>', 
                unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ESAK", 
                  f"{results.get('esak_mgy', 0):.3f} mGy",
                  help="Entrance Surface Air Kerma")
    
    with col2:
        st.metric("HVL1 (Al)", 
                  f"{results.get('hvl1_al_mm', 0):.2f} mm",
                  help="First Half Value Layer in Aluminum")
    
    with col3:
        st.metric("Mean Energy", 
                  f"{results.get('mean_energy_kev', 0):.1f} keV",
                  help="Mean energy of the X-ray spectrum")
    
    with col4:
        st.metric("Air Kerma/mAs", 
                  f"{results.get('kerma_per_mas_ugy', 0):.2f} µGy",
                  help="Air kerma per mAs at 100 cm")
    
    # Detailed results
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Spectrum Plot", "📋 Detailed Results", 
                                       "📊 Beam Quality", "📁 Export Data"])
    
    with tab1:
        display_spectrum_plot()
    
    with tab2:
        display_detailed_results()
    
    with tab3:
        display_beam_quality_analysis()
    
    with tab4:
        display_export_options()

def display_spectrum_plot():
    """Display the X-ray spectrum plot."""
    
    try:
        calculator = st.session_state.calculator
        energy, fluence = calculator.get_spectrum_data()
        
        if len(energy) > 0 and len(fluence) > 0:
            visualizer = st.session_state.visualizer
            
            # Create spectrum plot
            fig = visualizer.plot_spectrum(
                energy, fluence, 
                title="X-ray Spectrum",
                show_characteristic_lines=True,
                target_material=st.session_state.results['parameters'].get('target_material', 'W')
            )
            
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
            # Spectrum statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Spectrum Statistics:**")
                total_fluence = np.trapz(fluence, energy) if hasattr(np, 'trapz') else 0.0
                weighted_mean = np.average(energy, weights=fluence)
                
                st.write(f"- Energy bins: {len(energy)}")
                st.write(f"- Energy range: {np.min(energy):.1f} - {np.max(energy):.1f} keV")
                st.write(f"- Total fluence: {total_fluence:.2e} cm⁻²")
                st.write(f"- Weighted mean: {weighted_mean:.1f} keV")
            
            with col2:
                # Download spectrum data
                csv_buffer = io.StringIO()
                spectrum_df = pd.DataFrame({
                    'Energy_keV': energy,
                    'Fluence_cm2_keV': fluence
                })
                spectrum_df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    label="📥 Download Spectrum Data (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"spectrum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("⚠️ Spectrum data not available. Please recalculate.")
            
    except Exception as e:
        st.error(f"❌ Error creating spectrum plot: {str(e)}")

def display_detailed_results():
    """Display detailed calculation results."""
    
    results = st.session_state.results
    
    # Device and Protocol Information
    if 'device_info' in results:
        st.subheader("🏥 装置・プロトコール情報")
        device_info = results['device_info']
        device_data = [
            ["装置名", device_info.get('device_name', 'N/A')],
            ["プロトコール名", device_info.get('protocol_name', 'N/A')],
            ["記録日時", device_info.get('timestamp', 'N/A')]
        ]
        device_df = pd.DataFrame(device_data, columns=["項目", "値"])
        st.table(device_df)
    
    # Parameters table
    st.subheader("📊 Input Parameters")
    
    params = results.get('parameters', {})
    param_data = []
    
    param_data.append(["Tube Voltage", f"{params.get('kvp', 'N/A')} kVp"])
    param_data.append(["Tube Current", f"{params.get('ma', 'N/A')} mA"])
    param_data.append(["Exposure Time", f"{params.get('time_s', 'N/A')} s"])
    param_data.append(["mAs", f"{params.get('mas', 'N/A')}"])
    param_data.append(["Anode Angle", f"{params.get('anode_angle', 'N/A')}°"])
    param_data.append(["Source-to-Skin Distance", f"{params.get('ssd_cm', 'N/A')} cm"])
    
    if 'filters' in params:
        for i, filter_config in enumerate(params['filters']):
            param_data.append([f"Filter {i+1}", 
                              f"{filter_config['material']} {filter_config['thickness_mm']} mm"])
    
    param_df = pd.DataFrame(param_data, columns=["Parameter", "Value"])
    st.table(param_df)
    
    # Results table
    st.subheader("Dosimetric Results")
    
    result_data = [
        ["ESAK", f"{results.get('esak_mgy', 'N/A'):.3f} mGy"],
        ["Air Kerma per mAs", f"{results.get('kerma_per_mas_ugy', 'N/A'):.2f} µGy/mAs"],
        ["Distance Correction Factor", f"{results.get('distance_correction', 'N/A'):.3f}"],
    ]
    
    st.subheader("Beam Quality Parameters")
    
    quality_data = [
        ["HVL1 (Al)", f"{results.get('hvl1_al_mm', 'N/A'):.2f} mm"],
        ["HVL2 (Al)", f"{results.get('hvl2_al_mm', 'N/A'):.2f} mm"],
        ["HVL1 (Cu)", f"{results.get('hvl1_cu_mm', 'N/A'):.3f} mm"],
        ["Mean Energy", f"{results.get('mean_energy_kev', 'N/A'):.1f} keV"],
        ["Effective Energy", f"{results.get('effective_energy_kev', 'N/A'):.1f} keV"],
        ["Homogeneity Coefficient", f"{results.get('homogeneity_coefficient', 'N/A'):.3f}"],
        ["Total Fluence", f"{results.get('total_fluence', 'N/A'):.2e} cm⁻²"],
        ["Energy Fluence", f"{results.get('energy_fluence_kev', 'N/A'):.2e} keV·cm⁻²"],
    ]
    
    result_df = pd.DataFrame(result_data, columns=["Parameter", "Value"])
    quality_df = pd.DataFrame(quality_data, columns=["Parameter", "Value"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.table(result_df)
    with col2:
        st.table(quality_df)

def display_beam_quality_analysis():
    """Display beam quality analysis plots."""
    
    try:
        results = st.session_state.results
        visualizer = st.session_state.visualizer
        
        # HVL analysis plot
        hvl_fig = visualizer.plot_hvl_analysis(results)
        st.pyplot(hvl_fig, use_container_width=True)
        plt.close(hvl_fig)
        
        # Dose summary plot
        dose_fig = visualizer.plot_dose_summary(results)
        st.pyplot(dose_fig, use_container_width=True)
        plt.close(dose_fig)
        
    except Exception as e:
        st.error(f"❌ Error creating beam quality plots: {str(e)}")

def display_export_options():
    """Display data export options."""
    
    st.subheader("Export Options")
    
    results = st.session_state.results
    exporter = st.session_state.exporter
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Individual Exports:**")
        
        # JSON export
        if st.button("📄 Export JSON"):
            try:
                json_data = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"xray_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Export error: {e}")
        
        # Text report export
        if st.button("📝 Generate Text Report"):
            try:
                calculator = st.session_state.calculator
                energy, fluence = calculator.get_spectrum_data()
                
                report = create_report_template(results, energy, fluence)
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"xray_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Report generation error: {e}")
    
    with col2:
        st.markdown("**Configuration:**")
        
        # Configuration export
        if st.button("⚙️ Export Configuration"):
            try:
                config_data = {
                    "parameters": results.get('parameters', {}),
                    "metadata": {
                        "created": datetime.now().isoformat(),
                        "description": "X-ray calculation configuration"
                    }
                }
                config_json = json.dumps(config_data, indent=2, default=str)
                st.download_button(
                    label="📥 Download Config",
                    data=config_json,
                    file_name=f"xray_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Config export error: {e}")

def display_footer():
    """Display footer with additional information and options."""
    
    st.markdown("---")
    
    # Calculation history
    if st.session_state.calculation_history:
        with st.expander("📈 Calculation History"):
            history_df = pd.DataFrame(st.session_state.calculation_history)
            if not history_df.empty:
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                st.dataframe(history_df, use_container_width=True)
                
                if st.button("🗑️ Clear History"):
                    st.session_state.calculation_history = []
                    st.rerun()
    
    # Information
    with st.expander("ℹ️ About This Application"):
        st.markdown("""
        ### Clinical X-ray Dosimetry Calculator
        
        This application calculates **ESAK (Entrance Surface Air Kerma)** and other dosimetric 
        parameters for clinical X-ray examinations using the SpekPy spectral modeling toolkit.
        
        **Key Features:**
        - Accurate X-ray spectrum modeling
        - ESAK calculation with distance correction
        - Half Value Layer (HVL) analysis
        - Beam quality parameter assessment
        - Data export in multiple formats
        - Interactive visualization
        
        **References:**
        - Poludniowski, G. et al. "SpekPy v2.0—a software toolkit for modeling x‐ray tube spectra." Medical Physics 48.7 (2021): 3630-3637.
        
        **Disclaimer:**
        This software is for educational and research purposes. Always verify dosimetric calculations 
        with appropriate quality assurance procedures in clinical settings.
        """)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🔬 Clinical X-ray Dosimetry Calculator | Built with SpekPy and Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()