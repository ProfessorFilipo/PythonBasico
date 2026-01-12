####################################################
###                                              ###
###   interpretador de expressões matemáticas    ###
###                                              ###
####################################################
### Prof. Filipo Mor                             ###
####################################################
### github.com/ProfessorFilipo                   ###
####################################################

import ast
import operator

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
    Avalia a expressão matemática fornecida.
    """
    try:
        # Analisa a expressão para uma árvore sintática abstrata (AST)
        tree = ast.parse(expr, mode='eval')

        # Avalia o AST
        return eval_(tree.body)
    except Exception as e:
        return str(e)


def eval_(node):
    """
    Avalia nós de uma árvore sintática abstrata (AST).
    """
    if isinstance(node, ast.Constant):  # Se for um número ou constante
        return node.value
    elif isinstance(node, ast.BinOp):  # Se for uma operação binária (ex.: 1 + 2)
        left = eval_(node.left)
        right = eval_(node.right)
        return OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):  # Se for um operador unário (ex.: -1)
        operand = eval_(node.operand)
        return OPERATORS[type(node.op)](operand)
    else:
        raise TypeError(node)


# Exemplo de uso
#equation = "3 + 5 * (2 - 4)**2 / 2"
equation = "(4 * (2**2)**(1/2))"
result = eval_expr(equation)
print(f"O resultado da equacao '{equation}' eh {result}")
