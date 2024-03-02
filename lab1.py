import random
from Grammar import GenericGrammar
from FiniteAutomaton import GenericFiniteAutomaton


class Grammar(GenericGrammar):
    def generate_strings(self):
        results = []
        while len(results) < 5:
            str = self.S
            str = str.replace('S', random.choice(self.P[self.S]))

            while any(nt in str for nt in self.Vn):
                for nt in self.Vn:
                    if nt in str:
                        str = str.replace(nt, random.choice(self.P[nt]), 1)
                        break
            if str not in results:
                results.append(str)

        return results
    
    def to_finite_automaton(self):
        states = self.Vn + ['X'] # Add accept state X
        alphabet = self.Vt
        transition_function = {}
        transition_function['X'] = {}
        start = self.S
        accept = ['X']

        for non_terminal in self.Vn:
            transition_function[non_terminal] = {}
            for production in self.P.get(non_terminal, []):
                if len(production) == 1: # Terminal symbol leading to accept state
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2: #Terminal symbol followed by a non-terminal
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)
    
    def classify(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # Check for Type 3 (Regular Grammar)
                if not (len(rhs) == 1 and rhs in self.Vt) and not (len(rhs) == 2 and rhs[0] in self.Vt and rhs[1] in self.Vn):
                    is_regular = False
                # Check for Type 2 (Context-Free Grammar)
                if len(lhs) != 1 or not lhs.isupper():
                    is_context_free = False
                # Check for Type 1 (Context-Sensitive Grammar)
                if len(rhs) < len(lhs):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"
    

class FiniteAutomaton(GenericFiniteAutomaton):
    def is_word_accepted(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept


if __name__ == "__main__":
    vn = ['S', 'P', 'Q']
    vt = ['a', 'b', 'c', 'd', 'e', 'f']
    p = {
        'S': ['aP', 'bQ'],
        'P': ['bP', 'cP', 'dQ', 'e'],
        'Q': ['eQ', 'fQ', 'a']
    }
    s = 'S'

    grammar = Grammar(vn, vt, p, s)

    generated_words = grammar.generate_strings()
    print("\nGenerated strings using the grammar from variant 1:")
    print(generated_words)
    print()

    print("\nCheck if the 5 words generated were obtained correctly:")
    for i in generated_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()

    print("\nCheck if random words are evaluated correctly:")
    random_words = ['random', 'VictorBostan10LaLaborator', 'LFAIsCool', 'aecfafafac']
    for i in random_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()

    print(grammar.classify())

