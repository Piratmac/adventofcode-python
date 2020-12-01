import json

# -------------------------------- Notes ----------------------------- #


# This program will run pseudo-assembly code based on provided instructions
# It can handle a set of instructions (which are writable), a stack and registers


# -------------------------------- Program flow exceptions ----------------------------- #


class MissingInput(RuntimeError):
    pass


class ProgramHalt(RuntimeError):
    pass


# -------------------------------- Main program class ----------------------------- #
class Program:

    # Whether to print outputs
    print_output = False
    # Print outputs in a detailed way (useful when debugging is detailed)
    print_output_verbose = False
    # Print outputs when input is required (useful for text-based games)
    print_output_before_input = False

    # Whether to print the inputs received (useful for predefined inputs)
    print_input = False
    # Print inputs in a detailed way (useful when debugging is detailed)
    print_input_verbose = False

    # Whether to print the instructions before execution
    print_details_before = False
    # Whether to print the instructions after execution
    print_details_after = False

    # Output format - for all instructions
    print_format = "{pointer:5}-{opcode:15} {instr:50} - R: {registers} - Stack ({stack_len:4}): {stack}"
    # Output format for numbers
    print_format_numbers = "{val:5}"

    # Whether inputs and outputs are ASCII codes or not
    input_ascii = True
    output_ascii = True

    # Whether to ask user for input or not (if not, will raise exception)
    input_from_terminal = True

    # Bit length used for NOT operation (bitwise inverse)
    bit_length = 15

    # Where to store saves
    save_data_file = "save.txt"

    # Maximum number of instructions executed
    max_instructions = 10 ** 7

    # Sets up the program based on the provided instructions
    def __init__(self, program):
        self.instructions = program.copy()
        self.registers = [0] * 8
        self.stack = []
        self.pointer = 0
        self.state = "Running"
        self.output = []
        self.input = []
        self.instructions_done = 0

    ################### Main program body ###################

    def run(self):
        while (
            self.state == "Running" and self.instructions_done < self.max_instructions
        ):
            self.instructions_done += 1
            # Get details of current operation
            opcode = self.instructions[self.pointer]
            current_instr = self.get_instruction(opcode)

            # Outputs operation details before its execution
            if self.print_details_before:
                self.print_operation(opcode, current_instr)

            self.operation_codes[opcode][2](self, current_instr)

            # Outputs operation details after its execution
            if self.print_details_after:
                self.print_operation(opcode, self.get_instruction(opcode))

            # Moves the pointer
            if opcode not in self.operation_jumps and self.state == "Running":
                self.pointer += self.operation_codes[opcode][1]

        print("instructions", i)

    # Gets all parameters for the current instruction
    def get_instruction(self, opcode):
        args_order = self.operation_codes[opcode][3]
        values = [opcode] + [
            self.instructions[self.pointer + order + 1] for order in args_order
        ]
        print([self.pointer + order + 1 for order in args_order])

        print(args_order, values, self.operation_codes[opcode])

        return values

    # Prints the details of an operation according to the specified format
    def print_operation(self, opcode, instr):
        params = instr.copy()
        # Remove opcode
        del params[0]

        # Handle stack operations
        if opcode in self.operation_stack and self.stack:
            params.append(self.stack[-1])
        elif opcode in self.operation_stack:
            params.append("Empty")

        # Format the numbers
        params = list(map(self.format_numbers, params))

        data = {}
        data["opcode"] = opcode
        data["pointer"] = self.pointer
        data["registers"] = ",".join(map(self.format_numbers, self.registers))
        data["stack"] = ",".join(map(self.format_numbers, self.stack))
        data["stack_len"] = len(self.stack)

        instr_output = self.operation_codes[opcode][0].format(*params, **data)
        final_output = self.print_format.format(instr=instr_output, **data)
        print(final_output)

    # Outputs all stored data and resets it
    def print_output_data(self):
        if self.output and self.print_output_before_input:
            if self.output_ascii:
                print("".join(self.output), sep="", end="")
            else:
                print(self.output, end="")
        self.output = []

    # Formats numbers
    def format_numbers(self, code):
        return self.print_format_numbers.format(val=code)

    # Sets a log level based on predefined rules
    def log_level(self, level):
        self.print_output = False
        self.print_output_verbose = False
        self.print_output_before_input = False

        self.print_input = False
        self.print_input_verbose = False

        self.print_details_before = False
        self.print_details_after = False

        if level >= 1:
            self.print_output = True
            self.print_input = True

        if level >= 2:
            self.print_output_verbose = True
            self.print_output_before_input = True
            self.print_input_verbose = True
            self.print_details_before = True

        if level >= 3:
            self.print_details_after = True

    ################### Get and set registers and memory ###################

    # Reads a "normal" value based on the provided reference
    def get_register(self, reference):
        return self.registers[reference]

    # Writes a value to a register
    def set_register(self, reference, value):
        self.registers[reference] = value

    # Reads a memory value based on the code
    def get_memory(self, code):
        return self.instructions[code]

    # Writes a value to the memory
    def set_memory(self, reference, value):
        self.instructions[reference] = value

    ################### Start / Stop the program ###################

    # halt: Stop execution and terminate the program
    def op_halt(self, instr):
        self.state = "Stopped"
        raise ProgramHalt("Reached Halt instruction")

    # pass 21: No operation
    def op_pass(self, instr):
        return

    ################### Basic operations ###################

    # add a b c: Assign into <a> the sum of <b> and <c>",
    def op_add(self, instr):
        self.set_register(
            instr[1], self.get_register(instr[2]) + self.get_register(instr[3])
        )

    # mult a b c: store into <a> the product of <b> and <c>",
    def op_multiply(self, instr):
        self.set_register(
            instr[1], self.get_register(instr[2]) * self.get_register(instr[3])
        )

    # mod a b c: store into <a> the remainder of <b> divided by <c>",
    def op_modulo(self, instr):
        self.set_register(
            instr[1], self.get_register(instr[2]) % self.get_register(instr[3])
        )

    # set a b: set register <a> to the value of <b>
    def op_set(self, instr):
        self.set_register(instr[1], self.get_register(instr[2]))

    ################### Comparisons ###################

    # eq a b c: set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise",
    def op_equal(self, instr):
        self.set_register(
            instr[1],
            1 if self.get_register(instr[2]) == self.get_register(instr[3]) else 0,
        )

    # gt a b c: set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise",
    def op_greater_than(self, instr):
        self.set_register(
            instr[1],
            1 if self.get_register(instr[2]) > self.get_register(instr[3]) else 0,
        )

    ################### Binary operations ###################

    # and a b c: stores into <a> the bitwise and of <b> and <c>",
    def op_and(self, instr):
        self.set_register(
            instr[1], self.get_register(instr[2]) & self.get_register(instr[3])
        )

    # or a b c: stores into <a> the bitwise or of <b> and <c>",
    def op_or(self, instr):
        self.set_register(
            instr[1], self.get_register(instr[2]) | self.get_register(instr[3])
        )

    # not a b: stores 15-bit bitwise inverse of <b> in <a>",
    def op_not(self, instr):
        self.set_register(
            instr[1], ~self.get_register(instr[2]) & int("1" * self.bit_length, 2)
        )

    ################### Jumps ###################

    # jmp a: jump to <a>",
    def op_jump(self, instr):
        self.pointer = self.get_register(instr[1])

    # jt a b: if <a> is nonzero, jump to <b>",
    def op_jump_if_true(self, instr):
        self.pointer = (
            self.get_register(instr[2])
            if self.get_register(instr[1]) != 0
            else self.pointer + self.operation_codes["jump_if_true"][1]
        )

    # jf a b: if <a> is zero, jump to <b>",
    def op_jump_if_false(self, instr):
        self.pointer = (
            self.get_register(instr[2])
            if self.get_register(instr[1]) == 0
            else self.pointer + self.operation_codes["jump_if_false"][1]
        )

    ################### Memory-related operations ###################

    # rmem a b: read memory at address <b> and write it to <a>",
    def op_read_memory(self, instr):
        self.set_register(instr[1], self.get_memory(self.get_register(instr[2])))

    # wmem a b: write the value from <b> into memory at address <a>",
    def op_write_memory(self, instr):
        self.set_memory(self.get_register(instr[1]), self.get_register(instr[2]))

    ################### Stack-related operations ###################

    # push a: push <a> onto the stack",
    def op_push(self, instr):
        self.stack.append(self.get_register(instr[1]))

    # pop a: remove the top element from the stack and write it into <a>; empty stack = error",
    def op_pop(self, instr):
        if not self.stack:
            self.state = "Error"
        else:
            self.set_register(instr[1], self.stack.pop())

    # ret: remove the top element from the stack and jump to it; empty stack = halt",
    def op_jump_to_stack(self, instr):
        if not self.stack:
            raise RuntimeError("No stack available for jump")
        else:
            self.pointer = self.stack.pop()

    ################### Input and output ###################

    # in a: read a character from the terminal and write its ascii code to <a>
    def op_input(self, instr):
        self.print_output_data()

        self.custom_commands()
        while not self.input:
            if self.input_from_terminal:
                self.add_input(input() + "\n")
            else:
                raise MissingInput()

            if self.input[0] == "?":
                self.custom_commands()

        letter = self.input.pop(0)

        # Print what we received?
        if self.print_input_verbose:
            print("   Input: ", letter)
        elif self.print_input:
            print(letter, end="")

        # Actually write the input to the registers
        if self.input_ascii:
            self.set_register(instr[1], ord(letter))
        else:
            self.set_register(instr[1], letter)

    # out a: write the character represented by ascii code <a> to the terminal",
    def op_output(self, instr):
        # Determine what to output
        if self.output_ascii:
            letter = chr(self.get_register(instr[1]))
        else:
            letter = self.get_register(instr[1])

        # Store for future use
        self.output += letter

        # Display output immediatly?
        if self.print_output_verbose:
            print("       Output:", letter)
        elif self.print_output:
            print(letter, end="")

    ################### Save and restore ###################

    def save_state(self):
        data = [
            self.instructions,
            self.registers,
            self.stack,
            self.pointer,
            self.state,
            self.output,
            self.input,
        ]
        with open(self.save_data_file, "w") as f:
            json.dump(data, f)

    def restore_state(self):
        with open(self.save_data_file, "r") as f:
            data = json.load(f)

        (
            self.instructions,
            self.registers,
            self.stack,
            self.pointer,
            self.state,
            self.output,
            self.input,
        ) = data

    ################### Adding manual inputs ###################

    def add_input(self, input_data, convert_ascii=True):
        try:
            self.input += input_data
        except TypeError:
            self.input.append(input_data)

    ################### Custom commands ###################

    # Pause until input provided
    def custom_pause(self, instr):
        print("Program paused. Press Enter to continue.")
        input()

    # Pause until input provided
    def custom_stop(self, instr):
        self.op_halt(instr)

    # Save
    def custom_save(self, instr):
        self.save_state()
        if self.print_output:
            print("\nSaved game.")

    # Restore
    def custom_restore(self, instr):
        self.restore_state()
        if self.print_output:
            print("\nRestored the game.")

    # set a b: set register <a> to the value of <b>
    def custom_write(self, instr):
        self.op_set([instr[0]] + list(map(int, instr[1:])))

    # log a: sets the log level to X
    def custom_log(self, instr):
        self.log_level(int(instr[1]))
        if self.print_output:
            print("\nChanged log level to", instr[1])

    # print: prints the current situation in a detailed way
    def custom_print(self, instr):
        self.print_operation("?print", instr)

    def custom_commands(self):
        while self.input and self.input[0] == "?":
            command = self.input.pop(0)
            while command[-1] != "\n" and self.input:
                command += self.input.pop(0)

            if self.print_input:
                print(command)

            command = command.replace("\n", "").split(" ")
            self.operation_codes[command[0]][2](self, command)

    # ADDING NEW INSTRUCTIONS
    # - Create a method with a name starting by op_
    #     Its signature must be: op_X (self, instr)
    #     instr contains the list of values relevant to this operation (raw data from instructions set)
    # - Reference this method in the variable operation_codes
    #     Format of the variable:
    #     operation code: [
    #         debug formatting (used by str.format)
    #         number of operands (including the operation code)
    #         method to call
    #         argument order] ==> [2, 0, 1] means arguments are in provided as c, a, b
    # - Include it in operation_jumps or operation_stack if relevant

    # ADDING CUSTOM INSTRUCTIONS
    # Those instructions are not interpreted by the run() method
    # Therefore:
    #  - They will NOT move the pointer
    #  - They will NOT impact the program (unless you make them do so)
    # They're processed through the op_input method
    # Custom operations are also referenced in the same operation_codes variable
    # Custom operations start with ? for easy identification during input processing

    # TL;DR: Format:
    # operation code: [
    #     debug formatting
    #     number of operands (including the operation code)
    #     method to call
    #     argument order]
    operation_codes = {
        # Start / Stop
        0: ["halt", 1, op_halt, []],
        21: ["pass", 1, op_pass, []],
        # Basic operations
        9: ["add: {0} = {1}+{2}", 4, op_add, [2, 0, 1]],  # This means c = a + b
        10: ["mult: {0} = {1}*{2}", 4, op_multiply, [0, 1, 2]],
        11: ["mod: {0} = {1}%{2}", 4, op_modulo, [0, 1, 2]],
        1: ["set: {0} = {1}", 3, op_set, [0, 1]],
        # Comparisons
        4: ["eq: {0} = {1} == {2}", 4, op_equal, [0, 1, 2]],
        5: ["gt: {0} = ({1} > {2})", 4, op_greater_than, [0, 1, 2]],
        # Binary operations
        12: ["and: {0} = {1}&{2}", 4, op_and, [0, 1, 2]],
        13: ["or: {0} = {1}|{2}", 4, op_or, [0, 1, 2]],
        14: ["not: {0} = ~{1}", 3, op_not, [0, 1]],
        # Jumps
        6: ["jump: go to {0}", 2, op_jump, [0]],
        7: ["jump if yes: go to {1} if {0}", 3, op_jump_if_true, [0, 1]],
        8: ["jump if no: go to {1} if !{0}", 3, op_jump_if_false, [0, 1]],
        # Memory-related operations
        15: ["rmem: {0} = M{1}", 3, op_read_memory, [0, 1]],
        16: ["wmem: write {1} to M{0}", 3, op_write_memory, [0, 1]],
        # Stack-related operations
        2: ["push: stack += {0}", 2, op_push, [0]],
        3: ["pop: {0} = stack.pop() ({1})", 2, op_pop, [0]],
        18: ["pop & jump: jump to stack.pop() ({0})", 2, op_jump_to_stack, []],
        # Inputs and outputs
        19: ["out: print {0}", 2, op_output, [0]],
        20: ["in: {0} = input", 2, op_input, [0]],
        # Custom operations
        "?save": ["Saved data", 2, custom_save, []],
        "?write": ["Wrote data", 3, custom_write, []],
        "?restore": ["Restored data", 2, custom_restore, []],
        "?log": ["Logging enabled", 2, custom_log, []],
        "?stop": ["STOP", 2, custom_stop, []],
        "?pause": ["Pause", 2, custom_pause, []],
        "?print": ["Print data", 1, custom_print, []],
    }
    # Operations in this list will not move the pointer through the run method
    # (this is because they do it themselves)
    operation_jumps = ["jump", "jump_if_true", "jump_if_false", "jump_to_stack"]
    # Operations in this list use the stack
    # (the value taken from stack will be added to debug)
    operation_stack = ["pop", "jump_to_stack"]


# -------------------------------- Documentation & main variables ----------------------------- #

# HOW TO MAKE IT WORK
# The program has a set of possible instructions
# The exact list is available in variable operation_codes
# In order to work, you must modify this variable operation_codes so that the key is the code in your computer

# If you need to override the existing methods, you need to override operation_codes


# NOT OPERATION
# This will perform a bitwise inverse
# However, it requires the length (in bits) specific to the program's hardware
# Therefore, update Program.bit_length
# TL;DR: Length in bits used for NOT
Program.bit_length = 15

# Save file (stored as JSON)
Program.save_data_file = "save.txt"

# Maximum instructions to be executed
Program.max_instructions = 10 ** 7
