const firstFollow = require('first-follow');
const fs = require('fs');

const rules = [
  { left: 'Program', right: ['DeclarationList'] },
  { left: 'DeclarationList', right: ['Declaration', 'DeclarationList'] },
  { left: 'DeclarationList', right: ['epsilon'] },
  { left: 'Declaration', right: ['DeclarationInitial', 'DeclarationPrime'] },
  { left: 'DeclarationInitial', right: ['TypeSpecifier', 'ID'] },
  { left: 'DeclarationPrime', right: ['FunDeclarationPrime'] },
  { left: 'DeclarationPrime', right: ['VarDeclarationPrime'] },
  { left: 'VarDeclarationPrime', right: [';'] },
  { left: 'VarDeclarationPrime', right: ['[', 'NUM', ']', ';'] },
  { left: 'FunDeclarationPrime', right: ['(', 'Params', ')', 'CompoundStmt'] },
  { left: 'TypeSpecifier', right: ['int'] },
  { left: 'TypeSpecifier', right: ['void'] },
  { left: 'Params', right: ['int', 'ID', 'ParamPrime', 'ParamList'] },
  { left: 'Params', right: ['void'] },
  { left: 'ParamList', right: [',', 'Param', 'ParamList'] },
  { left: 'ParamList', right: ['epsilon'] },
  { left: 'Param', right: ['DeclarationInitial', 'ParamPrime'] },
  { left: 'ParamPrime', right: ['[', ']'] },
  { left: 'ParamPrime', right: ['epsilon'] },
  { left: 'CompoundStmt', right: ['{', 'DeclarationList', 'StatementList', '}'] },
  { left: 'StatementList', right: ['Statement', 'StatementList'] },
  { left: 'StatementList', right: ['epsilon'] },
  { left: 'Statement', right: ['ExpressionStmt'] },
  { left: 'Statement', right: ['CompoundStmt'] },
  { left: 'Statement', right: ['SelectionStmt'] },
  { left: 'Statement', right: ['IterationStmt'] },
  { left: 'Statement', right: ['ReturnStmt'] },
  { left: 'ExpressionStmt', right: ['Expression', ';'] },
  { left: 'ExpressionStmt', right: ['break', ';'] },
  { left: 'ExpressionStmt', right: [';'] },
  { left: 'SelectionStmt', right: ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement'] },
  { left: 'IterationStmt', right: ['while', '(', 'Expression', ')', 'Statement'] },
  { left: 'ReturnStmt', right: ['return', 'ReturnStmtPrime'] },
  { left: 'ReturnStmtPrime', right: [';'] },
  { left: 'ReturnStmtPrime', right: ['Expression', ';'] },
  { left: 'Expression', right: ['SimpleExpressionZegond'] },
  { left: 'Expression', right: ['ID', 'B'] },
  { left: 'B', right: ['=', 'Expression'] },
  { left: 'B', right: ['[', 'Expression', ']', 'H'] },
  { left: 'B', right: ['SimpleExpressionPrime'] },
  { left: 'H', right: ['=', 'Expression'] },
  { left: 'H', right: ['G', 'D', 'C'] },
  { left: 'SimpleExpressionZegond', right: ['AdditiveExpressionZegond', 'C'] },
  { left: 'SimpleExpressionPrime', right: ['AdditiveExpressionPrime', 'C'] },
  { left: 'C', right: ['Relop', 'AdditiveExpression'] },
  { left: 'C', right: ['epsilon'] },
  { left: 'Relop', right: ['<'] },
  { left: 'Relop', right: ['=='] },
  { left: 'AdditiveExpression', right: ['Term', 'D'] },
  { left: 'AdditiveExpressionPrime', right: ['TermPrime', 'D'] },
  { left: 'AdditiveExpressionZegond', right: ['TermZegond', 'D'] },
  { left: 'D', right: ['Addop', 'Term', 'D'] },
  { left: 'D', right: ['epsilon'] },
  { left: 'Addop', right: ['+'] },
  { left: 'Addop', right: ['-'] },
  { left: 'Term', right: ['SignedFactor', 'G'] },
  { left: 'TermPrime', right: ['SignedFactorPrime', 'G'] },
  { left: 'TermZegond', right: ['SignedFactorZegond', 'G'] },
  { left: 'G', right: ['*', 'SignedFactor', 'G'] },
  { left: 'G', right: ['epsilon'] },
  { left: 'Factor', right: ['(', 'Expression', ')'] },
  { left: 'Factor', right: ['ID', 'VarCallPrime'] },
  { left: 'Factor', right: ['NUM'] },
  { left: 'VarCallPrime', right: ['(', 'Args', ')'] },
  { left: 'VarCallPrime', right: ['VarPrime'] },
  { left: 'VarPrime', right: ['[', 'Expression', ']'] },
  { left: 'VarPrime', right: ['epsilon'] },

  { left: 'FactorZegond', right: ['(', 'Expression', ')'] },
  { left: 'FactorZegond', right: ['NUM'] },
  { left: 'Args', right: ['ArgList'] },
  { left: 'Args', right: ['epsilon'] },
  { left: 'ArgList', right: ['Expression', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: [',', 'Expression', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: ['epsilon'] },
  { left: 'SignedFactor', right: ['+', 'Factor'] },
  { left: 'SignedFactor', right: ['-', 'Factor'] },
  { left: 'SignedFactor', right: ['Factor'] },
  { left: 'SignedFactorPrime', right: ['FactorPrime'] },
  { left: 'FactorPrime', right: ['(', 'Args', ')'] },
  { left: 'FactorPrime', right: ['epsilon'] },
  { left: 'SignedFactorZegond', right: ['+', 'Factor'] },
  { left: 'SignedFactorZegond', right: ['-', 'Factor'] },
  { left: 'SignedFactorZegond', right: ['FactorZegond'] }
];


const { firstSets, followSets, predictSets } = firstFollow(rules);

const output = {
  firstSets,
  followSets,
  predictSets
};

fs.writeFile('../first-follow.json', JSON.stringify(output, null, 2), (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
});