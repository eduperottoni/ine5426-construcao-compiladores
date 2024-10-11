"""
Analisador sintático LL(1)
Entrada: x$
Saída: mensagem de erro ou de sucesso!


Temos uma pilha iniciando com o símbolo inicial da gramática e com o $

Pilha inicial:

$


1. defina i para que aponte para o primeiro símbolo de W
2. defina x para ser o símbolo no topo da pilha
3. enquanto x != $
4.      se x é o w[i] então desempilha e avança i
5.      senão se x é terminal então acuse erro
6.      senão se M[x][w[i]] vazio: erro
7.      senão se M[x][w[i]] = x -> y1 y2 yk
            imprima a produção x -> y1 y2 yk
            desempilha x
            empilha yk y2 y3
   defina x no topo da pilha
"""
# from queue import Queue

INPUT = "0M1m1M0"
TOKENS = []
TERMINALS = ["0", "1", "1M", "0M", "0m", "1m"]
TOKENS_MAPPING = {
    "0M": "a",
    "1M": "b", 
    "0m": "c",
    "1m": "d",
}
SYNTATIC_TABLE = {
    'S': {
        'a': 'B',
        "b": 'B',
        '0': 'B',    
        '1': 'B',
        '$': 'B',   
    },
    'B': {
        'a': 'aC',
        "b": "bC",
        '0': '0', 
        '1': '1',
    },
    "C": {
        'c': 'cB',
        'd': 'dB',
        '0': '0',
        '1': '1',
    }
}
QUEUE = []

def generate_tokens(input: str):
    for i in range(0, len(input) - 1, 2):
        TOKENS.append(TOKENS_MAPPING[f'{input[i]}{input[i+1]}'])
    TOKENS.append(f'{input[-1]}')
    TOKENS.append('$')
    print(TOKENS)


def syntatic_analysis() -> None:
    # squeue = Queue()
    QUEUE.append('$')
    QUEUE.append('S')

    i = TOKENS.pop(0)
    x = QUEUE.pop(-1)

    print(x)
    while x != '$':
        if x == i:
            i = TOKENS.pop(0)
            x = QUEUE.pop(-1)
        elif x in TERMINALS:
            raise SyntaxError("Algo está errado")
        elif i not in SYNTATIC_TABLE[x]:
            raise SyntaxError("Algo está errado")
        else:
            print(f'{x} -> {SYNTATIC_TABLE[x][i]}')
            for j in reversed(SYNTATIC_TABLE[x][i]):
                QUEUE.append(j)
            x = QUEUE.pop(-1)
    
    print('ENTRADA VÁLIDA')


generate_tokens(INPUT)
syntatic_analysis()


# 1. defina i para que aponte para o primeiro símbolo de W
# 2. defina x para ser o símbolo no topo da pilha
# 3. enquanto x != $
# 4.      se x é o w[i] então desempilha e avança
# 5.      senão se x é terminal então acuse erro
# 6.      senão se M[x][w[i]] vazio: erro
# 7.      senão se M[x][w[i]] = x -> y1 y2 yk
#             imprima a produção x -> y1 y2 yk
#             desempilha x
#             empilha yk y2 y3
#     defina x no topo da pilha