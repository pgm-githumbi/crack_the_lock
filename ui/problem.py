

from typing import Any


class Rule:
    def __init__(self, row:'int', are_corr:'int', corr_placed:'int') -> None:
        self.row:'int' = row
        self.are_correct:'int' = are_corr
        self.are_correctly_placed:'int' = corr_placed

    def __str__(self):
        preposition_0 = 'are' if self.are_correct > 1 else 'is'
        preposition_1 = 'are' if self.are_correctly_placed > 1 else 'is'
        correctly_placed = self.are_correctly_placed if self.are_correctly_placed > 0 else 'None'

        if self.are_correct > 0:
            first_part = f'Only {self.are_correct} {preposition_0} correct and '
        else:
            first_part = 'None is correct and'

        second_part = f'{correctly_placed} of them {preposition_1} correctly placed'
        return (first_part + second_part)
    
    def __repr__(self) -> str:
        return self.__str__()

class RuleBuilder:
    def __init__(self, rule:'Rule'=None):
        self.rule = Rule(row=-1, are_corr=0, corr_placed=0) if rule is None else rule
    def set_row(self, row:'int'):
        self.rule.row = row
        return self
    def are_correct_count(self, are_corr_count:'int'):
        self.rule.are_correct = are_corr_count
        return self
    def are_correctly_placed(self, corr_placed:'int'=0):
        self.rule.are_correctly_placed = corr_placed
        return self
    def build(self):
        return self.rule
    
class Problem:
    def __init__(self):
        
        self.code_alphabet:'set[str]' = set()
        self.solution:'str' = None
        self.grid:'list[list[str|Rule]]' = []
        self.solutions:'list[str]' = []

    def __repr__(self) -> str:
        string = '-----------------------------------\n'
        string += super(Problem, self).__repr__()
        string += '\n[\n'
        for row in self.grid:
            string += '\t%s\n'%str(row)
        string += ']\n'
        string += f'['
        for solution in self.solutions:
            string += '\t%s\n'%str(solution)
        string += f']\n'
        string += '-----------------------------------\n'
        return string
        



class ProblemBuilder:
    def __init__(self):
        self.problem = Problem()
    
    def insert_new_row(self, row:'list[str|Rule]'):
        self.problem.grid.append(row)
        return self
    
    def insert_value(self, value:'str|Rule', row:'int', column:'int'):
        self.problem.grid[row][column] = value
        return self
    
    def rule_for_row(self, row:'int', rule:'Rule'):
        self.problem.grid[row][-1] = rule
        return self
    
    def solution(self, solution:'str'):
        self.problem.solution = solution
        self.problem.solutions.append(solution)
        return self

    def build(self):
        return self.problem







