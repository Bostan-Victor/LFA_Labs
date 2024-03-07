import networkx as nx
import matplotlib.pyplot as plt
from Grammar import GenericGrammar
from FiniteAutomaton import GenericFiniteAutomaton


class FiniteAutomaton(GenericFiniteAutomaton):
    def fa_to_grammar(self):
        vn = self.states
        vt = self.alphabet
        s = self.start
        p = {state: [] for state in vn}

        for nt, vals in self.transition_function.items():
            for terminal, vals2 in vals.items():
                for i in vals2:
                    # Check if the current state is in the set of accept states
                    if i in self.accept:
                        p[nt].append(terminal)
                    else:
                        production = terminal + i
                        p[nt].append(production)

        return GenericGrammar(vn, vt, p, s)

    
    def nfa_to_dfa(self):
        # Initialize the list of states to process and the set of all created DFA states
        initial_state = frozenset([self.start])
        states_to_process = [initial_state]
        dfa_states = {initial_state}
        # Initialize the DFA transition function and the set of DFA's accept states
        dfa_transitions = {}
        dfa_accept = set()

        while states_to_process:
            current_state = states_to_process.pop()
            dfa_transitions[current_state] = {}  # Create an entry in the DFA transition function for the current state

            for symbol in self.alphabet:
                # Find the union of NFA states reachable from the current NFA states under the current symbol
                next_state = frozenset(
                    sum(
                        [self.transition_function.get(nfa_state, {}).get(symbol, []) for nfa_state in current_state],
                        []
                    )
                )

                # Only add the transition if the next state is not empty
                if next_state:
                    dfa_transitions[current_state][symbol] = next_state

                    # If this set of states is new, add it to the states we need to process
                    if next_state not in dfa_states:
                        dfa_states.add(next_state)
                        states_to_process.append(next_state)
                        
                    # If the new state includes any NFA accept states, add it to the DFA accept states
                    if next_state & set(self.accept):
                        dfa_accept.add(next_state)

        # Convert state sets to strings to make them more readable
        state_names = {state: ''.join(sorted(state)) for state in dfa_states}
        dfa_transitions_named = {
            state_names[state]: {symbol: state_names[next_state] for symbol, next_state in transitions.items()}
            for state, transitions in dfa_transitions.items()
        }
        dfa_states_named = set(state_names.values())
        dfa_accept_named = {state_names[state] for state in dfa_accept}
        dfa_start_named = state_names[initial_state]

        # Make the transitions lists
        for state in dfa_states_named:
            for key, val in dfa_transitions_named[state].items():
                dfa_transitions_named[state][key] = [val]

        # Return the new DFA
        return FiniteAutomaton(dfa_states_named, self.alphabet, dfa_transitions_named, dfa_start_named, dfa_accept_named)
    
    def check_fa(self):
        is_dfa = True

        for _, transitions in self.transition_function.items():
            for _, list in transitions.items():
                if len(list) > 1:
                    is_dfa = False
                    break

        if is_dfa:
            print("\nThis is a DFA!\n")
        else:
            print("\nThis is a NFA!\n")

    def create_graph(self):
        G = nx.DiGraph()  # Directed graph for finite automaton

        # Add states as nodes
        for state in self.states:
            G.add_node(state)

        # Add transitions as edges
        for state, transitions in self.transition_function.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    G.add_edge(state, next_state, label=symbol)

        # Graph layout
        pos = nx.spring_layout(G)  # positions for all nodes, spring layout

        # Drawing
        plt.figure(figsize=(8, 8))  # Increase figure size for better visibility
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=14)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Manually adjust and draw labels for self-loops
        for node, (x, y) in pos.items():
            for neighbor in G.neighbors(node):
                if node == neighbor:  # This means we have a self-loop
                    label = edge_labels[(node, neighbor)]
                    # Adjust these values to move the label around the self-loop as needed
                    loop_label_pos = (x, y + 0.2)  
                    plt.text(loop_label_pos[0], loop_label_pos[1], label, size=10, ha='center', va='center')

        plt.axis('off')  # Hide axes
        plt.show()  # Display the graph


if __name__ == "__main__":
    states = ['S', 'A', 'B', 'C']
    alphabet = ['a', 'c', 'b']
    transition_function = {
        'S': {'a': ['S', 'A']},  # δ(S,a) = S, δ(S,a) = A
        'A': {'c': ['A'], 'b': ['B']},  # δ(A,c) = A, δ(A,b) = B
        'B': {'b': ['C']},  # δ(B,b) = C
        'C': {'a': ['A']}  # δ(C,a) = A
    }
    start = 'S'
    accept = ['B']

    FA = FiniteAutomaton(states, alphabet, transition_function, start, accept)
    #FA.fa_to_grammar().print_grammar()
    #FA.check_fa()
    DFA = FA.nfa_to_dfa()
   # DFA.print_automaton()
   # DFA.check_fa()
    DFA.fa_to_grammar().print_grammar()
    #FA.create_graph()
    #DFA.create_graph()
