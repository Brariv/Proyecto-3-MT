
class TMSimulationError(Exception):
    """Raised when the Turing Machine encounters an invalid configuration or operation."""
    pass


class TuringMachine:
    """
    A simulator for the Turing Machine defined by TuringMachineConfig.
    Supports mem_cache_value + tape input as transition keys.
    """

    def __init__(self, config):
        self.config = config
        self.states = set(config.get_state_list())
        self.initial_state = config.get_initial_state()
        self.final_state = config.get_final_state()
        self.transitions = config.get_delta()
        self.alphabet = set(config.get_alphabet())
        self.tape_alphabet = set(config.get_tape_alphabet())

        # Build transition lookup dict for fast simulation
        self.delta_map: dict[tuple[str, str, str], dict[str, str]] = {}
        self._build_transition_map()

    def _build_transition_map(self):
        """
        Convert delta entries into a fast lookup table:
            (state, mem_val, tape_symbol) → output_dict
        Also detect duplicate/conflicting transitions.
        """
        for entry in self.transitions:
            params = entry["params"]
            output = entry["output"]

            key = (
                params["initial_state"],
                params["mem_cache_value"],
                params["tape_input"],
            )

            if key in self.delta_map:
                raise TMSimulationError(f"Duplicate transition found for key {key}")

            self.delta_map[key] = output

    def validate(self) -> bool:
        """Validate states, symbols, and transitions."""

        # Check initial + final
        if self.initial_state not in self.states:
            raise TMSimulationError(f"Initial state {self.initial_state} not in state list.")
        if self.final_state not in self.states:
            raise TMSimulationError(f"Final state {self.final_state} not in state list.")

        # Validate transitions
        for key, output in self.delta_map.items():
            state, mem_val, tape_in = key

            if state not in self.states:
                raise TMSimulationError(f"Transition uses undefined state: {state}")

            if tape_in not in self.tape_alphabet:
                raise TMSimulationError(f"Transition uses undefined tape symbol: {tape_in}")

            fs = output["final_state"]
            if fs not in self.states:
                raise TMSimulationError(f"Transition goes to undefined state: {fs}")

            if output["tape_output"] not in self.tape_alphabet:
                raise TMSimulationError(
                    f"Output symbol {output['tape_output']} not in tape alphabet"
                )

            if output["tape_displacement"] not in ("L", "R", "S"):
                raise TMSimulationError(
                    f"Invalid displacement: {output['tape_displacement']}"
                )

        return True

    def simulate(self, input_str: str, max_steps: int = 10000):
        """
        Run the TM on a given input string.
        Returns:
            accepted: bool
            final_tape: str
            trace: list of (state, head_pos, tape_snapshot, mem_cache)
        """

        tape = list(input_str)
        head = 0
        state = self.initial_state
        mem_cache = "blank"

        trace = []

        # Ensure tape has infinite blanks to the right
        def ensure_tape(i):
            if i >= len(tape):
                tape.extend(["_"] * (i - len(tape) + 1))

        for step in range(max_steps):
            ensure_tape(head)
            symbol = tape[head]

            trace.append((state, head, "".join(tape), mem_cache))

            if state == self.final_state:
                return True, "".join(tape), trace

            key = (state, mem_cache, symbol)
            if key not in self.delta_map:
                return False, "".join(tape), trace

            out = self.delta_map[key]

            # Apply transition
            state = out["final_state"]
            mem_cache = out["mem_cache_value"]
            tape[head] = out["tape_output"]

            # Move head
            move = out["tape_displacement"]
            if move == "L":
                head = max(0, head - 1)
            elif move == "R":
                head += 1

        # Exceeded step limit
        return False, "".join(tape), trace
