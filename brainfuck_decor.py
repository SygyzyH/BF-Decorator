import inspect


class BrainfuckInstance:
    def __init__(self, code_string, current_line):
        self.data_head_pointer = 0
        self.data_strip = [0]
        self.current_line = current_line
        self.call_stack = []
        self.code_string = code_string
        self.input_stream = []
        self.output_stream = []

    def load_input_stream(self, *args):
        self.input_stream += args

    def increment_line(func):
        def wrapper(self):
            func(self)
            self.current_line += 1
        return wrapper

    def run(self):
        # run through all instructions
        while self.current_line < len(self.code_string):
            instruction = self.code_string[self.current_line]
            if instruction == '>':
                self.inc_datap()
            elif instruction == '<':
                self.dec_datap()
            elif instruction == '+':
                self.inc_data()
            elif instruction == '-':
                self.dec_data()
            elif instruction == '[':
                self.start_loop()
            elif instruction == ']':
                self.stop_loop()
            elif instruction == ',':
                self.input()
            elif instruction == '.':
                self.output()
            else:
                self.current_line += 1

    def current_value(self):
        return {
            "output": self.output_stream,
            "head": self.data_head_pointer,
            "data": self.data_strip
        }

    # >
    @increment_line
    def inc_datap(self):
        self.data_head_pointer += 1
        if len(self.data_strip) == self.data_head_pointer:
            self.data_strip.append(0)

    # <
    @increment_line
    def dec_datap(self):
        if self.data_head_pointer > 0:
            self.data_head_pointer -= 1
        else:
            raise IndexError("line " + str(self.current_line) + ", Data head pointer cant point to a negative value.")

    # +
    @increment_line
    def inc_data(self):
        self.data_strip[self.data_head_pointer] = (self.data_strip[self.data_head_pointer] + 1) % 256

    # -
    @increment_line
    def dec_data(self):
        self.data_strip[self.data_head_pointer] = (self.data_strip[self.data_head_pointer] - 1) % 256

    # [
    def start_loop(self):
        self.call_stack.append(self.current_line)
        if self.data_strip[self.data_head_pointer] == 0:
            self.current_line = self.code_string.index(']', self.current_line)
        else:
            self.current_line += 1

    # ]
    def stop_loop(self):
        match = self.call_stack.pop()
        if self.data_strip[self.data_head_pointer] != 0:
            self.current_line = match
        else:
            self.current_line += 1

    # ,
    @increment_line
    def input(self):
        self.data_strip[self.data_head_pointer] = self.input_stream.pop(0) % 256

    # .
    @increment_line
    def output(self):
        self.output_stream.append(self.data_strip[self.data_head_pointer])


def brainfuck(func):
    def wrapper(*args, current_line=0):
        instance = BrainfuckInstance(''.join(inspect.getsource(func).split('\n')[2:]), current_line)
        instance.load_input_stream(*args)
        instance.run()
        return instance.current_value()
    return wrapper


def pow_f(base, exponent):
    return multiply_but_i_hate_myself(pow_f(base, exponent - 1), base)["output"][0] if exponent > 1 else base


def square(a):
    return multiply_but_i_hate_myself(a, a)["output"][0]


@brainfuck
def multiply_but_i_hate_myself(a, b):
    ",>,>><<<[>[->+>+<<]>[-<+>]<<-]>>>."


@brainfuck
def fibunachy_but_i_hate_myself():
    "+.>+>,-[-[->+<]<<[->>>>+>+<<<<<]>[->>>>>+>+<<<<<<]>>>[-<<<<+>>>>]>[-<<<+>>>]>[-<<<<<+>>>>>]>.[-<<<<<+>>>>>]<<<<]"

@brainfuck
def myfunc(a, b, c):
	",>,>,<<[->+<]>[->+<]>."


if __name__ == '__main__':
    print(square(15))
    print(pow_f(5, 3))
    print(fibunachy_but_i_hate_myself(14))
    print(myfunc(6, 9, 42)["output"][0])
