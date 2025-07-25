"""
Device Configuration Module for Clinical X-ray Dosimetry Calculator

This module manages device-specific parameters and settings for different X-ray devices.
It provides a centralized configuration that can be easily updated when new devices are added
or existing device parameters need modification.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DeviceConfiguration:
    """
    Data class for storing device-specific configuration parameters.
    """
    name: str
    anode_angle: float
    filter_material: str
    filter_thickness: float
    description: str = ""
    
    def __str__(self) -> str:
        return self.name


class DeviceManager:
    """
    Manager class for handling device configurations and selections.
    """
    
    def __init__(self):
        """Initialize the device manager with predefined device configurations."""
        self._devices = self._load_device_configurations()
    
    def _load_device_configurations(self) -> Dict[str, DeviceConfiguration]:
        """
        Load predefined device configurations.
        
        Returns:
            Dictionary mapping device names to DeviceConfiguration objects
        """
        devices = {
            "1,2撮影室: RAD speed Pro": DeviceConfiguration(
                name="1,2撮影室: RAD speed Pro",
                anode_angle=16.0,
                filter_material="Al",
                filter_thickness=3.0,
                description="RAD speed Pro device for examination rooms 1 and 2"
            ),
            "3撮影室: RAD speed Pro": DeviceConfiguration(
                name="3撮影室: RAD speed Pro",
                anode_angle=16.0,
                filter_material="Al",
                filter_thickness=3.0,
                description="RAD speed Pro device for examination room 3"
            ),
            "歯科撮影装置ALULA": DeviceConfiguration(
                name="歯科撮影装置ALULA",
                anode_angle=12.5,
                filter_material="Al",
                filter_thickness=2.6,
                description="ALULA dental X-ray device"
            ),
            "Varian kV Imager": DeviceConfiguration(
                name="Varian kV Imager",
                anode_angle=14.0,
                filter_material="Al",
                filter_thickness=3.3,
                description="Varian kV imaging device"
            )
        }
        return devices
    
    def get_device_names(self) -> List[str]:
        """
        Get list of available device names.
        
        Returns:
            List of device names
        """
        return list(self._devices.keys())
    
    def get_device_configuration(self, device_name: str) -> Optional[DeviceConfiguration]:
        """
        Get configuration for a specific device.
        
        Args:
            device_name: Name of the device
            
        Returns:
            DeviceConfiguration object if found, None otherwise
        """
        return self._devices.get(device_name)
    
    def is_predefined_device(self, device_name: str) -> bool:
        """
        Check if a device name is in the predefined list.
        
        Args:
            device_name: Name of the device to check
            
        Returns:
            True if device is predefined, False otherwise
        """
        return device_name in self._devices
    
    def add_device(self, device_config: DeviceConfiguration) -> None:
        """
        Add a new device configuration.
        
        Args:
            device_config: DeviceConfiguration object to add
        """
        self._devices[device_config.name] = device_config
    
    def update_device(self, device_name: str, **kwargs) -> bool:
        """
        Update parameters for an existing device.
        
        Args:
            device_name: Name of the device to update
            **kwargs: Parameters to update (anode_angle, filter_material, filter_thickness, description)
            
        Returns:
            True if device was updated, False if device not found
        """
        if device_name not in self._devices:
            return False
        
        device = self._devices[device_name]
        
        for key, value in kwargs.items():
            if hasattr(device, key):
                setattr(device, key, value)
        
        return True
    
    def remove_device(self, device_name: str) -> bool:
        """
        Remove a device configuration.
        
        Args:
            device_name: Name of the device to remove
            
        Returns:
            True if device was removed, False if device not found
        """
        if device_name in self._devices:
            del self._devices[device_name]
            return True
        return False
    
    def get_device_options_for_dropdown(self) -> List[str]:
        """
        Get device options formatted for dropdown selection.
        
        Returns:
            List of device names with an option for custom input
        """
        device_names = self.get_device_names()
        return device_names + ["その他（カスタム入力）"]
    
    def get_device_summary(self) -> str:
        """
        Get a formatted summary of all devices and their configurations.
        
        Returns:
            Formatted string containing device information
        """
        summary_lines = ["=== Device Configuration Summary ===", ""]
        
        for device_name, config in self._devices.items():
            summary_lines.extend([
                f"Device: {device_name}",
                f"  Anode Angle: {config.anode_angle}°",
                f"  Filter: {config.filter_material} {config.filter_thickness} mm",
                f"  Description: {config.description}",
                ""
            ])
        
        return "\n".join(summary_lines)


# Global device manager instance
device_manager = DeviceManager()


def get_device_manager() -> DeviceManager:
    """
    Get the global device manager instance.
    
    Returns:
        DeviceManager instance
    """
    return device_manager


def get_device_names() -> List[str]:
    """
    Convenience function to get device names.
    
    Returns:
        List of available device names
    """
    return device_manager.get_device_names()


def get_device_config(device_name: str) -> Optional[DeviceConfiguration]:
    """
    Convenience function to get device configuration.
    
    Args:
        device_name: Name of the device
        
    Returns:
        DeviceConfiguration object if found, None otherwise
    """
    return device_manager.get_device_configuration(device_name)


def is_predefined_device(device_name: str) -> bool:
    """
    Convenience function to check if device is predefined.
    
    Args:
        device_name: Name of the device to check
        
    Returns:
        True if device is predefined, False otherwise
    """
    return device_manager.is_predefined_device(device_name)


if __name__ == "__main__":
    # Demo functionality
    print("Device Configuration Demo")
    print("=" * 40)
    
    # Display all devices
    print(device_manager.get_device_summary())
    
    # Test device lookup
    test_device = "1,2撮影室: RAD speed Pro"
    config = get_device_config(test_device)
    if config:
        print(f"Configuration for '{test_device}':")
        print(f"  Anode Angle: {config.anode_angle}°")
        print(f"  Filter: {config.filter_material} {config.filter_thickness} mm")
    
    # Test predefined check
    print(f"\nIs '{test_device}' predefined? {is_predefined_device(test_device)}")
    print(f"Is 'Custom Device' predefined? {is_predefined_device('Custom Device')}")