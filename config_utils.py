"""
config_utils.py
---------------
Utility for managing configuration settings for the Learning Agent.

Provides a ConfigManager class that loads settings from a YAML file,
merges them with default values, and allows for easy access and 
in-memory updates to configuration parameters.
"""

import os
import yaml
from rich import print as rprint
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Manages configuration loading and access.
    
    Loads configuration from a YAML file specified by `CONFIG_PATH`.
    If the file is not found or an error occurs during loading, it falls back 
    to `DEFAULT_CONFIG`. User-defined configurations in the YAML file 
    override the default values.
    """
    
    CONFIG_PATH: str = "config.yaml"
    DEFAULT_CONFIG: Dict[str, Any] = {
        "model": "qwen3:4b",
        "model_provider": "ollama",
        "openrouter_model": "deepseek/deepseek-prover-v2:free",
        "temperature": 0.3,
        "use_memory": True,
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "top_k": 5,
        "similarity_threshold": 0.5,
        "chunk_size": 2000,
        "chunk_overlap": 200,
        "use_web_fallback": True,
        "web_results": 3,
        "collection": "kb",
        "prompt_template": "Answer the question based on the following context. \nIf you don't know the answer, just say you don't know; don't make up information.\n\nContext:\n{context}\n\nQuestion: {question}\n",
        # UI settings - new LaTeX processing keys
        "use_markdown_rendering": True,  # Enable/disable markdown rendering in chat (existing, added here for completeness)
        "enable_latex_processing": True,  # Enable/disable LaTeX processing in chat
        "use_advanced_latex_rendering": True, # Enable/disable advanced LaTeX to text/markup rendering
        "code_highlighting": True  # Enable/disable syntax highlighting for code blocks (existing, added here for completeness)
    }
    
    def __init__(self) -> None:
        self.config: Dict[str, Any] = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Loads configuration from the YAML file defined by `CONFIG_PATH`.
        
        If the file is not found, it returns `DEFAULT_CONFIG`.
        If the file exists, it loads the YAML content and merges it with
        `DEFAULT_CONFIG`, where values from the user's YAML file take
        precedence over default values.
        If an error occurs during file reading or YAML parsing, it prints an
        error message and returns `DEFAULT_CONFIG`.

        Returns:
            Dict[str, Any]: The loaded (and merged) configuration dictionary.
        """
        if not os.path.exists(self.CONFIG_PATH):
            rprint(f"[yellow]⚠️ Config file '{self.CONFIG_PATH}' not found. Using default configuration.[/yellow]")
            return self.DEFAULT_CONFIG.copy() # Return a copy to prevent modification of defaults

        try:
            with open(self.CONFIG_PATH, "r") as f:
                user_config = yaml.safe_load(f)
                
                # Merge DEFAULT_CONFIG with user_config. User_config values take precedence.
                # Ensure user_config is a dict before merging to avoid errors if YAML is empty/malformed.
                if isinstance(user_config, dict):
                    merged_config = {**self.DEFAULT_CONFIG, **user_config}
                    rprint(f"[green]✅ Loaded configuration from '{self.CONFIG_PATH}'.[/green]")
                    return merged_config
                else:
                    rprint(f"[yellow]⚠️ Config file '{self.CONFIG_PATH}' is empty or not valid YAML. Using default configuration.[/yellow]")
                    return self.DEFAULT_CONFIG.copy()
        except yaml.YAMLError as e_yaml:
            rprint(f"[red]❌ Error parsing YAML in config file '{self.CONFIG_PATH}': {e_yaml}[/red]")
            rprint("[yellow]⚠️ Using default configuration due to parsing error.[/yellow]")
            return self.DEFAULT_CONFIG.copy()
        except IOError as e_io:
            rprint(f"[red]❌ Error reading config file '{self.CONFIG_PATH}': {e_io}[/red]")
            rprint("[yellow]⚠️ Using default configuration due to I/O error.[/yellow]")
            return self.DEFAULT_CONFIG.copy()
        except Exception as e: # Catch-all for other unexpected errors
            rprint(f"[red]❌ Unexpected error loading config file '{self.CONFIG_PATH}': {e}[/red]")
            rprint("[yellow]⚠️ Using default configuration due to unexpected error.[/yellow]")
            return self.DEFAULT_CONFIG.copy()
    
    def get(self, key: str, default: Optional[Any] = None) -> Any: # Changed default to Optional[Any]
        """
        Retrieves a configuration value for the given key.

        Args:
            key (str): The configuration key to retrieve.
            default (Optional[Any], optional): The default value to return if the key 
                                             is not found. Defaults to None.

        Returns:
            Any: The value associated with the key, or the default value if not found.
        """
        return self.config.get(key, default)
    
    def update(self, key: str, value: Any) -> None:
        """
        Updates a configuration value in memory for the current session.
        This does not write the change back to the config file.

        Args:
            key (str): The configuration key to update.
            value (Any): The new value for the key.
        """
        self.config[key] = value
        rprint(f"[cyan]🔄 Config value for '{key}' updated to: {value} (in memory)[/cyan]")


