ss = []
data_block_base = 100
data_block_memory = []
symbol_table = []
Program_block = []
ENTRY_LEN = 4
scope_stack = [ ]

class Data :
    def __init__(self, lexeme, type , memory_address , size=4 , array_size = 1 ) -> None:
        self.lexem = lexeme
        self.type = type
        self.memory_address = memory_address
        self.size = size
        if(type == 'arr_int' ) :
            self.array_size = array_size
        self.value = 0
    


def error_handle(action, datas) :
    if action == 'DEC_VARIABLE' :
        name,type = datas[0], datas[1]
        if (type == 'void') :
            print("error !")
        else : return True



def SAVE(token):
    ss.push(token)

def DEC_VARIABLE() :
    name = ss.pop()
    type = ss.pop()
    if error_handle('DEC_VARIABLE' ,[name, type]) :
        data_memory_index = len(data_block_memory) + data_block_base + ENTRY_LEN 
        data = Data(lexeme = name ,type = type , memory_address = data_memory_index)
        # added to memory
        data_block_memory.append(data)
        # added to symbol table 
        symbol_table.append(data)
        
            
def DEC_ARRAY( ) :
    size = ss.pop()
    array_name = ss.pop()
    data_memory_index = len(data_block_memory) + data_block_base  + ENTRY_LEN
    array_start_index = data_memory_index
    for i in range(size) :
        data_memory_index +=4
        data = Data(lexeme=array_name, type='arr_int_val',memory_address=data_memory_index,  array_size = size )
        data_block_memory.append( data)

    data = Data(lexeme=array_name , type='arr_int', memory_address=array_start_index , array_size=size)
    symbol_table.append(data)

  

def DEC_FUNCTION( ) :
    func_name = ss.pop()
    return_type = ss.pop()
    scope_stack.append(func_name)
    if (func_name == 'main') :
        current_pb_index = len(Program_block)
        Program_block.append('(JP,'+str(current_pb_index)+',,)')
    data = Data(lexeme=func_name ,)
      


    



left = 'left'
right = 'right'
null = None

