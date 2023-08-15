
import enum
from typing import NewType
import pytest
import app
import random_prob
import tests.unit_tests.config_problem_build 
from tests.unit_tests.config_problem_build import *
import ui.problem

ProblemVersionApp = NewType('ProblemVersionApp', tests.unit_tests.config_problem_build.ProblemAppVersion)

def test_solve(problem_app_version:'ProblemVersionApp'):
    
    alleged_solns = app.lock_cracker(grid=problem_app_version.grid,
                                      rules=problem_app_version.rules,)
    alleged_solns = set(alleged_solns)
    expected_soln = problem_app_version.codes[0]
    err_msg = f"Expected soln: {expected_soln} \t"
    err_msg += f"Provided soln: {alleged_solns}"
    assert tuple(expected_soln) in alleged_solns, err_msg
    


def test_every_soln_makes_sense(problem_app_version:'ProblemVersionApp'):
    solns = app.lock_cracker(grid=problem_app_version.grid,
                            rules=problem_app_version.rules)
    for soln in solns:
        for row_no in range(len(problem_app_version.grid)):
            row = problem_app_version.grid[row_no]
            rule = problem_app_version.rules[row_no]
            expected_corr, expected_corr_placed = rule.correct, rule.correctly_placed
            actual_corr = set(soln).intersection(row)
            assert len(actual_corr) == expected_corr

            soln_indices:'set[tuple[int, int]]' = set(enumerate(soln))
            row_indices:'set[tuple[int, int]]' = set(enumerate(row))
            actual_corr_placed = soln_indices.intersection(row_indices)
            err_msg = f"soln: {soln}||row: {row} || rule: {rule}"
            assert len(actual_corr_placed) == expected_corr_placed, err_msg