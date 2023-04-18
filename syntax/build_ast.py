from dsl_token import *
from syntax.core import *


class TreeNode:
    class Type(Enum):
        TOKEN = 0
        NONTERMINAL = 1


    def __init__(self, type):
        self.type = type
        self.attribute = None


def __BuildAstNonterm(grammarDescription, tokenList, childs, commands, pos, nonterminal, end):
    node = grammarDescription[nonterminal]
    newToken = tokenList[pos]
    for rule_index, rule in enumerate(node.nextNodes):
        success, new_pos = __BuildAstPoint(grammarDescription, tokenList, childs, commands, pos, node, rule_index, end)
        if success:
            return True, new_pos
    return False, pos


def __BuildAstPoint(grammarDescription, tokenList, childs, commands, pos, node, rule_index, end):
    
    start_childs_len = len(childs)
    start_commands_len = len(commands)
    rule = node.nextNodes[rule_index]
    newNonterm = None

    if pos >= end:
        if NodeType.END == rule[0].type:
            commands.append(rule[1])
            return True, pos
        else:
            return False, pos
    newToken = tokenList[pos]
    if NodeType.END == rule[0].type:
        commands.append(rule[1])
        return True, pos
    elif NodeType.KEY == rule[0].type and Token.Type.KEY == newToken.type and newToken.str == rule[0].str:
        element = TreeNode(TreeNode.Type.TOKEN)
        element.attribute = newToken.attribute
        element.token = newToken
        childs.append(element)
        commands.append(rule[1])
        pos += 1
        node = rule[0]
    elif NodeType.TERMINAL == rule[0].type and Token.Type.TERMINAL == newToken.type and newToken.terminalType == rule[0].terminal:
        element = TreeNode(TreeNode.Type.TOKEN)
        element.attribute = newToken.attribute
        element.token = newToken
        childs.append(element)
        commands.append(rule[1])
        pos += 1
        node = rule[0]
    elif NodeType.NONTERMINAL == rule[0].type:
        if rule[0].nonterminal not in grammarDescription:
            raise Exception(f"Failed to find '{rule[0].nonterminal}' description")
        newNonterm = TreeNode(TreeNode.Type.NONTERMINAL)
        newNonterm.nonterminalType = rule[0].nonterminal
        newNonterm.childs = []
        newNonterm.commands = []
        childs.append(newNonterm)
        commands.append(rule[1])
        node = rule[0]
    else:
        return False, pos
    
    if newNonterm:
        success, new_pos = __BuildAstNonterm(grammarDescription, tokenList, newNonterm.childs, newNonterm.commands, pos, newNonterm.nonterminalType, end)
        if success:
            pos = new_pos
            for rule_index, rule in enumerate(node.nextNodes):
                success, new_pos = __BuildAstPoint(grammarDescription, tokenList, childs, commands, pos, node, rule_index, end)
                if success:
                    return True, new_pos
            
    else:
        for rule_index, rule in enumerate(node.nextNodes):
            success, new_pos = __BuildAstPoint(grammarDescription, tokenList, childs, commands, pos, node, rule_index, end)
            if success:
                return True, new_pos
            
    
    while len(childs) > start_childs_len:
        childs.pop()
    while len(commands) > start_commands_len:
        commands.pop()
    return False, pos
    
    



def __BuildAstElement(grammarDescription, nonterminal, tokenList, start, end):
    if nonterminal not in grammarDescription:
        raise Exception(f"Failed to find '{nonterminal}' description")
    pos = start
    result = TreeNode(TreeNode.Type.NONTERMINAL)
    result.nonterminalType = nonterminal
    result.childs = []
    result.commands = []
    returns = 0
    node = grammarDescription[nonterminal]
    state_stack = [{'returns': 0, 'pos': pos, 'childs_count': 0, 'commands_count': 0, 'node': node}]
    while pos < end and NodeType.END != node.type:
        newToken = tokenList[pos]
        exit = None
        success = False
        for i in range(returns, len(node.nextNodes)):
            next = node.nextNodes[i]
            if NodeType.END == next[0].type:
                exit = next
                continue
            if NodeType.KEY == next[0].type and Token.Type.KEY == newToken.type and newToken.str == next[0].str:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                result.childs.append(element)
                result.commands.append(next[1])
                pos += 1
                node = next[0]
                success = True
                break
            if NodeType.TERMINAL == next[0].type and Token.Type.TERMINAL == newToken.type and newToken.terminalType == next[0].terminal:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                result.childs.append(element)
                result.commands.append(next[1])
                pos += 1
                node = next[0]
                success = True
                break
            if NodeType.NONTERMINAL == next[0].type:
                try:
                    res = __BuildAstElement(grammarDescription, next[0].nonterminal, tokenList, pos, end)
                    pos = res[1]
                    result.childs.append(res[0])
                    result.commands.append(next[1])
                    node = next[0]
                    success = True
                except Exception:
                    continue
                break
        if success:
            state_stack.append({'returns': 0, 'pos': pos, 'childs_count': len(result.childs), 'commands_count': len(result.commands), 'node': node})
            continue
        if exit:
            node = exit[0]
            result.commands.append(exit[1])
        else:
            while len(state_stack) != 0:
                state_stack[-1]['returns'] += 1
                if state_stack[-1]['returns'] == len(state_stack[-1]['node'].nextNodes):
                    state_stack.pop()
                else:
                    break
            if len(state_stack) != 0:
                returns = state_stack[-1]['returns']
                pos = state_stack[-1]['pos']
                while len(result.childs) > state_stack[-1]['childs_count']:
                    result.childs.pop()
                while len(result.commands) > state_stack[-1]['commands_count']:
                    result.commands.pop()
                node = state_stack[-1]['node']
            else:
                raise Exception(f"Failed to process token '{newToken.str}'")
    return result, pos


def BuildAst(grammarDescription, axiom, tokenList):
    ast = TreeNode(TreeNode.Type.NONTERMINAL)
    ast.nonterminalType = axiom
    ast.childs = []
    ast.commands = []
    success, new_pos = __BuildAstNonterm(grammarDescription, tokenList, ast.childs, ast.commands, 0, ast.nonterminalType, len(tokenList))
    if success:
        return ast
    else:
        raise Exception(f"Fail")
    
