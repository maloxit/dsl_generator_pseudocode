from enum import Enum


class Terminal(Enum):
    name = "name"
    number = "number"
    string = "string"
    key = "key"


tokenRegularExpressions = [
    (Terminal.name, r"\A[a-zA-Z_][\w]*"),
    (Terminal.number, r"\A[0-9]+[.]{0,1}[0-9]*"),
    (Terminal.string, r"\A\"(\\.|[^\\\"])*\"")
]

keys = [
    ('\\n', Terminal.key),
    (';', Terminal.key),
    ('@@', Terminal.key),
    ('@set', Terminal.key),
    ('@value', Terminal.key),
    ('@unary', Terminal.key),
    ('@infix', Terminal.key),
    ('@type', Terminal.key),
    ('@set', Terminal.key),
    ('@seq', Terminal.key),
    ('factorial', Terminal.key),
    ('floor', Terminal.key),
    ('ceil', Terminal.key),
    ('abs', Terminal.key),
    ('end algorithm', Terminal.key),
    ('end while', Terminal.key),
    ('end if', Terminal.key),
    ('end for', Terminal.key),
    ('->', Terminal.key),
    ('-', Terminal.key),
    ('return', Terminal.key),
    ('(', Terminal.key),
    (')', Terminal.key),
    ('[', Terminal.key),
    (']', Terminal.key),
    ('{', Terminal.key),
    ('}', Terminal.key),
    (',', Terminal.key),
    ('...', Terminal.key),
    ('..', Terminal.key),
    ('.', Terminal.key),
    (':=', Terminal.key),
    (':', Terminal.key),
    ('for', Terminal.key),
    ('do', Terminal.key),
    ('if', Terminal.key),
    ('then', Terminal.key),
    ('elseif', Terminal.key),
    ('else', Terminal.key),
    ('while', Terminal.key),
    ('next for', Terminal.key),
    ('repeat', Terminal.key),
    ('until', Terminal.key),
    ('yield', Terminal.key),
    ('select', Terminal.key),
    ('goto', Terminal.key),
    ('proc', Terminal.key),
    ('func', Terminal.key),
    ('iter', Terminal.key),
    ('array', Terminal.key),
    ('of', Terminal.key),
    ('struct', Terminal.key),
    ('\\uparrow', Terminal.key),
    ('natural', Terminal.key),
    ('integer', Terminal.key),
    ('rational', Terminal.key),
    ('binary', Terminal.key),
    ('==', Terminal.key),
    ('!=', Terminal.key),
    ('+', Terminal.key),
    ('/', Terminal.key),
    ('*', Terminal.key),
    ('div', Terminal.key),
    ('mod', Terminal.key),
    ('&', Terminal.key),
    ('|', Terminal.key),
    ('\\cup', Terminal.key),
    ('\\cap', Terminal.key),
    ('\\in', Terminal.key),
    ('\\notin', Terminal.key),
    ('\\subset', Terminal.key),
    ('\\', Terminal.key),
    ('pow', Terminal.key),
    ('<=', Terminal.key),
    ('>=', Terminal.key),
    ('<', Terminal.key),
    ('>', Terminal.key),
]


class Nonterminal(Enum):
    S = 'S'
    ALG = 'ALG'
    ALG_HEAD = 'ALG_HEAD'
    ALG_TYPE = 'ALG_TYPE'
    FUNC_NAME = 'FUNC_NAME'
    ALG_IN = 'ALG_IN'
    ALG_OUT = 'ALG_OUT'
    CODE_BLOCK = 'CODE_BLOCK'
    COMMAND = 'COMMAND'
    PRAGMA = 'PRAGMA'
    PRAGMA_NAME = 'PRAGMA_NAME'
    RETURN = 'RETURN'
    PARAM_LIST = 'PARAM_LIST'
    VAR = 'VAR'
    VAR_NAME = 'VAR_NAME'
    TYPE = 'TYPE'
    CONTROL_OPERATOR = "CONTROL_OPERATOR"
    BRANCHING = "BRANCHING"
    LOOP = "LOOP"
    TRANSITION_OPERATOR = "TRANSITION_OPERATOR"
    FOR = "FOR"
    WHILE = "WHILE"
    UNTIL = "UNTIL"


axiom = Nonterminal.S
