class TuringMachine:
    def __init__(self, config):
        self.config = config
        self.states = set(config.get_state_list())
        self.initial_state = config.get_initial_state()
        self.final_state = config.get_final_state()
        self.transitions = config.get_delta()
        self.alphabet = set(config.get_alphabet())
        self.tape_alphabet = list(config.get_tape_alphabet())

        # --- Blank symbol: prefer explicit config, luego heurística (B, _), luego último de tape_alphabet
        self.blank_symbol = getattr(config, "blank_symbol", None)
        if not self.blank_symbol:
            if "B" in self.tape_alphabet:
                self.blank_symbol = "B"
            elif "_" in self.tape_alphabet:
                self.blank_symbol = "_"
            else:
                # fallback: last element of tape_alphabet
                self.blank_symbol = self.tape_alphabet[-1]

        # --- mem_cache initial: prefer explicit config, luego heurística sobre transiciones del estado inicial
        self.mem_cache_initial = getattr(config, "mem_cache_initial", None)
        if not self.mem_cache_initial:
            candidates = {
                entry["params"]["mem_cache_value"]
                for entry in self.transitions
                if entry["params"]["initial_state"] == self.initial_state
            }
            # prefer blank-like candidate if present
            if "B" in candidates:
                self.mem_cache_initial = "B"
            elif self.blank_symbol in candidates:
                self.mem_cache_initial = self.blank_symbol
            elif len(candidates) > 0:
                # take an arbitrary candidate (deterministic)
                self.mem_cache_initial = sorted(candidates)[0]
            else:
                # ultimate fallback: use blank_symbol
                self.mem_cache_initial = self.blank_symbol

        # Build transition lookup dict for fast simulation
        self.delta_map: dict[tuple[str, str, str], dict[str, str]] = {}
        self._build_transition_map()

    def _build_transition_map(self):
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

    def _tape_to_string(self, tape_dict):
        """Construye una representación minimal de la cinta desde el primer al último
        índice presente en tape_dict, rellenando con blank cuando falte."""
        if not tape_dict:
            return ""
        min_i = min(tape_dict.keys())
        max_i = max(tape_dict.keys())
        return "".join(tape_dict.get(i, self.blank_symbol) for i in range(min_i, max_i + 1))

    def simulate(self, input_str: str, max_steps: int = 10000):
        # Representamos la cinta como un diccionario index -> símbolo (permite índices negativos)
        tape = {}
        for i, ch in enumerate(input_str):
            tape[i] = ch

        head = 0
        state = self.initial_state
        mem_cache = self.mem_cache_initial

        trace = []

        for step in range(max_steps):
            symbol = tape.get(head, self.blank_symbol)
            trace.append((step, state, head, self._tape_to_string(tape), mem_cache))

            # aceptamos si estamos en el estado final
            if state == self.final_state:
                return True, self._tape_to_string(tape), trace

            key = (state, mem_cache, symbol)
            if key not in self.delta_map:
                # No hay transición; máquina rechaza
                return False, self._tape_to_string(tape), trace

            out = self.delta_map[key]

            # Aplicar efectos de la transición
            state = out["final_state"]
            mem_cache = out["mem_cache_value"]
            print("Mem cache now:", mem_cache)
            tape[head] = out["tape_output"]
            print("Tape now:", self._tape_to_string(tape))
            

            # Movimiento del cabezal
            move = out["tape_displacement"]
            if move == "L":
                head -= 1
            elif move == "R":
                head += 1
            elif move == "S":
                pass
            else:
                # seguridad en caso de valor inválido
                raise TMSimulationError(f"Invalid tape displacement: {move}")

        # Si se acaban los pasos, consideramos que no aceptó
        return False, self._tape_to_string(tape), trace

