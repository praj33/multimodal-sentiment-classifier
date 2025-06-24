#!/usr/bin/env python3
"""
Fusion Configuration Manager for Day 3 Runtime Control
Handles dynamic configuration loading, team presets, and runtime adjustments
"""

import os
import yaml
import time
import threading
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

class FusionConfigManager:
    """Manages fusion configuration with Day 3 runtime control features"""
    
    def __init__(self, config_path: str = "config/fusion_config.yaml"):
        self.config_path = Path(config_path)
        self.config = {}
        self.last_modified = 0
        self.hot_reload_enabled = False
        self.reload_thread = None
        self.logger = logging.getLogger(__name__)
        
        # Load initial configuration
        self.load_config()
        
        # Start hot reload if enabled
        if self.config.get('fusion', {}).get('hot_reload', False):
            self.start_hot_reload()
    
    def load_config(self) -> Dict[str, Any]:
        """Load fusion configuration from YAML file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = yaml.safe_load(f)
                self.last_modified = self.config_path.stat().st_mtime
                self.logger.info(f"Loaded fusion config from {self.config_path}")
            else:
                self.logger.warning(f"Fusion config file not found: {self.config_path}")
                self.config = self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading fusion config: {e}")
            self.config = self._get_default_config()
        
        # Validate configuration
        self._validate_config()
        return self.config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default fusion configuration"""
        return {
            'fusion': {
                'method': 'confidence_weighted',
                'enable_dynamic_weights': True,
                'confidence_threshold': 0.7,
                'hot_reload': False
            },
            'weights': {
                'text': 0.5,
                'audio': 0.25,
                'video': 0.25
            }
        }
    
    def _validate_config(self) -> bool:
        """Validate configuration according to Day 3 rules"""
        validation_rules = self.config.get('validation_rules', {})
        
        # Validate weights
        weights = self.config.get('weights', {})
        if validation_rules.get('weights', {}).get('sum_must_equal_one', True):
            weight_sum = sum(weights.values())
            if abs(weight_sum - 1.0) > 0.01:
                self.logger.warning(f"Weights sum to {weight_sum}, normalizing to 1.0")
                # Normalize weights
                for key in weights:
                    weights[key] = weights[key] / weight_sum
        
        # Validate confidence thresholds
        confidence_threshold = self.config.get('fusion', {}).get('confidence_threshold', 0.7)
        min_conf = validation_rules.get('confidence_thresholds', {}).get('min_value', 0.1)
        max_conf = validation_rules.get('confidence_thresholds', {}).get('max_value', 0.99)
        
        if not (min_conf <= confidence_threshold <= max_conf):
            self.logger.warning(f"Confidence threshold {confidence_threshold} out of range [{min_conf}, {max_conf}]")
            self.config['fusion']['confidence_threshold'] = max(min_conf, min(max_conf, confidence_threshold))
        
        return True
    
    def start_hot_reload(self):
        """Start hot reload monitoring thread"""
        if self.reload_thread and self.reload_thread.is_alive():
            return
            
        self.hot_reload_enabled = True
        self.reload_thread = threading.Thread(target=self._hot_reload_worker, daemon=True)
        self.reload_thread.start()
        self.logger.info("Started fusion config hot reload monitoring")
    
    def stop_hot_reload(self):
        """Stop hot reload monitoring"""
        self.hot_reload_enabled = False
        if self.reload_thread:
            self.reload_thread.join(timeout=1)
        self.logger.info("Stopped fusion config hot reload monitoring")
    
    def _hot_reload_worker(self):
        """Worker thread for hot reload monitoring"""
        reload_interval = self.config.get('fusion', {}).get('reload_interval', 30)
        
        while self.hot_reload_enabled:
            try:
                if self.config_path.exists():
                    current_modified = self.config_path.stat().st_mtime
                    if current_modified > self.last_modified:
                        self.logger.info("Fusion config file changed, reloading...")
                        self.load_config()
                        
                time.sleep(reload_interval)
            except Exception as e:
                self.logger.error(f"Error in hot reload worker: {e}")
                time.sleep(reload_interval)
    
    def get_team_preset(self, team_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration preset for specific team (Day 3 feature)"""
        presets = self.config.get('fusion', {}).get('team_presets', {})
        return presets.get(team_name)
    
    def apply_team_preset(self, team_name: str) -> bool:
        """Apply team-specific configuration preset"""
        preset = self.get_team_preset(team_name)
        if not preset:
            self.logger.warning(f"No preset found for team: {team_name}")
            return False
        
        # Apply preset configuration
        if 'method' in preset:
            self.config['fusion']['method'] = preset['method']
        if 'weights' in preset:
            self.config['weights'].update(preset['weights'])
        if 'confidence_threshold' in preset:
            self.config['fusion']['confidence_threshold'] = preset['confidence_threshold']
        
        self.logger.info(f"Applied team preset for: {team_name}")
        return True
    
    def get_fusion_method(self) -> str:
        """Get current fusion method"""
        return self.config.get('fusion', {}).get('method', 'confidence_weighted')
    
    def get_weights(self, normalize: bool = True) -> Dict[str, float]:
        """Get current fusion weights"""
        weights = self.config.get('weights', {}).copy()
        
        if normalize:
            weight_sum = sum(weights.values())
            if weight_sum > 0:
                weights = {k: v / weight_sum for k, v in weights.items()}
        
        return weights
    
    def get_confidence_threshold(self) -> float:
        """Get current confidence threshold"""
        return self.config.get('fusion', {}).get('confidence_threshold', 0.7)
    
    def update_weights(self, new_weights: Dict[str, float], validate: bool = True) -> bool:
        """Update fusion weights at runtime (Day 3 feature)"""
        if validate:
            # Validate new weights
            weight_sum = sum(new_weights.values())
            if abs(weight_sum - 1.0) > 0.01:
                # Normalize weights
                new_weights = {k: v / weight_sum for k, v in new_weights.items()}
        
        self.config['weights'].update(new_weights)
        self.logger.info(f"Updated fusion weights: {new_weights}")
        return True
    
    def update_method(self, method: str) -> bool:
        """Update fusion method at runtime"""
        valid_methods = ['simple', 'confidence_weighted', 'adaptive', 'custom']
        if method not in valid_methods:
            self.logger.error(f"Invalid fusion method: {method}")
            return False
        
        self.config['fusion']['method'] = method
        self.logger.info(f"Updated fusion method to: {method}")
        return True
    
    def get_environment_config(self, environment: str = None) -> Dict[str, Any]:
        """Get environment-specific configuration (Day 3 feature)"""
        if not environment:
            environment = os.getenv('ENVIRONMENT', 'development')
        
        env_configs = self.config.get('environments', {})
        env_config = env_configs.get(environment, {})
        
        # Merge with base config
        merged_config = self.config.copy()
        for section, values in env_config.items():
            if section in merged_config:
                merged_config[section].update(values)
            else:
                merged_config[section] = values
        
        return merged_config
    
    def get_integration_notes(self, team: str = None) -> Dict[str, Any]:
        """Get integration notes for teams (Day 3 feature)"""
        notes = self.config.get('integration_notes', {})
        if team:
            return notes.get(team, {})
        return notes
    
    def export_config(self, include_comments: bool = True) -> str:
        """Export current configuration as YAML string"""
        if include_comments:
            # Add helpful comments for teams
            config_with_comments = {
                '# Day 3 Fusion Configuration': None,
                '# Teams can modify weights and methods without code changes': None,
                **self.config
            }
            return yaml.dump(config_with_comments, default_flow_style=False)
        else:
            return yaml.dump(self.config, default_flow_style=False)
    
    def save_config(self, backup: bool = True) -> bool:
        """Save current configuration to file"""
        try:
            if backup and self.config_path.exists():
                backup_path = self.config_path.with_suffix('.yaml.backup')
                backup_path.write_text(self.config_path.read_text())
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            self.logger.info(f"Saved fusion config to {self.config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving fusion config: {e}")
            return False

# Global instance for easy access
_fusion_config_manager = None

def get_fusion_config_manager() -> FusionConfigManager:
    """Get global fusion configuration manager instance"""
    global _fusion_config_manager
    if _fusion_config_manager is None:
        _fusion_config_manager = FusionConfigManager()
    return _fusion_config_manager

def reload_fusion_config():
    """Reload fusion configuration"""
    manager = get_fusion_config_manager()
    return manager.load_config()

if __name__ == "__main__":
    # Test the fusion config manager
    manager = FusionConfigManager()
    
    print("Current fusion method:", manager.get_fusion_method())
    print("Current weights:", manager.get_weights())
    print("Available team presets:", list(manager.config.get('fusion', {}).get('team_presets', {}).keys()))
    
    # Test team preset
    if manager.apply_team_preset('gandhar_avatar_emotions'):
        print("Applied Gandhar's preset")
        print("New weights:", manager.get_weights())
    
    # Test integration notes
    notes = manager.get_integration_notes('gandhar_team')
    print("Integration notes for Gandhar's team:", notes)
