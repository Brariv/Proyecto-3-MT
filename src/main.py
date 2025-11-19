import yaml
from turing_machine import TuringMachineConfig


if __name__ == "__main__":
    config_file = 'files/turing_machine_config.yaml'
    
    try:
        tm_config = TuringMachineConfig(config_file)
        tm_config.load_config()
        tm_config.print_config()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


