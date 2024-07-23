def Tokenize(chars: str) -> list:
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def Parse(tokens: str) -> list:
    ast = []
    amt_parens = 0
    while tokens:
        if tokens[0] == '(':
            tokens.pop(0)
            amt_parens += 1
            continue
        if tokens[0] == ')':
            tokens.pop(0)
            amt_parens -= 1
            continue
        ast.append(tokens[0])
        tokens.pop(0)
    if amt_parens != 0:
        raise ValueError("Unbalanced parenthesis!")
    return ast

tokens = Tokenize("(define x 10)")
ast = Parse(tokens)
print(ast)