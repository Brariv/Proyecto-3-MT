"""
Turing Machine YAML Configuration Reader

This module provides functionality to read and parse Turing Machine 
configurations from YAML files.
"""

import yaml
from typing import  Any
from pathlib import Path


class TuringMachineConfig:
 
    
    def __init__(self, yaml_file_path: str):
       
        self.yaml_file_path = Path(yaml_file_path)
        self.config = None
        self.q_states = None
        self.alphabet = None
        self.tape_alphabet = None
        self.delta = None
        self.simulation_strings = None
        
    def load_config(self) -> dict[str, Any]:
        
        if not self.yaml_file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {self.yaml_file_path}")
        
        with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
        
        # Parse individual sections
        self._parse_config()
        
        return self.config
    
    def _parse_config(self):
        if self.config:
            self.q_states = self.config.get('q_states', {})
            self.alphabet = self.config.get('alphabet', [])
            self.tape_alphabet = self.config.get('tape_alphabet', [])
            self.delta = self.config.get('delta', [])
            self.simulation_strings = self.config.get('simulation_strings', [])
    
    def get_states(self) -> dict[str, Any]:
        
        return self.q_states
    
    def get_state_list(self) -> list[str]:
        return self.q_states.get('q_list', []) if self.q_states else []
    
    def get_initial_state(self) -> str:
        
        return self.q_states.get('initial', '') if self.q_states else ''
    
    def get_final_state(self) -> str:
        
        return self.q_states.get('final', '') if self.q_states else ''
    
    def get_alphabet(self) -> list[str]:
                return self.alphabet
    
    def get_tape_alphabet(self) -> list[str]:
                return self.tape_alphabet
    
    def get_delta(self) -> list[dict[str, Any]]:
        
        return self.delta
    
    def get_simulation_strings(self) -> list[str]:
                return self.simulation_strings
    
    def print_config(self):
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



