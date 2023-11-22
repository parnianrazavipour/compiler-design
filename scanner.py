white_space = [' ' , '  ','\r','\n','\t','\f','\v']
#symobols execpt equals
keyword  = ['if', 'else', 'void', 'int', 'break', 'while', 'return']
see = ["(",")","{","}","[","]","+","-","*",",",":",";","<"]
digits = ["0","1","2","3","4","5","6","7","8","9"]
symbol  = ["(",")","{","}","[","]","+","-","*","=","/",",",":",";","<"]
lower_case_alphabet =  list("abcdefghijklmnopqrstuvwxyz")
upper_case_alphabet  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
all_alphabets = lower_case_alphabet + upper_case_alphabet
excluded_symbols = [char for char in symbol if char not in ['/', '*']]
excluded_symbols_1= [char for char in symbol if char not in ['=']]
excluded_symbols_2= [char for char in symbol if char not in ['*']]
excluded_symbols_3= [char for char in symbol if char not in ['/']]

type_dict = { 'Digit' : digits , '^Digit': excluded_symbols_3 + white_space + ['\x00'] ,  'SEE' :see , 'Alpha' : all_alphabets , 
         'alpha' : lower_case_alphabet , '^alpha' : upper_case_alphabet + digits + symbol + white_space + ['\x00'] ,
         'AlphaDigit' : all_alphabets + digits , '^AlphaDigit' : symbol + white_space + ['\x00'] , '^Alpha' :  digits + symbol + white_space + ['\x00'],
           '^/*':  all_alphabets + digits + excluded_symbols + white_space + ['\x00'] , 
           '^=' : all_alphabets + digits + excluded_symbols_1 + white_space + ['\x00'] ,
           'Whitespace' : white_space , '^Whitespace' :  all_alphabets + symbol + digits + ['\x00'] ,
            '^*' :  all_alphabets + digits + excluded_symbols_2 + white_space + ['\x00'] }


class DFA:
    def __init__(self):

        self.start_state = None
        self.accept_states = set()
        self.marked_accept_states = set()
        self.states_type = {}
        # accepts with star in dfa
        self.current_state = 0
        self.states = set()
        self.alphabet = set()
        self.transitions = {} 
        self.accept_states_dict = {}
        self.marked_accept_states_dict = {} 


    def add_state(self, state, is_start=False, is_accept=False , is_marked_accept = False):
        self.states.add(state)
        if is_start:
            self.start_state = state
            self.current_state = state
        if is_accept:
            self.accept_states.add(state)
        if is_marked_accept:
            self.marked_accept_states.add(state)


    def check_transition(self ,char) :
        types = []
        for type, val in type_dict.items() :
            if char in val :
                types.append(type)

        return types



    def process_input(self, char):
        possible_transitions = self.check_transition(char)
        current_transiton = None
                 
        for t in self.transitions[self.current_state] :
            if t in possible_transitions :
                current_transiton = t

        
        if char in self.transitions[self.current_state]:
            current_transiton  = char
        
        if not current_transiton :
           return False 
        
        print("char",char, "current_state ", self.current_state  ,"transition ", current_transiton  )
        print("next state", self.transitions[self.current_state][current_transiton])

        self.current_state = self.transitions[self.current_state][current_transiton]

        return True


    def make_transition(self, src_state, input_symbol, dest_state):
        if src_state not in self.transitions:
            self.transitions[src_state] = {}
        self.transitions[src_state][input_symbol] = dest_state
        self.alphabet.add(input_symbol)


    def is_accept_state(self):
        if ( self.current_state in self.marked_accept_states_dict.keys()) :
            return True, self.marked_accept_states_dict[self.current_state]
        elif ( self.current_state in self.accept_states_dict.keys()) :
            return False , self.accept_states_dict[self.current_state]
        else :
            return None, None






    def add_mini_dfa(self, token_type , mini_dfa_transitions, start_offset):
        """
        Adds a mini DFA to the current DFA.
        :param mini_dfa_transitions: A dictionary representing the transitions of the mini DFA.
        :param start_offset: The starting offset for the state IDs in the mini DFA.
        """
        for src, transitions in mini_dfa_transitions.items():
            last_offset = 0 
            if ( src == 0 ) :
                src_state = 0
            else :
                src_state = start_offset + src
                self.add_state(src_state)
                self.states_type[src_state] = token_type
            
            for input_symbol, dest in transitions.items():
                if isinstance(dest, tuple):
                    dest_state, is_accept, is_marked_accept = dest
                    self.add_state(start_offset + dest_state, is_accept=is_accept, is_marked_accept=is_marked_accept)
                    self.states_type[start_offset + dest_state] = token_type
                    if is_accept:
                     self.accept_states_dict[start_offset + dest_state]= token_type
                    elif is_marked_accept :
                        self.marked_accept_states_dict[start_offset + dest_state]= token_type

                else:
                    dest_state = dest

                self.make_transition(src_state, input_symbol, start_offset + dest_state)
                last_offset = start_offset + dest_state


                
        return last_offset




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
# 1 - ^Alpha -> 2*a

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
# 3 - / -> 4a


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
            3: {'^*/': 2, '*': 3, '/': (4, True, False) }

        }

        # Calculate the starting offset for each mini DFA
        offset = len(dfa.states)
        
        # Add mini DFAs to the global DFA
        dfa.add_state(0)
        offset = dfa.add_mini_dfa("NUM", num_dfa, 0)

        # offset += len(num_dfa)

        offset = dfa.add_mini_dfa("ID",id_dfa, offset)

        offset = dfa.add_mini_dfa("KEYWORD",keyword_dfa, offset)

        offset = dfa.add_mini_dfa("SYMBOL",symbol_dfa, offset)

        offset = dfa.add_mini_dfa("WHITSPACE",whitespace_dfa, offset)

        offset = dfa.add_mini_dfa("COMMENT",comment_dfa, offset)



