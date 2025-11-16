# Turing Machine YAML Configuration Reader

This project provides a Python tool to read and parse Turing Machine configurations from YAML files.

## Files

- `yaml_reader.py`: Python module for reading and parsing YAML configurations
- `turing_machine_config.yaml`: Example YAML configuration file for a Turing Machine

## YAML Structure

The YAML file should follow this structure:

```yaml
---
# Lista de estados
q_states:
  q_list:
    - 'lista de estados de la MT'
    - ...
  initial: '0'
  final: '5'

alphabet:
  - 'lista de símbolos del alfabeto'
  - ...

tape_alphabet:
  - 'lista de símbolos del alfabeto de la cinta'
  - 'recuerde que incluye los símbolos de alphabet también'
  - ...

delta:
- params:
    initial_state: 'estado en el que inicia'
    mem_cache_value: 'Puede ser blank o contener algo'
    tape_input: 'el input leído sobre la cinta'
  output:
    final_state: 'estado en el que termina'
    mem_cache_value: 'Puede ser blank o contener algo'
    tape_output: 'el resultado sobre la cinta'
    tape_displacement: 'desplazamiento sobre la cinta, puede ser L, R o S'

simulation_strings:
  - 'string1'
  - 'string2'
  - ...
```

## Usage

### Basic Usage

Run the script directly to see the example configuration:

```bash
python yaml_reader.py
```

### Using in Your Code

```python
from yaml_reader import TuringMachineConfig

# Load configuration
tm_config = TuringMachineConfig('turing_machine_config.yaml')
tm_config.load_config()

# Access configuration elements
states = tm_config.get_state_list()
initial = tm_config.get_initial_state()
final = tm_config.get_final_state()
alphabet = tm_config.get_alphabet()
tape_alphabet = tm_config.get_tape_alphabet()
transitions = tm_config.get_delta()
test_strings = tm_config.get_simulation_strings()

# Print formatted configuration
tm_config.print_config()
```

### Available Methods

- `load_config()`: Load and parse the YAML file
- `get_states()`: Get the complete states configuration
- `get_state_list()`: Get the list of states
- `get_initial_state()`: Get the initial state
- `get_final_state()`: Get the final state
- `get_alphabet()`: Get the alphabet symbols
- `get_tape_alphabet()`: Get the tape alphabet symbols
- `get_delta()`: Get the transition function
- `get_simulation_strings()`: Get the simulation strings
- `print_config()`: Print a formatted summary of the configuration

## Requirements

- Python 3.6+
- PyYAML

Install dependencies:

```bash
pip install pyyaml
```

## Example Output

When you run `python yaml_reader.py`, you'll see:

```
============================================================
TURING MACHINE CONFIGURATION
============================================================

--- STATES ---
State list: ['0', '1', '2', '3', '4', '5']
Initial state: 0
Final state: 5

--- ALPHABET ---
Alphabet: ['a', 'b', '#']

--- TAPE ALPHABET ---
Tape alphabet: ['a', 'b', '#', 'X', 'Y', '_']

--- DELTA (Transition Function) ---

Transition 1:
  Input:  (0, blank, a)
  Output: (1, a, X, R)

[... additional transitions ...]

--- SIMULATION STRINGS ---
1. aab#aab
2. ab#ab
3. abbababa#aba

============================================================
```
