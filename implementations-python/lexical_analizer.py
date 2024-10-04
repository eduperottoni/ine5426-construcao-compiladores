from enum import Enum


# Define the TokenType enum
class TokenType(Enum):
    IDENT = 1
    OUTRO = 2
    NI = 3
    NPF = 4


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
DIGITS = "0123456789"
WS = ['\t', ' ', '\n']
RESERVED = ["def", "int", "return", "float", "string", "break", "print", "read", "if", "for", "else", "new"]

TOKEN_LIST_SIZE = 0
LEXIC_ANALYSIS_STAGE = 0
token_list = []

READ_POINTER_POSITION = 0
PROGRAM_LINE_NUMBER = 1

# In python, we just need a dictionary to represent the symbol table
SYMBOL_TABLE: dict[str, set[int]] = {}

def is_letter(c):
    return c in LETTERS


def is_digit(c):
    return c in DIGITS


def is_ws(c):
    return c in WS


def generate_token(token_type, token_value):
    global TOKEN_LIST_SIZE, token_list, SYMBOL_TABLE, PROGRAM_LINE_NUMBER
    try:
        token_list.append(Token(token_type, token_value))
        TOKEN_LIST_SIZE += 1
        # print(f"Adding token of type {token_type}")
        if token_type == TokenType.IDENT and token_value not in RESERVED:
            if token_value not in SYMBOL_TABLE:
                SYMBOL_TABLE[token_value] = set([PROGRAM_LINE_NUMBER])
            else:
                SYMBOL_TABLE[token_value].add(PROGRAM_LINE_NUMBER)
    
    except MemoryError:
        # print("Memory allocation failed")
        token_list = []


def fail():
    global LEXIC_ANALYSIS_STAGE, READ_POINTER_POSITION
    # print("fail")
    # Move one character back in the file (to be read by the next diagram)
    READ_POINTER_POSITION -= 1
    LEXIC_ANALYSIS_STAGE += 1


def get_identifier(buffer):
    # print(f'ENTRANDO EM IDENT: {id(file_ptr)}')
    global READ_POINTER_POSITION
    IDENTIFIER_CURRENT_STATE = 0

    ident_buffer = ""
    while True:
        if IDENTIFIER_CURRENT_STATE != 2:
            c = buffer[READ_POINTER_POSITION]
            READ_POINTER_POSITION += 1
        # print(f"id-CHAR: {c}")
        # print(f"id-STATE: {IDENTIFIER_CURRENT_STATE}")

        if not c:  # End of file check
            return fail()

        if IDENTIFIER_CURRENT_STATE == 0:
            if is_letter(c):
                ident_buffer += c
                IDENTIFIER_CURRENT_STATE = 1
            else:
                # file_ptr.seek(-1, 1)  # Move back one character
                return fail()
        elif IDENTIFIER_CURRENT_STATE == 1:
            if not is_letter(c) and not is_digit(c):
                IDENTIFIER_CURRENT_STATE = 2
            else:
                ident_buffer += c
        elif IDENTIFIER_CURRENT_STATE == 2:
            READ_POINTER_POSITION -= 1
            return generate_token(TokenType.IDENT, ident_buffer)


