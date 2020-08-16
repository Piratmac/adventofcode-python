class IntCode:
    # Verbosity
    verbose_level = 0

    # Count of parameters per opcode
    instr_length = {
        "01": 4,
        "02": 4,
        "03": 2,
        "04": 2,
        "05": 3,
        "06": 3,
        "07": 4,
        "08": 4,
        "09": 2,
        "99": 1,
    }

    def __init__(self, instructions, reference=""):
        self.instructions = list(map(int, instructions.split(",")))
        self.reference = reference

        # Current state
        self.pointer = 0
        self.state = "Running"
        self.relative_base = 0

        # Current instruction modes
        self.modes = "000"

        # Inputs and outputs
        self.inputs = []
        self.all_inputs = []
        self.outputs = []

    def reset(self, instructions):
        self.instructions = list(map(int, instructions.split(",")))
        self.pointer = 0
        self.state = "Running"

    def restart(self):
        self.state = "Running"

    def add_input(self, value):
        try:
            self.inputs += value
            self.all_inputs += value
        except:
            self.inputs.append(value)
            self.all_inputs.append(value)

    def get_opcode(self):
        instr = self.instructions[self.pointer]
        opcode_full = "0" * (5 - len(str(instr))) + str(instr)
        return opcode_full

    def get_instruction(self, opcode):
        return self.instructions[
            self.pointer : self.pointer + self.instr_length[opcode]
        ]

    def get_value(self, param_position):
        assert self.modes[2 - (param_position - 1)] in "012"
        try:
            if self.modes[2 - (param_position - 1)] == "0":
                return self.instructions[
                    self.instructions[self.pointer + param_position]
                ]
            elif self.modes[2 - (param_position - 1)] == "1":
                return self.instructions[self.pointer + param_position]
            else:
                return self.instructions[
                    self.relative_base
                    + self.instructions[self.pointer + param_position]
                ]
        except:
            return 0

    def set_value(self, param_position, value):
        assert self.modes[2 - (param_position - 1)] in "02"
        if self.modes[2 - (param_position - 1)] == "0":
            try:
                self.instructions[
                    self.instructions[self.pointer + param_position]
                ] = value
            except:
                self.instructions += [0] * (
                    self.instructions[self.pointer + param_position]
                    - len(self.instructions)
                    + 1
                )
                self.instructions[
                    self.instructions[self.pointer + param_position]
                ] = value
        else:
            try:
                self.instructions[
                    self.relative_base
                    + self.instructions[self.pointer + param_position]
                ] = value
            except:
                self.instructions += [0] * (
                    self.relative_base
                    + self.instructions[self.pointer + param_position]
                    - len(self.instructions)
                    + 1
                )
                self.instructions[
                    self.relative_base
                    + self.instructions[self.pointer + param_position]
                ] = value

    def op_01(self, instr):
        self.set_value(3, self.get_value(1) + self.get_value(2))
        self.pointer += self.instr_length["01"]
        self.state = "Running"

    def op_02(self, instr):
        self.set_value(3, self.get_value(1) * self.get_value(2))
        self.pointer += self.instr_length["02"]
        self.state = "Running"

    def op_03(self, instr):
        if len(self.inputs) == 0:
            self.state = "Paused"
            return
        self.set_value(1, self.inputs.pop(0))
        self.pointer += self.instr_length["03"]
        self.state = "Running"

    def op_04(self, instr):
        self.outputs.append(self.get_value(1))
        self.pointer += self.instr_length["04"]
        self.state = "Running"

    def op_05(self, instr):
        if self.get_value(1) != 0:
            self.pointer = self.get_value(2)
        else:
            self.pointer += self.instr_length["05"]
        self.state = "Running"

    def op_06(self, instr):
        if self.get_value(1) == 0:
            self.pointer = self.get_value(2)
        else:
            self.pointer += self.instr_length["06"]
        self.state = "Running"

    def op_07(self, instr):
        if self.get_value(1) < self.get_value(2):
            self.set_value(3, 1)
        else:
            self.set_value(3, 0)
        self.pointer += self.instr_length["07"]
        self.state = "Running"

    def op_08(self, instr):
        if self.get_value(1) == self.get_value(2):
            self.set_value(3, 1)
        else:
            self.set_value(3, 0)
        self.pointer += self.instr_length["08"]
        self.state = "Running"

    def op_09(self, instr):
        self.relative_base += self.get_value(1)
        self.pointer += self.instr_length["09"]
        self.state = "Running"

    def op_99(self, instr):
        self.pointer += self.instr_length["99"]
        self.state = "Stopped"

    def run(self):
        while self.state == "Running":
            opcode_full = self.get_opcode()
            opcode = opcode_full[-2:]
            self.modes = opcode_full[:-2]
            current_instr = self.get_instruction(opcode)
            if self.verbose_level >= 3:
                print("Executing", current_instr)
                print("Found opcode", opcode_full, opcode, self.modes)
            getattr(self, "op_" + opcode)(current_instr)
            if self.verbose_level >= 2:
                print("Pointer after execution:", self.pointer)
                print("Instructions:", ",".join(map(str, self.instructions)))

    def export(self):
        output = ""
        if self.reference != "":
            output += "Computer # " + str(self.reference)
        output += "\n" + "Instructions: " + ",".join(map(str, self.instructions))
        output += "\n" + "Relative base: " + str(self.relative_base)
        output += "\n" + "Inputs: " + ",".join(map(str, self.all_inputs))
        output += "\n" + "Outputs: " + ",".join(map(str, self.outputs))
        return output

    def export_io(self):
        output = ""
        if self.reference != "":
            output += "Computer # " + str(self.reference)
        output += "\n" + "Inputs: " + ",".join(map(str, self.all_inputs))
        output += "\n" + "Outputs: " + ",".join(map(str, self.outputs))
        return output
