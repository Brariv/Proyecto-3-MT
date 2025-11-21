from argparse import ArgumentParser, Namespace

# function for getting arguments from cli
def parseLexerArgs() -> Namespace:
    parser = ArgumentParser()
    
    # I don't want to input my string, this flow is cleaner, like DUH
    parser.add_argument("--tm_config_file", dest="tm_config_file", type=str, help="Add the turing machine file")
    parser.add_argument("--validator_mode", dest="validator_mode", type=bool, help="enter validator mode")

    parse_args = parser.parse_args()

    if parse_args.tm_config_file is None or parse_args.validator_mode is None:
        raise Exception("Arguments where not suplly")

    return parse_args