grammar_rules =  [
  { left: 'Program', right: ['DeclarationList'] },
  { left: 'DeclarationList', right: ['Declaration', 'DeclarationList'] },
  { left: 'DeclarationList', right: ['epsilon'] },
  { left: 'Declaration', right: ['DeclarationInitial', 'DeclarationPrime'] },
  { left: 'DeclarationInitial', right: ['@SAVE','TypeSpecifier', '@SAVE', 'ID',''] },
  { left: 'DeclarationPrime', right: ['FunDeclarationPrime'] },
  { left: 'DeclarationPrime', right: ['VarDeclarationPrime'] },
  { left: 'VarDeclarationPrime', right: [';' , '@DEC_VARIABLE'] },
  { left: 'VarDeclarationPrime', right: ['[', '@SAVE','NUM', ']',';' ,'@DEC_ARRAY'] },
  { left: 'FunDeclarationPrime', right: ['@DEC_FUNCTION','(', 'Params', ')','@SAVE_ARGS', 'CompoundStmt' , '@END_FUNCTION'] },
  { left: 'TypeSpecifier', right: ['int'] },
  { left: 'TypeSpecifier', right: ['void'] },
  { left: 'Params', right: ['@SAVE','int','@PID', 'ID', 'ParamPrime', 'ParamList'] },
  { left: 'Params', right: ['void'] },
  { left: 'ParamList', right: [',', 'Param', 'ParamList'] },
  { left: 'ParamList', right: ['epsilon'] },
  { left: 'Param', right: ['DeclarationInitial', 'ParamPrime'] },
  { left: 'ParamPrime', right: ['[', ']', '@DEC_ARRAY_POINTER'] },
  { left: 'ParamPrime', right: ['epsilon' , '@DEC_VARIABLE'] },
  { left: 'CompoundStmt', right: ['{', 'DeclarationList', 'StatementList', '}'] },
  { left: 'StatementList', right: ['Statement', 'StatementList'] },
  { left: 'StatementList', right: ['epsilon'] },
  { left: 'Statement', right: ['ExpressionStmt'] },
  { left: 'Statement', right: ['CompoundStmt'] },
  { left: 'Statement', right: ['SelectionStmt'] },
  { left: 'Statement', right: ['IterationStmt'] },
  { left: 'Statement', right: ['ReturnStmt'] },
  { left: 'ExpressionStmt', right: ['Expression', ';'] },
  { left: 'ExpressionStmt', right: ['break' , '@BREAK', ';'] },
  { left: 'ExpressionStmt', right: [';'] },
  { left: 'SelectionStmt', right: ['if', '(', 'Expression', ')' , '@SAVE_IF' , 'Statement', 'else','@JPF_SAVE_IF', 'Statement' ,'@JP_IF'] },
  { left: 'IterationStmt', right: ['while','@LABEL', '(', 'Expression', ')','@SAVE_WHILE', 'Statement', '@WHILE'] },
  { left: 'ReturnStmt', right: ['return', 'ReturnStmtPrime'] },
  { left: 'ReturnStmtPrime', right: [ '@RETURN_VOID', ';'] },
  { left: 'ReturnStmtPrime', right: ['Expression', '@RETURN_VALUE', ';'] },
  { left: 'Expression', right: ['SimpleExpressionZegond'] },
  { left: 'Expression', right: ['@PID' ,'ID', 'B'] },
  { left: 'B', right: ['=', 'Expression' , '@ASSIGN'] },
  { left: 'B', right: ['[', 'Expression', ']', '@ARR_ADDR' ,'H'] },
  { left: 'B', right: ['SimpleExpressionPrime'] },
  { left: 'H', right: ['=', 'Expression', '@ASSIGN'] },
  { left: 'H', right: ['G', 'D', 'C'] },
  { left: 'SimpleExpressionZegond', right: ['AdditiveExpressionZegond', 'C'] },
  { left: 'SimpleExpressionPrime', right: ['AdditiveExpressionPrime', 'C'] },
  { left: 'C', right: ['Relop', 'AdditiveExpression', '@SAVE_RELOP_RESULT'] },
  { left: 'C', right: ['epsilon'] },
  { left: 'Relop', right: [ '@SAVE', '<'] },
  { left: 'Relop', right: ['@SAVE' , '=='] },
  { left: 'AdditiveExpression', right: ['Term', 'D'] },
  { left: 'AdditiveExpressionPrime', right: ['TermPrime', 'D'] },
  { left: 'AdditiveExpressionZegond', right: ['TermZegond', 'D'] },
  { left: 'D', right: ['Addop', 'Term','@ADD_SUB' 'D'] },
  { left: 'D', right: ['epsilon'] },
  { left: 'Addop', right: ['@SAVE','+'] },
  { left: 'Addop', right: ['@SAVE','-'] },
  { left: 'Term', right: ['SignedFactor', 'G'] },
  { left: 'TermPrime', right: ['SignedFactorPrime', 'G'] },
  { left: 'TermZegond', right: ['SignedFactorZegond', 'G'] },
  { left: 'G', right: ['*', 'SignedFactor','@MULT', 'G'] },
  { left: 'G', right: ['epsilon'] },
  { left: 'Factor', right: ['(', 'Expression', ')'] },
  { left: 'Factor', right: ['@PID','ID', 'VarCallPrime'] },
  { left: 'Factor', right: ['@SAVE_CONST','NUM'] },
  { left: 'VarCallPrime', right: ['(', 'Args', ')','@CHECK_ARGS'] },
  { left: 'VarCallPrime', right: ['VarPrime'] },
  { left: 'VarPrime', right: ['[', 'Expression', ']'] },
  { left: 'VarPrime', right: ['epsilon'] },
  { left: 'FactorZegond', right: ['(', 'Expression', ')'] },
  { left: 'FactorZegond', right: ['@SAVE_CONST','NUM'] },
  { left: 'Args', right: ['ArgList'] },
  { left: 'Args', right: ['epsilon'] },
  { left: 'ArgList', right: ['Expression', '@ASSIGN_ARG', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: [',', 'Expression', '@ASSIGN_ARG', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: ['epsilon'] },
  { left: 'SignedFactor', right: ['+', 'Factor'] },
  { left: 'SignedFactor', right: ['-', 'Factor','@NEG'] },
  { left: 'SignedFactor', right: ['Factor'] },
  { left: 'SignedFactorPrime', right: ['FactorPrime'] },
  { left: 'FactorPrime', right: ['(', 'Args', ')', '@CHECK_ARGS'] },
  { left: 'FactorPrime', right: ['epsilon'] },
  { left: 'SignedFactorZegond', right: ['+', 'Factor'] },
  { left: 'SignedFactorZegond', right: ['-', 'Factor', '@NEG'] },
  { left: 'SignedFactorZegond', right: ['FactorZegond'] }
]
