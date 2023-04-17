from dsl_token import Token
import sys
import re


def __SkipSpaces(code, pos):
    for i in range(pos, len(code)):
        if not code[i].isspace() or code[i] == '\n':
            return i
    return len(code)


def __GetCurrentToken(code, pos, terms, keys):
    if code[pos] == '\n':
        token = Token(Token.Type.KEY)
        token.terminalType = "key"
        token.str = '\\n'
        return token, pos + 1
    for key in keys:
        if code[pos : pos + len(key)] == key:
            if key[-1].isalpha() and pos + len(key) < len(code) and (code[pos + len(key)].isalpha() or code[pos + len(key)].isdigit() or code[pos + len(key)] == '_'):
                continue
            token = Token(Token.Type.KEY)
            token.terminalType = "key"
            token.str = key
            return token, pos + len(token.str)
    for terminal in terms.keys():
        result = re.match(terms[terminal], code[pos:])
        if not result:
            continue
        token = Token(Token.Type.TERMINAL)
        token.terminalType = terminal
        token.str = result.group(0)
        return token, pos + len(token.str)
    raise SyntaxError("Failed to recognize token")


def Tokenize(code, terms, keys):
    size = len(code)
    pos = 0
    tokens = []
    pos = __SkipSpaces(code, pos)
    while pos < size:
        token, pos = __GetCurrentToken(code, pos, terms, keys)
        tokens.append(token)
        pos = __SkipSpaces(code, pos)
    return tokens
