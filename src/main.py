import yaml
from turing_machine.simulator import TuringMachine
from turing_machine.config import TuringMachineConfig
from utils.arg_parsing import parseLexerArgs


if __name__ == "__main__":

    parse_args = parseLexerArgs()
    
    try:
        tm_config = TuringMachineConfig(parse_args.tm_config_file)
        tm_config.load_config()
        tm_config.print_config()
        
        tm = TuringMachine(tm_config)

        for string in tm_config.get_simulation_strings():
            accepted, final_tape, trace = tm.simulate(string)

            print(f"Input: {string}")
            print(f"Final Tape: {final_tape}")
            print("Steps:", len(trace), "\n")
            
            if parse_args.validator_mode:
                print("Is it valid?")
                print(accepted, "\n")


    except FileNotFoundError as e:
        print(f"Error: {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