def Scanner ( input_string , dfa ) :
    point1 = 0
    point2 = 0 
    input_string = input_string +'\x00'


    while point1 != len(input_string) -1 and point2 != len( input_string) -1:
        start_ch =input_string[point1]
        current_ch = input_string[point2]

        result = dfa.process_input(current_ch)
        if result :
            is_marked, token_type = dfa.is_accept_state()
            if( dfa.states_type[dfa.current_state] == 'COMMENT'):
                if(input_string[point2+1] == '\x00'):
                    print("Unclosed comment", input_string[point1:point2+1])
                    break

            if(dfa.current_state == 0 or dfa.states_type[dfa.current_state] in ['ID','KEYWORD']):
                if(current_ch == '*' and input_string[point2+1] == "/"):
                    print("Unmatched comment" , "*/")
                    dfa.current_state = 0
                    point2+=2
                    point1=point2
                    continue

            if (token_type in ['ID','KEYWORD']):
                if(input_string[point1:point2] in keyword) :
                    token_type = 'KEYWORD'
                else : token_type = 'ID'
            

            if not token_type  :
                point2+=1
            
            elif (is_marked) :
                print("type : ", token_type, " token : ", input_string[point1:point2])
                dfa.current_state = 0
                point1 = point2
            else :
                print("type : ", token_type, " token : ", input_string[point1:point2+1])
                dfa.current_state = 0
                point2+=1 
                point1=point2
        else :

            if(dfa.current_state == 0 or dfa.states_type[dfa.current_state] in ['ID','KEYWORD']):
                print("Invalid input",input_string[point1:point2+1])
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue

                                
            if(dfa.states_type[dfa.current_state] == 'NUM') :
                print("invalid number" , input_string[point1:point2+1])
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue
                   



    return









def display_dfa(dfa):
    print("DFA States and Transitions:")
    for state in dfa.states:
        print(f"State {state}:")
        if state in dfa.transitions:
            for input_symbol, dest_state in dfa.transitions[state].items():
                print(f"  On '{input_symbol}' -> State {dest_state}")
        if state in dfa.accept_states:
            print("  [Accept State]")
        if state in dfa.marked_accept_states:
            print("  [Marked Accept State]")

        # If you have specific tokens associated with accept states
        if state in dfa.accept_states_dict:
            print(f"  Token Type: {dfa.accept_states_dict[state]}")
        if state in dfa.marked_accept_states_dict:
            print(f"  Token Type (Marked): {dfa.marked_accept_states_dict[state]}")
    print("\n")


with open('input.txt', 'r') as file:
    content = file.read()


dfa = DFA()
add_token_states(dfa)

display_dfa(dfa)

Scanner(content, dfa)



