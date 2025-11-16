"""
Test script for TuringMachineConfig class
"""

from yaml_reader import TuringMachineConfig


def test_yaml_reader():
    """Test the YAML reader functionality."""
    print("Running tests for TuringMachineConfig...")
    
    # Test 1: Load configuration
    print("\n[TEST 1] Loading configuration...")
    tm_config = TuringMachineConfig('turing_machine_config.yaml')
    config = tm_config.load_config()
    assert config is not None, "Configuration should not be None"
    print("✓ Configuration loaded successfully")
    
    # Test 2: Get state list
    print("\n[TEST 2] Checking state list...")
    states = tm_config.get_state_list()
    assert isinstance(states, list), "States should be a list"
    assert len(states) > 0, "States list should not be empty"
    assert '0' in states, "Initial state '0' should be in state list"
    assert '5' in states, "Final state '5' should be in state list"
    print(f"✓ State list contains {len(states)} states: {states}")
    
    # Test 3: Get initial and final states
    print("\n[TEST 3] Checking initial and final states...")
    initial = tm_config.get_initial_state()
    final = tm_config.get_final_state()
    assert initial == '0', f"Initial state should be '0', got '{initial}'"
    assert final == '5', f"Final state should be '5', got '{final}'"
    print(f"✓ Initial state: {initial}, Final state: {final}")
    
    # Test 4: Get alphabet
    print("\n[TEST 4] Checking alphabet...")
    alphabet = tm_config.get_alphabet()
    assert isinstance(alphabet, list), "Alphabet should be a list"
    assert 'a' in alphabet, "Symbol 'a' should be in alphabet"
    assert 'b' in alphabet, "Symbol 'b' should be in alphabet"
    assert '#' in alphabet, "Symbol '#' should be in alphabet"
    print(f"✓ Alphabet: {alphabet}")
    
    # Test 5: Get tape alphabet
    print("\n[TEST 5] Checking tape alphabet...")
    tape_alphabet = tm_config.get_tape_alphabet()
    assert isinstance(tape_alphabet, list), "Tape alphabet should be a list"
    assert len(tape_alphabet) >= len(alphabet), "Tape alphabet should include alphabet symbols"
    print(f"✓ Tape alphabet: {tape_alphabet}")
    
    # Test 6: Get delta (transition function)
    print("\n[TEST 6] Checking delta transitions...")
    delta = tm_config.get_delta()
    assert isinstance(delta, list), "Delta should be a list"
    assert len(delta) > 0, "Delta should contain transitions"
    
    # Verify first transition structure
    first_transition = delta[0]
    assert 'params' in first_transition, "Transition should have 'params'"
    assert 'output' in first_transition, "Transition should have 'output'"
    
    params = first_transition['params']
    assert 'initial_state' in params, "Params should have 'initial_state'"
    assert 'mem_cache_value' in params, "Params should have 'mem_cache_value'"
    assert 'tape_input' in params, "Params should have 'tape_input'"
    
    output = first_transition['output']
    assert 'final_state' in output, "Output should have 'final_state'"
    assert 'mem_cache_value' in output, "Output should have 'mem_cache_value'"
    assert 'tape_output' in output, "Output should have 'tape_output'"
    assert 'tape_displacement' in output, "Output should have 'tape_displacement'"
    
    print(f"✓ Delta contains {len(delta)} transitions")
    
    # Test 7: Get simulation strings
    print("\n[TEST 7] Checking simulation strings...")
    sim_strings = tm_config.get_simulation_strings()
    assert isinstance(sim_strings, list), "Simulation strings should be a list"
    assert len(sim_strings) > 0, "Should have at least one simulation string"
    assert 'aab#aab' in sim_strings, "Should contain example string 'aab#aab'"
    print(f"✓ Simulation strings: {sim_strings}")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60)


def test_file_not_found():
    """Test handling of missing file."""
    print("\n[TEST 8] Testing file not found handling...")
    try:
        tm_config = TuringMachineConfig('nonexistent.yaml')
        tm_config.load_config()
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"✓ Correctly raised FileNotFoundError: {e}")


if __name__ == "__main__":
    test_yaml_reader()
    test_file_not_found()
