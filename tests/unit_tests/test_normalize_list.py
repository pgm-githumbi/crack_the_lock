import pytest
import random

@pytest.fixture
def maximums():
    return [3, 8, 2, 4, 5, 0]

@pytest.fixture(params=[(1, 1), (1, 2), (1, 3), (2, 3), 
                        (3, 4), (5, 6), (7, 8), (3, 8)])
def values(maximums, ratio:'tuple[int, int]'):
    # Number of values to exceed their maximum counterparts
    to_exceed = int(len(maximums) * (ratio[0]/(ratio[0] + ratio[1])))
    to_be_less = len(maximums) - to_exceed
    [random.randint(0, maximums[i]) for i in range(to_be_less)]
    [random.randint(maximums[i],) for i in range(to_exceed)]
