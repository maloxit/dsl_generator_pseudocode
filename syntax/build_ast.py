from dsl_token import *
from syntax.core import *


class TreeNode:
    class Type(Enum):
        TOKEN = 0
        NONTERMINAL = 1


    def __init__(self, type):
        self.type = type
        self.attribute = None

class AstBuilder():

    def __init__(self, grammar, tokenList, axiom) -> None:
        self.states = []
        self.grammar = grammar
        self.tokenList = tokenList
        self.end = len(tokenList)
        self.axiom = axiom
        self.states = []

    
    def __ret(self):
        self.states[-1]['rule_index'] += 1
        while self.states[-1]['rule_index'] >= len(self.states[-1]['node'].nextNodes):
            self.states.pop()
            if len(self.states) == 0:
                raise Exception(f"Fail")
            self.states[-1]['rule_index'] += 1
    
    def __walk(self):
        self.states = [{
            'parent_state': None,
            'pos': 0,
            'node': self.grammar[self.axiom],
            'rule_index': 0,
            'nonterm': self.axiom
        }]
        while True:
            state = self.states[-1]
            
            pos = state['pos']
            node = state['node']
            rule = node.nextNodes[state['rule_index']]

            if NodeType.END == rule[0].type:
                parent_state = state['parent_state']
                if parent_state is None:
                    if pos == self.end:
                        return
                    else:
                        self.__ret()
                        continue    
                self.states.append({
                    'parent_state': parent_state['parent_state'],
                    'pos': pos,
                    'node': parent_state['node'].nextNodes[parent_state['rule_index']][0],
                    'rule_index': 0,
                    'nonterm': parent_state['nonterm']
                })
                continue
            elif NodeType.NONTERMINAL == rule[0].type:
                if rule[0].nonterminal not in self.grammar:
                    raise Exception(f"Failed to find '{rule[0].nonterminal}' description")
                self.states.append({
                    'parent_state': state,
                    'pos': pos,
                    'node': self.grammar[rule[0].nonterminal],
                    'rule_index': 0,
                    'nonterm': rule[0].nonterminal
                })
                continue
            if pos >= self.end:
                self.__ret()
                continue
            newToken = self.tokenList[pos]
            if NodeType.KEY == rule[0].type and Token.Type.KEY == newToken.type and newToken.str == rule[0].str:
                self.states.append({
                    'parent_state': state['parent_state'],
                    'pos': pos+1,
                    'node': rule[0],
                    'rule_index': 0,
                    'nonterm': state['nonterm']
                })
                continue
            elif NodeType.TERMINAL == rule[0].type and Token.Type.TERMINAL == newToken.type and newToken.terminalType == rule[0].terminal:
                self.states.append({
                    'parent_state': state['parent_state'],
                    'pos': pos+1,
                    'node': rule[0],
                    'rule_index': 0,
                    'nonterm': state['nonterm']
                })
                continue

            self.__ret()
            continue
    
    def build(self):
        ast = TreeNode(TreeNode.Type.NONTERMINAL)
        ast.nonterminalType = self.axiom
        ast.childs = []
        ast.commands = []
        nodes_stack = [ast]
        self.__walk()
        for state in self.states:
            pos = state['pos']
            node = state['node']
            rule = node.nextNodes[state['rule_index']]

            if NodeType.END == rule[0].type:
                parent_state = state['parent_state']
                if parent_state is None:
                    if pos == self.end:
                        nodes_stack[-1].commands.append(rule[1])
                        return ast
                    else:
                        raise Exception(f"Fail")
                nodes_stack[-1].commands.append(rule[1])
                nodes_stack.pop()
                continue
            elif NodeType.NONTERMINAL == rule[0].type:
                if rule[0].nonterminal not in self.grammar:
                    raise Exception(f"Failed to find '{rule[0].nonterminal}' description")
                newNonterm = TreeNode(TreeNode.Type.NONTERMINAL)
                newNonterm.nonterminalType = rule[0].nonterminal
                newNonterm.childs = []
                newNonterm.commands = []
                nodes_stack[-1].childs.append(newNonterm)
                nodes_stack[-1].commands.append(rule[1])
                node = rule[0]
                nodes_stack.append(newNonterm)
                continue
            if pos >= self.end:
                raise Exception(f"Fail")
            newToken = self.tokenList[pos]
            if NodeType.KEY == rule[0].type and Token.Type.KEY == newToken.type and newToken.str == rule[0].str:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                nodes_stack[-1].childs.append(element)
                nodes_stack[-1].commands.append(rule[1])
                continue
            elif NodeType.TERMINAL == rule[0].type and Token.Type.TERMINAL == newToken.type and newToken.terminalType == rule[0].terminal:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                nodes_stack[-1].childs.append(element)
                nodes_stack[-1].commands.append(rule[1])
                continue

            raise Exception(f"Fail")
        return ast


def BuildAst(grammarDescription, axiom, tokenList):
    return AstBuilder(grammarDescription, tokenList, axiom).build()
    