def get_number(buffer):
    # print(f'ENTRANDO EM NUM: {id(file_ptr)}')
    global READ_POINTER_POSITION
    NUM_CURRENT_STATE = 17  # Start state
    num_buffer = ""
    while True:
        if NUM_CURRENT_STATE not in [19, 22, 26]:
            c = buffer[READ_POINTER_POSITION]
            READ_POINTER_POSITION += 1
        # print(f"num-CHAR: {ord(c)}")
        # print(f"num-STATE: {NUM_CURRENT_STATE}")

        if not c:  # End of file check
            return fail()

        if NUM_CURRENT_STATE == 17:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 18
            else:
                # print("AQUI")
                # file_ptr.seek(-1, 1)
                # READ_POINTER_POSITION -= 1
                return fail()
        elif NUM_CURRENT_STATE == 18:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 18
            elif c == '.':
                num_buffer += c
                NUM_CURRENT_STATE = 20
            elif c == 'E':
                num_buffer += c
                NUM_CURRENT_STATE = 23
            else:
                NUM_CURRENT_STATE = 19
        elif NUM_CURRENT_STATE == 19:
            # file_ptr.seek(-1, 1)
            READ_POINTER_POSITION -= 1
            return generate_token(TokenType.NI, num_buffer)
        elif NUM_CURRENT_STATE == 20:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 21
            else:
                return fail()
        elif NUM_CURRENT_STATE == 21:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 21
            elif c == 'E':
                num_buffer += c
                NUM_CURRENT_STATE = 23
            else:
                NUM_CURRENT_STATE = 22
        elif NUM_CURRENT_STATE == 22:
            # file_ptr.seek(-1, 1)
            READ_POINTER_POSITION -= 1
            return generate_token(TokenType.NPF, num_buffer)
        elif NUM_CURRENT_STATE == 23:
            if c in ['+', '-']:
                num_buffer += c
                NUM_CURRENT_STATE = 24
            elif is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 25
            else:
                return fail()
        elif NUM_CURRENT_STATE == 24:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 25
            else:
                return fail()
        elif NUM_CURRENT_STATE == 25:
            if is_digit(c):
                num_buffer += c
                NUM_CURRENT_STATE = 25
            else:
                NUM_CURRENT_STATE = 26
        elif NUM_CURRENT_STATE == 26:
            # file_ptr.seek(-1, 1)
            READ_POINTER_POSITION -= 1
            return generate_token(TokenType.NPF, num_buffer)

def get_other(buffer):
    # print(f'ENTRANDO EM OTHER: {id(file_ptr)}')
    global READ_POINTER_POSITION
    OTHER_CURRENT_STATE = 0
    other_buffer = ''
    while True:
        if OTHER_CURRENT_STATE != 1:
            c = buffer[READ_POINTER_POSITION]
            READ_POINTER_POSITION += 1

            # c = file_ptr.read(1).decode('utf-8')  # Read next character from input

        if not c:  # End of file check
            return fail()

        # print(f"other-CHAR: {c}")  # To print the ASCII value of `c`
        # print(f"other-state: {OTHER_CURRENT_STATE}")

        if OTHER_CURRENT_STATE == 0:
            if is_letter(c) or is_digit(c) or is_ws(c):
                # READ_POINTER_POSITION -= 1
                # file_ptr.seek(-1, 1)  # Move back one character
                return fail()
            else:
                # print('INDO PARA ESTADO 1')
                other_buffer += c
                OTHER_CURRENT_STATE = 1
        elif OTHER_CURRENT_STATE == 1:
            # file_ptr.seek(-1, 1)
            # READ_POINTER_POSITION -= 1
            return generate_token(TokenType.OUTRO, other_buffer)

def main():
    global TOKEN_LIST_SIZE, READ_POINTER_POSITION, PROGRAM_LINE_NUMBER
    num_tokens = TOKEN_LIST_SIZE

    with open("input3.txt", "rb") as file:
        buffer = file.read().decode('utf-8')
        while True:
            if READ_POINTER_POSITION >= len(buffer):
                break

            c = buffer[READ_POINTER_POSITION]
            # print(f"pointer position: {READ_POINTER_POSITION}")
            # print(f'CARACTERE LIDO: {c}')

            READ_POINTER_POSITION += 1
            if not c:  # End of file
                break
                
            if c == '\n':
                PROGRAM_LINE_NUMBER += 1
            # Ignore occurrences of \b, \t, or \n
            if is_ws(c):
                continue

            READ_POINTER_POSITION -= 1

            get_identifier(buffer)

            if TOKEN_LIST_SIZE > num_tokens:
                # print(f"Number of tokens: {TOKEN_LIST_SIZE}")
                num_tokens = TOKEN_LIST_SIZE
                continue

            get_number(buffer)

            if TOKEN_LIST_SIZE > num_tokens:
                # print(f"Number of tokens: {TOKEN_LIST_SIZE}")
                num_tokens = TOKEN_LIST_SIZE
                continue

            get_other(buffer)

    # Print the token list
    for i in range(TOKEN_LIST_SIZE):
        print(f"{token_list[i].type} -> {token_list[i].value}")

    print('\nTABELA DE SÍMBOLOS:')
    print(SYMBOL_TABLE)

    print()

if __name__ == "__main__":
    main()