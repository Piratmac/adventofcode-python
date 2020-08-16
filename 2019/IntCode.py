class IntCode:
    instructions = []
    pointer = 0
    state = "Running"
    modes = "000"
    inputs = []
    outputs = []
    verbose_level = 0
    instr_length = {
        "01": 4,
        "02": 4,
        "03": 2,
        "04": 2,
        "05": 3,
        "06": 3,
        "07": 4,
        "08": 4,
        "99": 1,
    }

    def __init__(self, instructions):
        self.instructions = list(map(int, instructions.split(",")))

    def reset(self, instructions):
        self.instructions = list(map(int, instructions.split(",")))
        self.pointer = 0
        self.state = "Running"

    def get_opcode(self):
        instr = self.instructions[self.pointer]
        opcode_full = "0" * (5 - len(str(instr))) + str(instr)
        return opcode_full

    def get_instruction(self, opcode):
        return self.instructions[
            self.pointer : self.pointer + self.instr_length[opcode]
        ]

    def get_value(self, param_position):
        if self.modes[2 - (param_position - 1)] == "0":
            return self.instructions[self.instructions[self.pointer + param_position]]
        else:
            return self.instructions[self.pointer + param_position]

    def op_01(self, instr):
        self.instructions[instr[3]] = self.get_value(1) + self.get_value(2)
        self.pointer += self.instr_length["01"]
        self.state = "Running"

    def op_02(self, instr):
        self.instructions[instr[3]] = self.get_value(1) * self.get_value(2)
        self.pointer += self.instr_length["02"]
        self.state = "Running"

    def op_03(self, instr):
        self.instructions[instr[1]] = self.inputs.pop(0)
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
            self.instructions[instr[3]] = 1
        else:
            self.instructions[instr[3]] = 0
        self.pointer += self.instr_length["07"]
        self.state = "Running"

    def op_08(self, instr):
        if self.get_value(1) == self.get_value(2):
            self.instructions[instr[3]] = 1
        else:
            self.instructions[instr[3]] = 0
        self.pointer += self.instr_length["08"]
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
        instr = ",".join(map(str, self.instructions))
        inputs = ",".join(map(str, self.inputs))
        outputs = ",".join(map(str, self.outputs))
        return (
            "Instructions: " + instr + "\nInputs: " + inputs + "\nOutputs: " + outputs
        )
