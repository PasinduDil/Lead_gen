# Configuration loader for the leadgen application

import os
from typing import Dict, Any, Optional
import yaml


class ConfigLoader:
    """Utility class for loading configuration from YAML files"""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize the config loader
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.config_cache: Dict[str, Any] = {}
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load a YAML file
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Dictionary containing the YAML content
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    
    def get_config(self, refresh: bool = False) -> Dict[str, Any]:
        """Get the main configuration
        
        Args:
            refresh: Whether to refresh the cached configuration
            
        Returns:
            Dictionary containing the configuration
        """
        if "config" not in self.config_cache or refresh:
            file_path = os.path.join(self.config_dir, "config.yaml")
            self.config_cache["config"] = self._load_yaml(file_path)
        return self.config_cache["config"]
    
    def get_prompts(self, refresh: bool = False) -> Dict[str, Any]:
        """Get the prompts configuration
        
        Args:
            refresh: Whether to refresh the cached configuration
            
        Returns:
            Dictionary containing the prompts
        """
        if "prompts" not in self.config_cache or refresh:
            file_path = os.path.join(self.config_dir, "prompts.yaml")
            self.config_cache["prompts"] = self._load_yaml(file_path)
        return self.config_cache["prompts"]
    
    def get_params(self, refresh: bool = False) -> Dict[str, Any]:
        """Get the parameters configuration
        
        Args:
            refresh: Whether to refresh the cached configuration
            
        Returns:
            Dictionary containing the parameters
        """
        if "params" not in self.config_cache or refresh:
            file_path = os.path.join(self.config_dir, "params.yaml")
            self.config_cache["params"] = self._load_yaml(file_path)
        return self.config_cache["params"]
    
    def get_schema(self, refresh: bool = False) -> Dict[str, Any]:
        """Get the schema configuration
        
        Args:
            refresh: Whether to refresh the cached configuration
            
        Returns:
            Dictionary containing the schema
        """
        if "schema" not in self.config_cache or refresh:
            file_path = os.path.join(self.config_dir, "schema.yaml")
            self.config_cache["schema"] = self._load_yaml(file_path)
        return self.config_cache["schema"]
    
    def get_default_questions(self) -> list:
        """Get the default questions from the parameters
        
        Returns:
            List of default questions
        """
        params = self.get_params()
        return params.get("default_questions", [])
    
    def get_agent_params(self) -> Dict[str, Any]:
        """Get the agent parameters
        
        Returns:
            Dictionary containing agent parameters
        """
        params = self.get_params()
        return params.get("agent_params", {})
    
    def get_system_prompt(self, agent_type: str) -> Optional[str]:
        """Get a system prompt for a specific agent type
        
        Args:
            agent_type: Type of agent (e.g., default_questions_agent)
            
        Returns:
            System prompt string or None if not found
        """
        prompts = self.get_prompts()
        agent_config = prompts.get(agent_type, {})
        return agent_config.get("system_prompt")