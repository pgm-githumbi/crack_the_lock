
import random
import pytest

import random_prob
import app
import ui.problem

class ProblemAppVersion:
    def __init__(self):
        self.codes:'list[list[int]]' = []
        self.alphabet = None
        self.rules:'list[app.Rule]' = []
        self.grid:'list[list[int]]' = []

    def __str__(self) -> str:
        string = "Problem:\n["
        for row_no in range(len(self.grid)):
            string += f"\t{self.grid[row_no]}\t{self.rules[row_no]}\n"
        string += f"]\n{self.codes}"
        return string
    
    def __repr__(self) -> str:
        return str(self)


class ProblemAppVersionBuilder:
    def __init__(self):
        self.problem_app_version:'ProblemAppVersion' = ProblemAppVersion()

    def add_codes(self, codes:'list[list[int]]'):
        self.problem_app_version.codes.extend(codes)
        return self
    
    def add_rules(self, rules:'list[list[app.Rule]]'):
        self.problem_app_version.rules.extend(rules)
        return self
    
    def grid(self, grid:'list[list[int]]') -> 'ProblemAppVersionBuilder':
        self.problem_app_version.grid = grid
        return self
    
    def alphabet(self, alphabet):
        self.problem_app_version.alphabet = alphabet
        return self
    
    def build(self) -> 'ProblemAppVersion':
        return self.problem_app_version

#-----------------------------------------------------------------------------
# Fixtures
#-----------------------------------------------------------------------------
CODE_LENGTHS = [2, 3, 4, 5]
MAX_CODE_LEN:'int' = max(CODE_LENGTHS)

@pytest.fixture(params=CODE_LENGTHS)
def code_length(request):
    return request.param

@pytest.fixture(params=[26])
def alphabet(request):
    alphabetsize = request.param
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return list(random.choices(alpha, k=alphabetsize))

@pytest.fixture(params=range(1, random_prob.getMaxHintCount(MAX_CODE_LEN)))
def hint_count(request):
    return request.param

@pytest.fixture
def problem(code_length, alphabet, hint_count):
    return random_prob.generateRandomProblem(code_length, alphabet, hint_count=hint_count)


@pytest.fixture
def problem_app_version(problem:'ui.problem.Problem', alphabet):
    prob_builder = ProblemAppVersionBuilder()
    codes = (_translate_code(soln, alphabet) for soln in  problem.solutions)
    (prob_builder.add_codes(codes)
                .alphabet(alphabet))

    rules_ui = [row[-1] for row in problem.grid]
    rules_app = _translate_rules(rules_ui)

    grid_app = _translate_grid(problem.grid, alphabet=alphabet)

    (prob_builder.add_rules(rules_app)
                .grid(grid_app))
    return prob_builder.build()


# -------------------------------------------------------------------------------
# Helpers
#-------------------------------------------------------------------------------

def _translate_rules(rules_ui:'list[ui.problem.Rule]') -> 'list[app.Rule]':
    for row, rule in enumerate(rules_ui):
        yield app.Rule(row=row, exclusively_correct=rule.are_correct,
                        correctly_placed=rule.are_correctly_placed)
        
def _translate_grid(grid:'list[list[str|ui.problem.Rule]]', alphabet) -> 'list[list[int]]':
    grid_new:'list[list[str|ui.problem.Rule]]' = []
    map_letter_to_int = dict(((v, k) for k, v in enumerate(alphabet)))
    for row in grid:
        new_row:'list[int]' = []
        for letter in row[:-1]:
            new_row.append(map_letter_to_int[letter])
        grid_new.append(new_row)
    return grid_new

def _translate_code(code:'list[str]', alphabet) -> 'list[int]':
    map_letter2int = {v: k for k, v in enumerate(alphabet)}
    return [map_letter2int[letter] for letter in code]

