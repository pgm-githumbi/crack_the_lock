
import app
import pytest
import pytest_lazyfixture
import tests.unit_tests.config_problem_build
from tests.unit_tests.config_problem_build import *


@pytest.fixture
def hypothesis_set(problem_app_version:'tests.unit_tests.config_problem_build.ProblemAppVersion'):
    hypoths = []
    for code in problem_app_version.codes:
        hypoths.extend(app.HypothesisFactory().fromCode(problem_app_version.grid, code))
    return hypoths

def _stringify_hypoth_set(hypothesis_set):
    string = "["
    for hypothesis in hypothesis_set:
        string += f"\t{hypothesis}\n"
    string += "]"
    return string

def test_no_false_negatives(problem_app_version:'tests.unit_tests.config_problem_build.ProblemAppVersion',
                             hypothesis_set):

    conflicting_hypoths = []
    for i in range(len(hypothesis_set)):
        hypoth1 = hypothesis_set[i]
        for j in range(i + 1, len(hypothesis_set)):
            hypoth2 = hypothesis_set[j]
            if app.conflict(problem_app_version.grid,
                                                    hypoth1, hypoth2):
                conflicting_hypoths.append((hypoth1, hypoth2))
    error_msg = f"{problem_app_version}\n"
    error_msg += f"Conflicting Hypotheses: {_stringify_hypoth_set(conflicting_hypoths)}"
    assert app.anomaly(problem_app_version.grid, hypothesis_set) == False, error_msg


