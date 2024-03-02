

class GenericGrammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def print_grammar(self):
        print('Vn:', self.Vn)
        print('Vt:', self.Vt)
        print('P: ', self.P)
        print('S: ', self.S, '\n')
        