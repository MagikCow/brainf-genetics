# brackets: list identifying all brackets in the code
# [[line opened, line closed]]
# eg [[3,5], [6,9]] means that the first bracket was opened on line 3, closed on 5.
# second pair was opened on line 6 and closed on line 9.


def validate(code):
    open = code.count('[')
    close = code.count(']')

    if open != close:
        raise SyntaxError('Number of square brackets does not match!')


def bracket_map(code):
    brackets = []
    code_pos = 0   # position in the code to be compiled
    indentation_level = 0   # number of active open brackets

    for char in code:
        if char == '[':  # add line number as new item in list
            brackets.append([code_pos])
            indentation_level += 1

        elif char == ']':  # we find the previous non closed bracket
            if indentation_level == 0:
                raise SyntaxError('Closed square bracket before open one!')

            indentation_level -= 1

            for item in reversed(brackets):
                if len(item) == 1:  # if the length of the sublist is one
                    ix = brackets.index([item[0]])  # find the index of this item the main brackets list
                    brackets[ix].append(code_pos)  # add the closing bracket position to the main list
                    break

        code_pos += 1
    return brackets


# code: the brainf code to be complied
# code_pos: the current instruction being executed in the code
# cells: the row of cells in the brainf output
# pointer: which cell we are currently editing


def compile_step(code, code_pos, cells, pointer, brackets, output):
    cell_value = cells[pointer]
    instruction = code[code_pos]

    if instruction == '>':
        pointer += 1

    elif instruction == '<' and pointer > 0:
        pointer -= 1

    elif instruction == '+':
        if cell_value == 255:
            cells[pointer] = 0
        else:
            cells[pointer] += 1

    elif instruction == '-':
        if cell_value == 0:
            cells[pointer] = 255
        else:
            cells[pointer] -= 1

    elif instruction == '.':
        output.append(cell_value)

    elif instruction == ',':
        cells[pointer] = input('Enter input (1 byte)')

    elif instruction == '[':  # jump to matching ]
        if cell_value == 0:
            for pair in brackets:
                if pair[0] == code_pos:
                    code_pos = pair[1]

    elif instruction == ']':  # jump to matching [
        if cell_value != 0:
            for pair in brackets:
                if pair[1] == code_pos:
                    code_pos = pair[0]

    code_pos += 1

    return code_pos, cells, pointer


def compile(code):
    validate(code)

    brackets = bracket_map(code)
    code_pos = 0
    cells = [0] * 10000
    pointer = 0
    output = []

    ticks = 0  # number of instructions executed in the program
    while code_pos < len(code) and ticks < 10000:
        code_pos, cells, pointer = compile_step(code, code_pos, cells, pointer, brackets, output)
        ticks += 1

    output = list(map(lambda x: chr(x), output))  # turn list of ASCII characters to string
    output = ''.join(output)
    return output
