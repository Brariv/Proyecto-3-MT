"""
Turing Machine YAML Configuration Reader

This module provides functionality to read and parse Turing Machine 
configurations from YAML files.
"""

import yaml
from typing import  Any
from pathlib import Path


class TuringMachineConfig:
    """
    A class to read and manage Turing Machine configurations from YAML files.
    
    The YAML structure should contain:
    - q_states: States configuration (list, initial, final)
    - alphabet: List of alphabet symbols
    - tape_alphabet: List of tape alphabet symbols (includes alphabet symbols)
    - delta: Transition function with params and outputs
    - simulation_strings: Strings to test the Turing Machine
    """
    
    def __init__(self, yaml_file_path: str):
        """
        Initialize the TuringMachineConfig with a YAML file.
        
        Args:
            yaml_file_path (str): Path to the YAML configuration file
        """
        self.yaml_file_path = Path(yaml_file_path)
        self.config = None
        self.q_states = None
        self.alphabet = None
        self.tape_alphabet = None
        self.delta = None
        self.simulation_strings = None
        
    def load_config(self) -> dict[str, Any]:
        """
        Load the YAML configuration file.
        
        Returns:
            Dict[str, Any]: The parsed YAML configuration
            
        Raises:
            FileNotFoundError: If the YAML file doesn't exist
            yaml.YAMLError: If the YAML file is malformed
        """
        if not self.yaml_file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {self.yaml_file_path}")
        
        with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
        
        # Parse individual sections
        self._parse_config()
        
        return self.config
    
    def _parse_config(self):
        """Parse the configuration sections into class attributes."""
        if self.config:
            self.q_states = self.config.get('q_states', {})
            self.alphabet = self.config.get('alphabet', [])
            self.tape_alphabet = self.config.get('tape_alphabet', [])
            self.delta = self.config.get('delta', [])
            self.simulation_strings = self.config.get('simulation_strings', [])
    
    def get_states(self) -> dict[str, Any]:
        """
        Get the states configuration.
        
        Returns:
            Dict[str, Any]: Dictionary containing q_list, initial, and final states
        """
        return self.q_states
    
    def get_state_list(self) -> list[str]:
        """
        Get the list of states.
        
        Returns:
            List[str]: List of state identifiers
        """
        return self.q_states.get('q_list', []) if self.q_states else []
    
    def get_initial_state(self) -> str:
        """
        Get the initial state.
        
        Returns:
            str: Initial state identifier
        """
        return self.q_states.get('initial', '') if self.q_states else ''
    
    def get_final_state(self) -> str:
        """
        Get the final state.
        
        Returns:
            str: Final state identifier
        """
        return self.q_states.get('final', '') if self.q_states else ''
    
    def get_alphabet(self) -> list[str]:
        """
        Get the alphabet symbols.
        
        Returns:
            List[str]: List of alphabet symbols
        """
        return self.alphabet
    
    def get_tape_alphabet(self) -> list[str]:
        """
        Get the tape alphabet symbols.
        
        Returns:
            List[str]: List of tape alphabet symbols
        """
        return self.tape_alphabet
    
    def get_delta(self) -> list[dict[str, Any]]:
        """
        Get the transition function (delta).
        
        Returns:
            List[Dict[str, Any]]: List of transitions with params and outputs
        """
        return self.delta
    
    def get_simulation_strings(self) -> list[str]:
        """
        Get the simulation strings.
        
        Returns:
            List[str]: List of strings to simulate
        """
        return self.simulation_strings
    
    def print_config(self):
        """Print a formatted summary of the configuration."""
        if not self.config:
            print("No configuration loaded. Please call load_config() first.")
            return
        
        print("=" * 60)
        print("TURING MACHINE CONFIGURATION")
        print("=" * 60)
        
        print("\n--- STATES ---")
        print(f"State list: {self.get_state_list()}")
        print(f"Initial state: {self.get_initial_state()}")
        print(f"Final state: {self.get_final_state()}")
        
        print("\n--- ALPHABET ---")
        print(f"Alphabet: {self.get_alphabet()}")
        
        print("\n--- TAPE ALPHABET ---")
        print(f"Tape alphabet: {self.get_tape_alphabet()}")
        
        print("\n--- DELTA (Transition Function) ---")
        for i, transition in enumerate(self.get_delta(), 1):
            params = transition.get('params', {})
            output = transition.get('output', {})
            print(f"\nTransition {i}:")
            print(f"  Input:  ({params.get('initial_state')}, "
                  f"{params.get('mem_cache_value')}, "
                  f"{params.get('tape_input')})")
            print(f"  Output: ({output.get('final_state')}, "
                  f"{output.get('mem_cache_value')}, "
                  f"{output.get('tape_output')}, "
                  f"{output.get('tape_displacement')})")
        
        print("\n--- SIMULATION STRINGS ---")
        for i, string in enumerate(self.get_simulation_strings(), 1):
            print(f"{i}. {string}")
        
        print("\n" + "=" * 60)



