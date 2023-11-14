white_space = ["\r","\n","\t","\f","\v"]
#symobols execpt equals
SEE = ["(",")","{","}","[","]","+","-","*",",",":",";","<"]
digits = ["0","1","2","3","4","5","6","7","8","9"]
symbol  = ["(",")","{","}","[","]","+","-","*","=","/",",",":",";","<"]
lower_case_alphabet =  list("abcdefghijklmnopqrstuvwxyz")
upper_case_alphabet  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
all_alphabets = lower_case_alphabet + upper_case_alphabet

class DFA:
    def __init__(self):

        self.start_state = None
        self.accept_states = set()
        self.marked_accept_states = set()
        # accepts with star in dfa
        self.current_state = None
        self.states = set()
        self.alphabet = set()
        self.transitions = {}  


    def add_state(self, state, is_start=False, is_accept=False , is_marked_accept = False):
        self.states.add(state)
        if is_start:
            self.start_state = state
            self.current_state = state
        if is_accept:
            self.accept_states.add(state)
        if is_marked_accept:
            self.marked_accept_states.add(state)

    def process_input(self, input_string):
        self.current_state = self.start_state
        for symbol in input_string:
            if symbol in self.alphabet:
                 
                self.current_state = self.transitions[self.current_state][symbol]


                if ( self.current_state in self.accept_states) :
                    #todo
                    pass

                if ( self.current_state in self.marked_accept_states ):

                    #todo
                    pass

                
            else:
                return False  
            
        
            
        return


    def make_transition(self, src_state, input_symbol, dest_state):
        if src_state not in self.transitions:
            self.transitions[src_state] = {}
        self.transitions[src_state][input_symbol] = dest_state
        self.alphabet.add(input_symbol)


    def is_accept_state(self):
        return self.current_state in self.accept_states






    def add_mini_dfa(self, mini_dfa_transitions, start_offset):
        """
        Adds a mini DFA to the current DFA.
        :param mini_dfa_transitions: A dictionary representing the transitions of the mini DFA.
        :param start_offset: The starting offset for the state IDs in the mini DFA.
        """
        for src, transitions in mini_dfa_transitions.items():
            src_state = start_offset + src
            self.add_state(src_state)

            for input_symbol, dest in transitions.items():
                if isinstance(dest, tuple):
                    dest_state, is_accept, is_marked_accept = dest
                    self.add_state(start_offset + dest_state, is_accept=is_accept, is_marked_accept=is_marked_accept)
                else:
                    dest_state = dest

                self.make_transition(src_state, input_symbol, start_offset + dest_state)




# NUM states and transitions:
# number of nodes = 3 
# 0 - Digit -> 1
# 1 - Digit -> 1
# 1 - ^Digit -> 2*a

# ID states and transitions:
# number of nodes = 3 
# 0 - Alpha -> 1
# 1 - AlphaDigit -> 1
# 1 - ^AlphaDigit -> 2*a

# KEYWORD states and transitions:
# number of nodes = 3 
# 0 - Alpha -> 1
# 1 - alpha -> 1
# 1 - ^alpha -> 2*a

# SYMBOL states and transitions:
# number of nodes = 3 
# 0 - = -> 1
# 1 - = -> 2a
# 1 - ^= -> 3*a
# 0 - SEE -> 4a
# 0 - / -> 5
# 5 - ^/* -> 6a

# WHITESPACE states and transitions:
#number of nodes = 3
# 0 - Whitespace -> 1
# 1 - Whitespace -> 1
# 1 - ^Whitespace -> 2*a

#COMMENT states and transitions:
#number of nodes = 3
# 0 - / -> 1
# 1 - * -> 2
# 2 - * -> 3
# 2 - ^* -> 2
# 3 - ^*/ -> 2
# 3 - * -> 3
# 3 - / -> 4*a


def add_token_states(dfa):

        num_dfa = {
            0: {'Digit': 1},
            1: {'Digit': 1, '^Digit': (2, False, True)}
        }

        id_dfa = {
            0: {'Alpha': 1},
            1: {'AlphaDigit': 1, '^AlphaDigit': (2, False, True)}
        }

        keyword_dfa = {
            0: {'Alpha': 1},
            1: {'alpha': 1, '^alpha': (2, False, True)}
        }

        symbol_dfa = {
            0: {'=': 1, 'SEE': (4, True, False), '/': 5},
            1: {'=': (2, True, False), '^=': (3, False, True)},
            5: {'^/*': (6, True, False)}
        }

        whitespace_dfa = {
            0: {'Whitespace': 1},
            1: {'Whitespace': 1, '^Whitespace': (2, False, True)}
        }

        comment_dfa = {
            0: {'/': 1},
            1: {'*': 2},
            2: {'*': 3, '^*': 2},
            3: {'^*/': 2, '*': 3, '/': (4, False, True) }

        }

        # Calculate the starting offset for each mini DFA
        offset = len(dfa.states)

        # Add mini DFAs to the global DFA
        dfa.add_mini_dfa(num_dfa, offset)
        offset += len(num_dfa)
        
        dfa.add_mini_dfa(id_dfa, offset)
        offset += len(id_dfa)

        dfa.add_mini_dfa(keyword_dfa, offset)
        offset += len(keyword_dfa)

        dfa.add_mini_dfa(symbol_dfa, offset)
        offset += len(symbol_dfa)

        dfa.add_mini_dfa(whitespace_dfa, offset)
        offset += len(whitespace_dfa)

        dfa.add_mini_dfa(comment_dfa, offset)
        offset += len(comment_dfa)


dfa = DFA()
add_token_states(dfa)