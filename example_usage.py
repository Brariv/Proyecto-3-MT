"""
Example demonstrating various ways to use the TuringMachineConfig class.
"""

from yaml_reader import TuringMachineConfig


def example_basic_usage():
    """Basic usage example."""
    print("="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Create config object and load
    tm_config = TuringMachineConfig('turing_machine_config.yaml')
    tm_config.load_config()
    
    # Print formatted configuration
    tm_config.print_config()


def example_accessing_specific_data():
    """Example of accessing specific configuration data."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Accessing Specific Data")
    print("="*60)
    
    tm_config = TuringMachineConfig('turing_machine_config.yaml')
    tm_config.load_config()
    
    # Get specific information
    print(f"\nNumber of states: {len(tm_config.get_state_list())}")
    print(f"Alphabet size: {len(tm_config.get_alphabet())}")
    print(f"Tape alphabet size: {len(tm_config.get_tape_alphabet())}")
    print(f"Number of transitions: {len(tm_config.get_delta())}")
    print(f"Number of test strings: {len(tm_config.get_simulation_strings())}")


def example_transition_analysis():
    """Example of analyzing transitions."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Analyzing Transitions")
    print("="*60)
    
    tm_config = TuringMachineConfig('turing_machine_config.yaml')
    tm_config.load_config()
    
    # Count transitions by displacement direction
    transitions = tm_config.get_delta()
    left_count = sum(1 for t in transitions if t['output']['tape_displacement'] == 'L')
    right_count = sum(1 for t in transitions if t['output']['tape_displacement'] == 'R')
    stay_count = sum(1 for t in transitions if t['output']['tape_displacement'] == 'S')
    
    print(f"\nTransition directions:")
    print(f"  Left (L): {left_count}")
    print(f"  Right (R): {right_count}")
    print(f"  Stay (S): {stay_count}")
    
    # Show transitions from initial state
    initial_state = tm_config.get_initial_state()
    initial_transitions = [t for t in transitions 
                          if t['params']['initial_state'] == initial_state]
    
    print(f"\nTransitions from initial state '{initial_state}':")
    for i, t in enumerate(initial_transitions, 1):
        params = t['params']
        output = t['output']
        print(f"  {i}. Read '{params['tape_input']}' → "
              f"Write '{output['tape_output']}', "
              f"Move {output['tape_displacement']}, "
              f"Go to state {output['final_state']}")


if __name__ == "__main__":
    example_basic_usage()
    example_accessing_specific_data()
    example_transition_analysis()
