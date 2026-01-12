####################################################
###                                              ###
###   interpretador de expressões matemáticas    ###
### sem uso de bibliotecas para tokenizacao      ###
### gera um PNG com a AST, expressao e resultado ###
####################################################
### Prof. Filipo Mor                             ###
####################################################
### github.com/ProfessorFilipo                   ###
####################################################

import graphviz
import os
os.environ['PATH'] += r';D:\Aplicativos\Graphviz\bin' # ajustei o path na mao grande

class Node:
    def __init__(self, value, type=''):
        self.value = value
        self.type = type
        self.left = None
        self.right = None

def tokenize(expression):
    tokens = []
    current_number = ""
    for char in expression:
        if char.isdigit() or char == '.':
            current_number += char
        elif char in "+-*/()^":  # Adicionado '^' para exponenciação
            if current_number:
                tokens.append(current_number)
                current_number = ""
            tokens.append(char)
        elif char.isspace():
            continue
        else:
            raise ValueError("Caractere inválido: {}".format(char))
    if current_number:
        tokens.append(current_number)
    return tokens

def build_ast(tokens):
    # Converte a notação infixa para posfixa (Reverse Polish Notation - RPN)
    def infix_to_postfix(tokens):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output = []
        operators = []

        for token in tokens:
            if token.isdigit() or '.' in token:
                output.append(token)
            elif token in '+-*/^':
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Remove o '('

        while operators:
            output.append(operators.pop())
        return output

    postfix_tokens = infix_to_postfix(tokens)

    # Constrói a AST a partir da notação posfixa
    stack = []
    for token in postfix_tokens:
        if token.isdigit() or '.' in token:
            node = Node(float(token), 'number')
            stack.append(node)
        elif token in '+-*/^':
            node = Node(token, 'operator')
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)

    return stack[0] if stack else None

def evaluate_ast(node):
    if node.type == 'number':
        return node.value
    elif node.type == 'operator':
        left_val = evaluate_ast(node.left)
        right_val = evaluate_ast(node.right)
        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            if right_val == 0:
                raise ValueError("Divisão por zero!")
            return left_val / right_val
        elif node.value == '^':
            return left_val ** right_val
    return 0

def build_graph(node, dot):
    node_id = str(id(node))
    label = f"{node.value}"
    dot.node(node_id, label=label)

    if node.left:
        left_id = build_graph(node.left, dot)
        dot.edge(node_id, left_id)
    if node.right:
        right_id = build_graph(node.right, dot)
        dot.edge(node_id, right_id)

    return node_id

def generate_graph_image(ast_root, expression, result, filename="arvore_abstrata_sintaxe"):
    dot = graphviz.Digraph(comment='AST',
                           graph_attr={'label': f'Expressão: {expression}',
                                       'labelloc': 't',
                                       'fontsize': '20',
                                       'rankdir': 'TB'})

    build_graph(ast_root, dot)

    # Adiciona um nó para o resultado
    result_node_id = "resultado"
    dot.node(result_node_id, label=f"Resultado: {result}", shape="box", fontsize="16")

    # Adiciona uma aresta invisível para conectar o grafo principal ao nó de resultado
    dot.edge(str(id(ast_root)), result_node_id, style="invis", constraint="true")

    dot.render(filename, format='png', cleanup=True)
    return filename + ".png"

# Exemplo de uso
#expression = "3 + 5 * (2 - 4.5)^2 / 2"  # Adicionando exponenciação
expression = "2 + ( 5 * (2^2)^(1/2))*34+15*(27^(1/3))"
tokens = tokenize(expression)
ast_root = build_ast(tokens)
result = evaluate_ast(ast_root)
graph_file = generate_graph_image(ast_root, expression, result)

print(f"Expressão: {expression}")
print(f"Resultado: {result}")
print(f"Grafo salvo em: {graph_file}")
