from pseudocode_scanner import Tokenize
import graphviz
from dsl_token import *
from syntax import *
import pathlib
import os
import dsl_info
import json

def __RenderTokenStream(diagramName, tokenList, debugInfoDir):
    if debugInfoDir is None:
        return
    h = graphviz.Digraph(diagramName, format='png')
    h.node('0', '', shape='point')
    i = 1
    for token in tokenList:
        if Token.Type.TERMINAL == token.type:
            h.node(str(i),
                   f"TERMINAL\ntype: {token.terminalType.name}\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""),
                   shape='diamond')
        elif Token.Type.KEY == token.type:
            h.node(str(i), f"KEY\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""), shape='oval')
        h.edge(str(i - 1), str(i))
        i += 1
    h.node(str(i), '', shape='point')
    h.edge(str(i - 1), str(i))
    h.render(directory=debugInfoDir, view=False)

def __RenderAst(diagramName, ast, debugInfoDir):
    if debugInfoDir is None:
        return
    h = graphviz.Digraph(diagramName, format='png')
    i = 1
    nodes = [(ast, 0)]
    while len(nodes):
        node = nodes[0]
        if TreeNode.Type.NONTERMINAL == node[0].type:
            h.node(str(i),
                   f"NONTERMINAL\ntype: {node[0].nonterminalType}" + (f"\nattribute: {node[0].attribute}" if node[0].attribute else ""),
                   shape='box')
            if node[1] != 0:
                h.edge(str(node[1]), str(i))
            nodes += [(child, i) for child in node[0].childs]
        else:
            token = node[0].token
            if Token.Type.TERMINAL == token.type:
                h.node(str(i),
                       f"TERMINAL\ntype: {token.terminalType.name}\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""),
                       shape='diamond')
            elif Token.Type.KEY == token.type:
                h.node(str(i), f"KEY\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""), shape='oval')
            h.edge(str(node[1]), str(i))
        nodes = nodes[1:]
        i += 1
    h.render(directory=debugInfoDir, view=False)
    
class ASTEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TreeNode):
            node: TreeNode= obj
            if TreeNode.Type.NONTERMINAL == node.type:
                return {'nonterm': node.nonterminalType.name, 'content': node.childs}
            else:
                token = node.token
                if Token.Type.TERMINAL == token.type:
                    return {'term': token.terminalType.name, 'value': token.str}
                elif Token.Type.KEY == token.type:
                    return {'key': token.str}
            
        return json.JSONEncoder.default(self, obj)


def process(code, syntaxInfo, debugInfoDir=None):

    if not debugInfoDir is None:
        debugInfoDir = pathlib.Path(debugInfoDir)
        if not debugInfoDir.exists():
            os.mkdir(debugInfoDir)
    syntaxDesription = GetSyntaxDesription(syntaxInfo)
    tokenList = Tokenize(code)
    __RenderTokenStream('token_stream_after_scanner', tokenList, debugInfoDir)
    ast = BuildAst(syntaxDesription, dsl_info.axiom, tokenList)
    __RenderAst('ast', ast, debugInfoDir)
    return (ASTEncoder().encode(ast))



if __name__ == "__main__":
    syntaxInfo = {
        "type": "virt",
        "info": {
            "supportInfo": "_examples/pseudocode/pseudocode.sgi",
            "diagrams": "_examples/pseudocode"
        }
    }
    code ='''return B
return G
func GetSet (n) -> @@comment{"Множество $B$ целых чисел от $2$ до $n$"}
    return B
    return B
    return B
    return B; return B
end algorithm
@@comment{"Множество $B$ целых чисел от $2$ до $n$"}
return B
return G
return B
func GetSet (n) -> @@comment{"Множество $B$ целых чисел от $2$ до $n$"}
    return B
end algorithm'''
    print(process(code, syntaxInfo, "other"))



