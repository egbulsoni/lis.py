# Definir tipos para maior clareza e anotação de tipos
from typing import Union, List

Symbol = str  # Um símbolo é apenas uma string
Number = Union[int, float]
Exp = Union[Symbol, Number, List]  # Uma expressão pode ser um símbolo, número ou lista

def tokenize(chars: str) -> List[str]:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: List[str]) -> Exp:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Exp:
    "Numbers become numbers; every other token is a symbol."
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            return Symbol(token)

def standard_env():
    "An environment with some Scheme standard procedures."
    import math
    env = {}
    env.update(vars(math))  # Sin, cos, sqrt, pi, etc.
    env.update({
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    })
    return env

global_env = standard_env()

def eval(x: Exp, env=global_env) -> Exp:
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):        # variable reference
        return env[x]
    elif isinstance(x, Number):      # constant number
        return x                
    elif x[0] == 'if':               # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':           # definition
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:                            # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            source = input(prompt)
            if source.lower() in ['exit', 'quit']:
                break
            val = eval(parse(source))
            if val is not None: 
                print(schemestr(val))
        except Exception as e:
            print(f"Error: {e}")

def schemestr(exp) -> str:
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

repl()
