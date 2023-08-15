
import pytest

import random_prob

@pytest.fixture(params=[2, 4, 7, 100])
def lengths(request):
    return request.param

@pytest.fixture(params=[1, 3, 7 ])
def sums(request):
    return request.param

@pytest.fixture(params=[4, 7, 9, 36, 1, 3])
def max_value(request):
    return request.param


@pytest.fixture(params=[lengths, sums, max_value])
def combinations(lengths, sums, max_value):
    return random_prob._combinations_with_sum(lengths, sums, max_value)
        

def no_combination_possible(length, exp_sum, maximum_val):
    if maximum_val * length < exp_sum:
        return True
    if length > exp_sum:
        return True
    return False

def test_length_adhered(combinations, lengths, sums, max_value):
    for combination in combinations:
        if combination is None:
            assert False, 'combination is None'
        if no_combination_possible(lengths, sums, max_value):
            assert combination == []
            continue
        err_msg = (f'\tcombination length is incorrect; ', 
                    f'len is {len(combination)} ', 
                    f'expected {lengths} is {combination} ',
                    f'The comb is {combination}')
        assert len(combination) == lengths, err_msg
       

def test_max_value_adhered(combinations, lengths, sums, max_value):
    for combination in combinations:
        if no_combination_possible(lengths, sums, max_value):
            assert combination == []
            continue
        assert max(combination) <= max_value

def test_sum_adhered(combinations,lengths, sums, max_value):
    for combination in combinations:
        if no_combination_possible(lengths, sums, max_value):
            assert combination == []
            continue
        assert sum(combination) == sums


def test_actually_combinations(combinations):
    hashes = set()
    for combination in combinations:
        combination = tuple(sorted(combination))
        h = hash(combination)
        if h in hashes:
            assert False, "Repeated combination"
        hashes.add(h)


@pytest.mark.parametrize("length, sum, max_value", [(2, 6, 100)])
def test_combinations_count(length, sum, max_value):
    assert len(list(random_prob._combinations_with_sum(length, sum, max_value))) == 3