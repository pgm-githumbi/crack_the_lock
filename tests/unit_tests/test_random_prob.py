
import pytest

import random_prob
import ui.problem 

CODE_LENGTHS:'list[int]' = [1, 2, 3, 4, 5, 7, 9, 10]
MAX_CODE_LEN:'int' = max(CODE_LENGTHS)

@pytest.fixture(params=CODE_LENGTHS)
def code_length(request):
    return request.param


@pytest.fixture(params=range(1, random_prob.getMaxHintCount(MAX_CODE_LEN)))
def hint_counts(request):
    return request.param

@pytest.fixture
def problem(code_length, hint_counts) -> 'ui.problem.Problem':
    return random_prob.generateRandomProblem(code_length, hint_count=hint_counts)
    

#---------------------------------------------------------------------------------------------------------
# Utilities
#---------------------------------------------------------------------------------------------------------
def get_row(prob:'ui.problem.Problem', value:'str'):
    for i in range(len(prob.grid)):
        if value in set(prob.grid[i]):
            yield i

def get_rows_rule(prob:'ui.problem.Problem', row:'int'):
    return prob.grid[row][len(prob.grid[row]) - 1]

def get_correct_vals_in_row(prob:'ui.problem.Problem',solution:'str',  row:'int'):
    """Returns all values in `row` that are in `solution"""
    return set(solution).intersection(prob.grid[row])

def get_correctly_placed(prob:'ui.problem.Problem', solution:'str', row:'int'=None):
    """Returns all values in `row` that are in the same pos they are in `solution`"""
    solution_map = set(enumerate(solution))
    row_map = set(enumerate(prob.grid[row]))
    return solution_map.intersection(row_map)

#---------------------------------------------------------------------------------------------------------
# Tests
#---------------------------------------------------------------------------------------------------------


def test_every_soln_valid(problem):
    prob:'ui.problem.Problem' = problem
    for sol in prob.solutions:
        for i in range(len(prob.grid)):
            rule:'ui.problem.Rule' = get_rows_rule(prob, row=i)
            
            actual_correct = get_correct_vals_in_row(prob, solution=sol, row=i)
            assert len(actual_correct) == rule.are_correct

            correctly_placed = get_correctly_placed(prob, sol, row=i)
            assert len(correctly_placed) == rule.are_correctly_placed


def test_every_soln_char_is_in_problem(problem:'ui.problem.Problem'):
    
    _problem:'ui.problem.Problem' = problem
    chars_in_soln = set((char for sol in _problem.solutions for char in sol))
    chars_in_problm = set()
    for row in _problem.grid:
        for char in row:
            chars_in_problm.add(char)
    error_msg = (f"These characters are in solution but not in problem: " + 
                f"{chars_in_soln.difference(chars_in_problm)}")
    assert chars_in_soln.issubset(chars_in_problm), error_msg


def test_no_repetition_in_problm_rows(problem:'ui.problem.Problem'):
    
    _problem:'ui.problem.Problem' = problem
    for i in range(len(_problem.grid)):
        row = _problem.grid[i]
        value_counts_map:'dict[str,int]' = dict()
        for val in row:
            if val in value_counts_map:
                value_counts_map[val] += 1
            else:
                value_counts_map[val] = 1
        repeated_values = set()
        for key, value in value_counts_map.items():
            if value > 1:
                repeated_values.add(key)
        err_msg = f"These values are duplicated in problem row {i}: {str(repeated_values)}"
        assert len(repeated_values) == 0, err_msg
        

