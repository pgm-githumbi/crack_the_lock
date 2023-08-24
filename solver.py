
import app
import random_prob
import ui.problem

#----------------------------------------------------------------
# Public API
#----------------------------------------------------------------
def get_solutions(problem:'ui.problem.Problem', alphabet:'list[str]'=None):
    """
    Yields tuples of solutions for the given ui.problem.Problem
    """
    if alphabet is None or len(alphabet) == 0:
        alphabet = random_prob.ALPHABET_DEFAULT

    problem_app_version_builder = _ProblemAppVersionBuilder()
    problem_app_version_builder.grid(_translate_grid(problem.grid, alphabet))
    problem_app_version_builder.alphabet(alphabet)
    rules:'list[ui.problem.Rule]' = []
    for row in problem.grid:
        rules.append(row[-1]) # The last item is a rule
    problem_app_version_builder.add_rules(_translate_rules(rules))
    problem_app_version = problem_app_version_builder.build()
    code = next(app.lock_cracker(grid=problem_app_version.grid,
                                 rules=problem_app_version.rules))
    yield _translate_code(code, alphabet)
    

#----------------------------------------------------------------
# Private API
#----------------------------------------------------------------

class _ProblemAppVersion:
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

class _ProblemAppVersionBuilder:
    def __init__(self):
        self.problem_app_version:'_ProblemAppVersion' = _ProblemAppVersion()

    def add_codes(self, codes:'list[list[int]]'):
        self.problem_app_version.codes.extend(codes)
        return self
    
    def add_rules(self, rules:'list[list[app.Rule]]'):
        self.problem_app_version.rules.extend(rules)
        return self
    
    def grid(self, grid:'list[list[int]]') -> '_ProblemAppVersionBuilder':
        self.problem_app_version.grid = grid
        return self
    
    def alphabet(self, alphabet):
        self.problem_app_version.alphabet = alphabet
        return self
    
    def build(self) -> '_ProblemAppVersion':
        return self.problem_app_version


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

def _translate_code(code:'list[int]', alphabet) -> 'list[int]':
    return [alphabet[i] for i in code]
    