if __name__ == '__main__':
    # This block demonstrates example usage and basic testing of ConfigManager.
    
    rprint("[bold cyan]🧪 Running ConfigManager Test Suite...[/bold cyan]")

    # Test 1: Initialization and default values
    rprint("\n[b]Test 1: Initialization and default values[/b]")
    manager = ConfigManager()
    rprint("Default Model:", manager.get("model"))
    rprint("Default Temperature:", manager.get("temperature"))
    rprint("Non-existent key (expected default None):", manager.get("some_random_key"))
    rprint("Non-existent key (with provided default):", manager.get("another_random_key", "my_default"))

    # Test 2: Update method
    rprint("\n[b]Test 2: Update method[/b]")
    manager.update("model", "gpt-4-test")
    rprint("Updated Model:", manager.get("model"))
    manager.update("temperature", 0.99)
    rprint("Updated Temperature:", manager.get("temperature"))

    # Test 3: Loading from a dummy config file
    rprint("\n[b]Test 3: Loading from a dummy config file[/b]")
    DUMMY_CONFIG_PATH = "dummy_test_config.yaml"
    dummy_data = {
        "model": "dummy_model_from_file", 
        "new_setting": "custom_value",
        "temperature": 0.55 # Override default
    }
    try:
        with open(DUMMY_CONFIG_PATH, "w") as f:
            yaml.dump(dummy_data, f)
        rprint(f"Created dummy config file: {DUMMY_CONFIG_PATH}")

        original_actual_config_path = ConfigManager.CONFIG_PATH
        ConfigManager.CONFIG_PATH = DUMMY_CONFIG_PATH  # Temporarily change path for test
        
        dummy_manager = ConfigManager() # This will load dummy_test_config.yaml
        
        rprint("Model from dummy file:", dummy_manager.get("model")) # Expected: dummy_model_from_file
        rprint("New setting from dummy file:", dummy_manager.get("new_setting")) # Expected: custom_value
        rprint("Temperature (overridden by dummy file):", dummy_manager.get("temperature")) # Expected: 0.55
        rprint("Collection (from default config, not in dummy):", dummy_manager.get("collection")) # Expected: kb
        
    except Exception as e:
        rprint(f"[red]Error during dummy config test: {e}[/red]")
    finally:
        if os.path.exists(DUMMY_CONFIG_PATH):
            os.remove(DUMMY_CONFIG_PATH)
            rprint(f"Cleaned up dummy config file: {DUMMY_CONFIG_PATH}")
        ConfigManager.CONFIG_PATH = original_actual_config_path # Reset to original
        rprint(f"Restored CONFIG_PATH to: {ConfigManager.CONFIG_PATH}")

    # Test 4: Handling non-existent config file (already covered by initial load if config.yaml doesn't exist)
    rprint("\n[b]Test 4: Handling non-existent config file[/b]")
    original_config_path_for_non_existent_test = ConfigManager.CONFIG_PATH
    ConfigManager.CONFIG_PATH = "non_existent_config.yaml"
    non_existent_manager = ConfigManager() # Should print warning and use defaults
    rprint("Model (non-existent file, default):", non_existent_manager.get("model"))
    ConfigManager.CONFIG_PATH = original_config_path_for_non_existent_test # Reset

    # Test 5: Handling empty or malformed config file
    rprint("\n[b]Test 5: Handling empty config file[/b]")
    EMPTY_CONFIG_PATH = "empty_test_config.yaml"
    try:
        with open(EMPTY_CONFIG_PATH, "w") as f:
            f.write("") # Create an empty file
        original_config_path_for_empty_test = ConfigManager.CONFIG_PATH
        ConfigManager.CONFIG_PATH = EMPTY_CONFIG_PATH
        empty_manager = ConfigManager() # Should warn and use defaults
        rprint("Model (empty file, default):", empty_manager.get("model"))
    finally:
        if os.path.exists(EMPTY_CONFIG_PATH):
            os.remove(EMPTY_CONFIG_PATH)
        ConfigManager.CONFIG_PATH = original_config_path_for_empty_test

    rprint("\n[bold cyan]✅ ConfigManager Test Suite Complete.[/bold cyan]")
