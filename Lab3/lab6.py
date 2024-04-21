import re
import enum
from graphviz import Digraph

# Define the TokenType using an enumeration for clarity and robustness
class TokenType(enum.Enum):
    WHITESPACE = 1
    COMMENT = 2
    AT_RULE = 3
    SELECTOR = 4
    BRACE_OPEN = 5
    BRACE_CLOSE = 6
    PROPERTY = 7
    FUNCTION = 8
    FUNCTION_ARGS = 9
    VALUE = 10
    COLON = 11
    SEMICOLON = 12
    COMMA = 13

# Lexer function to tokenize the input CSS content
def lexer(css):
    tokens = []
    while css:
        css = css.strip()
        match_found = False
        for token_type, token_regex in TOKENS:
            regex = re.compile(token_regex)
            match = regex.match(css)
            if match:
                value = match.group(0).strip()
                if token_type != TokenType.WHITESPACE and token_type != TokenType.COMMENT:
                    tokens.append((token_type, value))
                css = css[match.end():]
                match_found = True
                break
        if not match_found:
            raise SyntaxError(f'Unknown CSS: {css}')
    return tokens

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, enum.Enum) else self.type
        return f"{type_name}({self.value}, {self.children})"

# Parser function to build AST from tokens
def parse(tokens):
    root = ASTNode(TokenType.SELECTOR, value="ROOT")  # Use enum for ROOT
    current_node = root

    i = 0
    while i < len(tokens):
        token_type, value = tokens[i]
        if token_type == TokenType.SELECTOR:
            current_node = ASTNode(token_type, value=value)
            root.children.append(current_node)
        elif token_type == TokenType.PROPERTY:
            property_node = ASTNode(token_type, value=value)
            current_node.children.append(property_node)
            # Expecting a VALUE token next
            if i+2 < len(tokens) and tokens[i+2][0] == TokenType.VALUE:
                value_node = ASTNode(tokens[i+2][0], value=tokens[i+2][1])
                property_node.children.append(value_node)
                i += 2  # Move past the VALUE token
        i += 1

    return root

def add_nodes_edges(tree, graph=None):
    if graph is None:
        graph = Digraph()
        # Include both the type and value in the label for the root node
        graph.node(name=str(id(tree)), label=f'{tree.type.name}({tree.value})')

    for child in tree.children:
        # Include both the type and value in the label for each child node
        child_label = f'{child.type.name}({child.value})' if child.value else child.type.name
        graph.node(name=str(id(child)), label=child_label)
        graph.edge(str(id(tree)), str(id(child)))
        graph = add_nodes_edges(child, graph)

    return graph

TOKENS = [
    (TokenType.WHITESPACE, r'\s+'),
    (TokenType.COMMENT, r'\/\*[^*]*\*+([^/*][^*]*\*+)*\/'),
    (TokenType.AT_RULE, r'@[a-zA-Z]+[^{]*'),
    (TokenType.SELECTOR, r'[^{}]+(?=\s*\{)'),
    (TokenType.BRACE_OPEN, r'\{'),
    (TokenType.BRACE_CLOSE, r'\}'),
    (TokenType.PROPERTY, r'[-_a-zA-Z]+(?=\s*:)'),
    (TokenType.FUNCTION, r'[-a-zA-Z0-9]+(?=\()'),
    (TokenType.FUNCTION_ARGS, r'\([^)]+\)'),
    (TokenType.VALUE, r'[^;{}:]+(?=;|\})'),
    (TokenType.COLON, r':'),
    (TokenType.SEMICOLON, r';'),
    (TokenType.COMMA, r','),
]

with open('Lab3/style.css', 'r') as file:  
    css_content = file.read()

tokens = lexer(css_content)
ast = parse(tokens)
graph = add_nodes_edges(ast)
graph.render('ast', view=True)  # Generates a PDF and opens it
