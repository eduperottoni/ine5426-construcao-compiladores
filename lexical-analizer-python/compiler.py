class LexicalAnalyser:
    def __init__(self):
        self.current_state = 0
        self.ws = [' ', '\t', '\n']
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '_'
        ]
        self.output = []

    def read_input(self, input_path: str):
        with open(input_path, 'rb') as code:
            buffer = code.read().decode() + '$'

        pointer_position = 0
        while pointer_position < len(buffer):
            char = buffer[pointer_position]
            print(self.current_state, char)
            if self.current_state == 0:
                if char in self.letters:
                    self.current_state = 1
                elif char in self.ws:
                    self.current_state = 0
                else:
                    self.current_state = 3

                pointer_position += 1

            elif self.current_state == 1:
                if char in self.letters or char in self.digits:
                    self.current_state = 1
                    pointer_position += 1
                else:
                    self.current_state = 2

            elif self.current_state == 2:
                self.output.append('IDENT')
                self.current_state = 0

            elif self.current_state == 3:
                if char in self.ws or char in self.letters or char == '$':
                    self.current_state = 4
                else:
                    self.current_state = 3
                    pointer_position += 1

            else:
                self.output.append('OUTRO')
                self.current_state = 0


analiser = LexicalAnalyser()
analiser.read_input('input.txt')
print(analiser.output)