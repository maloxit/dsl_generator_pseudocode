from dsl_info import Terminal, tokenRegularExpressions, keys
from dsl_token import Token
import sys
import re


def __SkipSpaces(code, pos):
    for i in range(pos, len(code)):
        if not code[i].isspace() or code[i] == '\n':
            return i
    return len(code)


def __GetCurrentToken(code, pos):
    if code[pos] == '\n':
        token = Token(Token.Type.KEY)
        token.terminalType = Terminal.key
        token.str = '\\n'
        return token, pos + 1
    for key, terminal in keys:
        if code[pos : pos + len(key)] == key:
            if key[-1].isalpha() and pos + len(key) < len(code) and (code[pos + len(key)].isalpha() or code[pos + len(key)].isdigit() or code[pos + len(key)] == '_'):
                continue
            token = Token(Token.Type.KEY)
            token.terminalType = terminal
            token.str = key
            return token, pos + len(token.str)
    for terminal, regex in tokenRegularExpressions:
        result = re.match(regex, code[pos:])
        if not result:
            continue
        token = Token(Token.Type.TERMINAL)
        token.terminalType = terminal
        token.str = result.group(0)
        return token, pos + len(token.str)
    raise SyntaxError("Failed to recognize token")


def Tokenize(code):
    size = len(code)
    pos = 0
    tokens = []
    pos = __SkipSpaces(code, pos)
    while pos < size:
        token, pos = __GetCurrentToken(code, pos)
        tokens.append(token)
        pos = __SkipSpaces(code, pos)
    return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Need only one argument: program text path")
        sys.exit()
    with open(sys.argv[1], 'r') as file:
        tokenList = Tokenize(file.read())
        print("tokens:")
        for token in tokenList:
            print(f"TYPE: '{token.terminalType.name}', STRING: '{token.str}'.")
