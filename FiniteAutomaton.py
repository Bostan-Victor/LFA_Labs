

class GenericFiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def print_automaton(self):
        print('States:', self.states)
        print('Alphabet:', self.alphabet)
        print('Transition function:', self.transition_function)
        print('Start state:', self.start)
        print('Accept state:', self.accept, '\n')
