import re

# Define token types and patterns
TOKENS = [
    ('WHITESPACE', r'\s+'),  # Whitespace (ignored but important for separating tokens)
    ('COMMENT', r'\/\*[^*]*\*+([^/*][^*]*\*+)*\/'),  # CSS comments
    ('AT_RULE', r'@[a-zA-Z]+[^{]*'),  # At-rules like @media, @keyframes (simplified)
    ('SELECTOR', r'[^{}]+(?=\s*\{)'),  # CSS selectors 
    ('BRACE_OPEN', r'\{'),  # Opening brace
    ('BRACE_CLOSE', r'\}'),  # Closing brace
    ('PROPERTY', r'[-_a-zA-Z]+(?=\s*:)'),  # CSS properties, improved to ensure it ends before a colon
    ('FUNCTION', r'[-a-zA-Z0-9]+(?=\()'),  # Function names
    ('FUNCTION_ARGS', r'\([^)]+\)'),  # Arguments within a function
    ('VALUE', r'[^;{}:]+(?=;|\})'),  # General values, stop ats semicolon or closing brace
    ('COLON', r':'),  # Colon
    ('SEMICOLON', r';'),  # Semicolon (terminates a declaration)
    ('COMMA', r','),  # Comma
]

# Lexer function
def lexer(css):
    tokens = []
    while css:
        css = css.strip()  # Remove leading and trailing whitespace
        match_found = False
        for token_type, token_regex in TOKENS:
            regex = re.compile(token_regex)
            match = regex.match(css)
            if match:
                value = match.group(0).strip()  # Strip leading/trailing whitespace from the matched value
                if token_type != 'WHITESPACE' and token_type != 'COMMENT':  # Skip whitespace and comments
                    tokens.append((token_type, value))
                css = css[match.end():]  # Remove the matched part from the beginning
                match_found = True
                break  # Exit the for loop since we found a match
        if not match_found:
            raise SyntaxError(f'Unknown CSS: {css}')
    return tokens

# Read CSS content from a file
with open('Lab3/style.css', 'r') as file:
    css_content = file.read()

# Lexing the CSS content from the file
tokens = lexer(css_content)
print(f'{"Token Type":<20} | {"Token Value":<50}')
print('-' * 73) 
for token_type, token_value in tokens:
    print(f'{token_type:<20} | {token_value:<50}')

