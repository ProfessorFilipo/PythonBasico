####################################################
###                                              ###
###   interpretador de expressões matemáticas    ###
### COM uso de bibliotecas para tokenizacao      ###
####################################################
### Prof. Filipo Mor                             ###
####################################################
### github.com/ProfessorFilipo                   ###
####################################################

import ast
import operator
import graphviz
import os
os.environ['PATH'] += r';D:\Aplicativos\Graphviz\bin' #ajuste do path na mão

# Dicionário para mapear operadores de AST a funções correspondentes
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def eval_expr(expr):
    """
    Avalia a expressão matemática, gera grafo da AST com valores nos nós,
    e retorna o resultado e o nome do arquivo PNG gerado.
    """
    try:
        tree = ast.parse(expr, mode='eval')
        dot = graphviz.Digraph(comment='AST')
        build_graph(tree.body, dot)
        filename = 'ast_graph'
        dot.render(filename, format='png', cleanup=True)
        result = eval_(tree.body)
        return result, filename + '.png'
    except Exception as e:
        return str(e), None


def build_graph(node, dot):
    """
    Constrói o grafo da AST, incluindo o valor de cada nó.
    Retorna o id do nó criado.
    """
    node_id = str(id(node))
    label = ''

    if isinstance(node, ast.Constant):
        # Exibir tipo e valor de forma clara
        label = f'{type(node.value).__name__} ({node.value})'
        dot.node(node_id, label)
    elif isinstance(node, ast.BinOp):
        # Mostrar somente o nome do operador
        op_type = type(node.op).__name__
        label = f'{op_type}\n({operator_symbol(node.op)})'
        dot.node(node_id, label)
        # Recursivamente constrói os nós filhos
        left_id = build_graph(node.left, dot)
        right_id = build_graph(node.right, dot)
        # Conectar os filhos ao operador
        dot.edge(node_id, left_id)
        dot.edge(node_id, right_id)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op).__name__
        label = f'{op_type}\n({operator_symbol(node.op)})'
        dot.node(node_id, label)
        operand_id = build_graph(node.operand, dot)
        dot.edge(node_id, operand_id)
    else:
        label = type(node).__name__
        dot.node(node_id, label)
    return node_id


def operator_symbol(op):
    """
    Retorna o símbolo do operador.
    """
    symbol_map = {
        ast.Add: '+',
        ast.Sub: '-',
        ast.Mult: '*',
        ast.Div: '/',
        ast.Mod: '%',
        ast.Pow: '**',
        ast.USub: '-',
    }
    return symbol_map.get(type(op), '?')


def eval_(node):
    """
    Avalia o valor do nó para uso nos rótulos.
    """
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = eval_(node.left)
        right = eval_(node.right)
        return OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = eval_(node.operand)
        return OPERATORS[type(node.op)](operand)
    else:
        raise TypeError(node)


# Exemplo de uso
expressao = "3 + 5 * (2 - 4.5)**2 / 2"
resultado, arquivo_grafo = eval_expr(expressao)
print(f"Expressão: {expressao}")
print(f"Resultado: {resultado}")
if arquivo_grafo:
    print(f"Árvore em grafo salvo como: {arquivo_grafo}")
