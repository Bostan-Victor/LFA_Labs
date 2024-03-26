import random


# Function to generate strings based on provided regular expression patterns
def generate_strings(reg_exp, n, limit):
    strings = []  # List to store the generated strings

    for i in range(n):
        string = ''  # Initialize the string to be built
        # Iterate through each token in the regular expression
        for tup in reg_exp:
            if tup[0] == '1':  # '1' denotes a mandatory symbol
                string += random.choice(tup[1])
            elif tup[0] == '?':  # '?' denotes an optional symbol
                nr = random.randint(0, 1)
                if nr:
                    string += random.choice(tup[1])
            elif tup[0] == '5':  # '5' denotes a symbol repeated exactly 5 times
                char = random.choice(tup[1])
                for j in range(5):
                    string += char
            elif tup[0] == '+':  # '+' denotes one or more repetitions of a symbol
                char = random.choice(tup[1])
                nr_of_chars = random.randint(1, limit)
                for j in range(nr_of_chars):
                    string += char
            else:  # For other types, assume '*', denoting zero or more repetitions
                char = random.choice(tup[1])
                nr_of_chars = random.randint(0, limit)
                for j in range(nr_of_chars):
                    string += char

        strings.append(string)

    return strings


# Function to generate a string with a step-by-step explanation
def generate_string_with_explanation(exp, reg_exp, n, limit):
    string = ''
    step = 1  # Step counter for explanation
    print(f'\nGenerating a string for Regular Expression {exp}:\n')
    print(f'Step-by-step explenation:')
    
    for tup in reg_exp:
        l = len(tup[1])  # Get the number of options for the current component
        if tup[0] == '1':
            string += random.choice(tup[1])
            if l == 1:
                print(f'Step {step}. Append 1 instance of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(f'Step {step}. Append 1 instance of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        elif tup[0] == '?':
            nr = random.randint(0, 1)
            print(f'Step {step}. Generate a random number between 0 and 1 to determine if a symbol is going to be appended. Generated number = {nr}')
            step += 1
            if nr:
                string += random.choice(tup[1])
                if l == 1:
                    print(f'Step {step}. Append 1 instance of the symbol "{tup[1][0]}". String = {string}')
                    step += 1
                else:
                    print(f'Step {step}. Append 1 instance of one of these symbols - {", ".join(tup[1])}. String = {string}')
                    step += 1
            else:
                print(f'Step {step}. Nothing is being appended. String = {string}')
                step += 1
        elif tup[0] == '5':
            char = random.choice(tup[1])
            for j in range(5):
                string += char
            if l == 1:
                print(f'Step {step}. Append 5 instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(f'Step {step}. Append 5 instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        elif tup[0] == '+':
            char = random.choice(tup[1])
            nr_of_chars = random.randint(1, limit)
            print(f"Step {step}. Generate how many symbols will be appended between 1 and the limit, which is {limit}. In this case we append {nr_of_chars} symbols")
            step += 1
            for j in range(nr_of_chars):
                string += char
            if l == 1:
                print(f'Step {step}. Append {nr_of_chars} instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(f'Step {step}. Append {nr_of_chars} instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        else:
            char = random.choice(tup[1])
            nr_of_chars = random.randint(0, limit)
            print(f'Step {step}. Generate how many symbols will be appended between 0 and the limit, which is {limit}. In this case we append {nr_of_chars} symbols')
            step += 1
            for j in range(nr_of_chars):
                string += char
            if l == 1:
                print(f'Step {step}. Append {nr_of_chars} instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(f'Step {step}. Append {nr_of_chars} instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1

    print(f'\nThe resulting string is: {string}')


# Define example regular expressions and their tokenized forms
reg_expressions = [
    '(a|b)(c|d)E⁺G?',
    'P(Q|R|S)T(UV|W|X)*Z⁺',
    '1(0,1)*2(3|4)⁵36'
]
reg_expressions_tokens = [  # Regular expressions tokens
    [('1', ['a', 'b']), ('1', ['c', 'd']), ('+', ['E']), ('?', ['G'])],
    [('1', ['P']), ('1', ['Q', 'R', 'S']), ('1', ['T']), ('*', ['UV', 'W', 'X']), ('+', ['Z'])],
    [('1', ['1']), ('*', ['0', '1']), ('1', ['2']), ('5', ['3', '4']), ('1', ['36'])]
]
limit = 5  # Limit for symbols written an undefined number of times
n = 5  # Number of strings to generate

for i in range(len(reg_expressions_tokens)):
    print(f'{n} random strings for Regular Expression {reg_expressions[i]}:')
    print(generate_strings(reg_expressions_tokens[i], n, limit), '\n')

generate_string_with_explanation(reg_expressions[1], reg_expressions_tokens[1], n, limit)
