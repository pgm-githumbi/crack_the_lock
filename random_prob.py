

from collections import Counter
from functools import lru_cache
import itertools
from typing import Any
import numpy as np
import statistics
import math
import random


from ui.problem import Problem, ProblemBuilder, RuleBuilder

#-------------------------------Public APIS-------------------------------------------------------------------------------------------------

ALPHABET_DEFAULT = list( 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' )

def generateRandomProblem(code_len:'int', alphabet:'list'=ALPHABET_DEFAULT, 
                          hint_count:'int'=None):
    """
    Generates a random problem of code_len length and hint_count hints.
    This game is about cracking a lock given hints; 
    """
    code = random.sample(sorted(set(alphabet)), k=code_len)
    if hint_count == None:
        hint_count = random.randint(getMinHintCount(len(code)),
                                     getMaxHintCount(len(code)))
    _vertical_corr_hint = _generate_vertical_corr_hint(code, hint_count)
    _vertical_corr_placed_hint = _generate_corr_placed_hints(code, _vertical_corr_hint)

    return _fill_up_problem(code, _vertical_corr_hint, _vertical_corr_placed_hint, alphabet)
    

DIFFICULTY_FACTOR_CORR: 'int' = 1.5 # The higher the easier, mininum is 1.0
DIFFICULTY_FACTOR_CORR_PLACED: 'int' = 0.5 # The higher the easier, mininum is 0.0, max is 1.0

def getMaxHintCount(code_len:'int'):
    """Returns the maximum number of hints that can be generated from the given code length."""
    return math.ceil(code_len * DIFFICULTY_FACTOR_CORR)

def getMinHintCount(code_length:'int'):
    return math.ceil(getMaxHintCount(code_length)/code_length)

def everyPossibleHintCount(code_length:'int'):
    """For testing purposes"""
    yield from range(getMinHintCount(code_length), getMaxHintCount(code_length)+1)
#--------------------------------------------------------------------------------------------------------------------------------

def _generate_vertical_corr_hint(code:'list', hint_count:'int',) -> 'list[list]':
    """Returns a list representing the grid but only containing values that are correct.
    i.e are contained in the `code`.
    """
    no_of_corr_hints = max(math.ceil(len(code) * DIFFICULTY_FACTOR_CORR), hint_count)
    
    hint_grid = [] # The grid but only containing values that are correct.
    
    # BUG FIX: No of correct hints should be able to fit in the grid
    grid_slot_count = len(code) * hint_count
    if no_of_corr_hints > grid_slot_count:
        no_of_corr_hints = grid_slot_count
        
    combinations = list(_combinations_with_sum(length=hint_count, sum_of_comb=no_of_corr_hints,
                                                max_value=len(code)))
    if hint_count > 1:
        chosen_indx = np.argmin([statistics.variance(c) for c in combinations]) 
    else:
        chosen_indx = 0
    chosen_comb = combinations[chosen_indx] # pick combination with least variance
    del combinations

    #randomly permute the chosen combination
    corr_values_count_per_row = random.choices(chosen_comb, k=len(chosen_comb))
    code_set, picked_sets = set(code), [set()]
    picked_set_pointer = 0
    # Generate a list `vertical_hint` representing the problem grid but containing only
    # the values that are correct(belong to the code).
    # The `permuted_chosen_comb` defines how many correct values we will assign 
    # to each row of the grid.
    for row, corr_count in enumerate(corr_values_count_per_row):
        pointer_in_corr_values_in_row = 0
        corr_values_in_row = [None] * corr_count
        while None in corr_values_in_row:
            if len(code_set) == len(picked_sets[picked_set_pointer]):
                # FIXED: initialize with values in row already
                picked_sets.append(set([v for v in corr_values_in_row if v is not None])) 
                picked_set_pointer += 1
            # Select and insert a random correct value that has not yet been picked
            values_not_yet_picked = list(code_set.difference(picked_sets[picked_set_pointer]))
            corr_value = random.choice(values_not_yet_picked) 
            corr_values_in_row[pointer_in_corr_values_in_row] = corr_value
            picked_sets[picked_set_pointer].add(corr_value)
            pointer_in_corr_values_in_row += 1
            
        # Add the correct values to the row of the grid.
        hint_grid.append(corr_values_in_row)
    return hint_grid

def print_2d_array(*args):
    """Prints a 2d array."""
    for arg in args:
        if type(arg) is not list:
            print(arg)
        print('[')
        for row in arg:
            print('\t',row)
        print(']')




















 

#------------------------------------------------------------------------------
# Utilities
#------------------------------------------------------------------------------

def _combinations_with_sum(length:'int', sum_of_comb:'int',
                            max_value:'int', start:'int'=1):
    """
    Returns a list of all possible combinations positive integers of length `length`
    that add up to `sum_of_comb`. The max integer allowable is `max_value`.
    """
    if length == 0:
        yield []
        return
    if length == 1:
        if sum_of_comb <= max_value:
            yield [sum_of_comb]
            return
        return # The current combination does not add up to sum_of_comb
    max_value = min(sum_of_comb, max_value)

    end = math.floor((1/length) * sum_of_comb)
    
    for i in range(start, end + 1):
        for comb in _combinations_with_sum(length - 1, sum_of_comb - i, max_value, i):
            yield [i, *comb]

def _combinations_of_sum_with_zeros(length, sum_of_combination, max_value):
    """
    Yields all possible combinations of integers greater than
     or equal to 0 and less than or equal to `max_value` of length `length`,
     that each add up to `sum_of_combination`;\n
     It yields lists `l` such that for all `value` in `l`, `0` >= `value` <= `max_value`
    
    """
    current_len = length
    while current_len > 0:    
        for combination in  _combinations_with_sum(current_len, sum_of_combination, max_value):
            zeros_count = length - len(combination)
            new_combination = [None] * (len(combination) + zeros_count)
            indices_for_zeros = itertools.combinations(range(0, len(new_combination)),
                                                        r=zeros_count)
            for indices in indices_for_zeros:
                for index in indices:
                    new_combination[index] = 0
                # Fill up the new combination with old combination's values
                # This turns new_combination = [0, None, None, 0, None] into [0, 1, 2, 0, 3] 
                # given combination was [1, 2, 3]
                old_combination_pos = 0
                for j in range(len(new_combination)):
                    if new_combination[j] == 0:
                        continue
                    new_combination[j] = combination[old_combination_pos]
                    old_combination_pos += 1
                yield new_combination
                new_combination = [None] * (len(combination) + zeros_count)
        current_len -= 1

def _combination_of_sum_with_zeros_of_least_variance(length, sum_of_combination, max_value):
    """
    Returns the combination of integers greater than
     or equal to 0 and less than or equal to `max_value` of length `length`,
     that adds up to `sum_of_combination`;\n
    """
    minvariance = math.inf
    minvariancecombination = []
    for combination in _combinations_of_sum_with_zeros(length, sum_of_combination, 
                                                                        max_value):
        if length != len(combination):
            return None
        if length == 1: # cannot calculate variance for a single value
            return combination
        if (var:=statistics.variance(combination)) < minvariance:
            minvariance = var
            minvariancecombination = combination

    return minvariancecombination

#------------------------------------------------------------------------------       
    
    




















def _generate_corr_placed_hints(code:'list', corr_hints:'list[list]',) -> 'list[list]':
    """ `vert_corr_hint` is the output of the function `_generate_vertical_corr_hint`.\n

    Returns a list of lists of 1s and 0s of length and shape of `vert_corr_hint` 
        (a mirror of `vert_corr_hint`), 
        where 1s mean the corresponding value in the `vert_corr_hint` list is correctly placed;
        while a 0 would mean the corresponding value in the `vert_corr_hint` list is not correctly placed."""
    no_of_corr_hints = math.ceil(len(code) * DIFFICULTY_FACTOR_CORR)
    no_of_corr_placed_hints = math.ceil(no_of_corr_hints * DIFFICULTY_FACTOR_CORR_PLACED)
    no_of_rows = len(corr_hints)

    combination = _combination_of_sum_with_zeros_of_least_variance(length=no_of_rows,
                                                        sum_of_combination=no_of_corr_placed_hints,
                                                        max_value=len(code))
    no_of_corr_placed_hints_per_row = combination
    print(f'\n{no_of_corr_placed_hints_per_row}')
    # Handle special case where there are just one incorrectly placed value
    # in a row where all values are correct. 
    # You can't have just one incorrectly
    # placed correct value in a row where all values are correct.
    array_incorr_placed_corr_counts = [None] * no_of_rows
    extra_incorr_placed_corr_counts, extra_corr_placed_counts = 0, 0
    for row_no in range(no_of_rows):
        corr_count = len(corr_hints[row_no]); 
        incorr_count = len(code) - corr_count
        corr_placed_count = no_of_corr_placed_hints_per_row[row_no]
        incorr_placed_corr_count = corr_count - corr_placed_count
        all_values_correct:'bool' = len(code) == corr_count
        #if all_values_correct and incorr_placed_corr_count == 1:
        if len(code) == 1:
            no_of_corr_placed_hints_per_row[row_no] = 1
            continue

        if incorr_count + incorr_placed_corr_count == 1:
            # Check if I can't add one more incorrectly placed correct value
            if len(code) == 1:
                no_of_corr_placed_hints_per_row[row_no] = 1
                extra_corr_placed_counts += 1
            # I can add one more incorrectly placed correct value
            no_of_corr_placed_hints_per_row[row_no] -= 1
            extra_incorr_placed_corr_counts += 1
            continue
        if corr_placed_count > corr_count:
            diff = corr_placed_count - corr_count
            no_of_corr_placed_hints_per_row[row_no] -= diff
            extra_incorr_placed_corr_counts += diff
            continue
        array_incorr_placed_corr_counts[row_no] = incorr_placed_corr_count
   
    # Redistribute the extra_incorr_placed_counts
    # TODO implement the redistribution

    # Select the values in each row to be correctly placed
    corr_placed_hints = [[None] * len(corr_hints[i]) for i in range(no_of_rows)]
    for row_no, corr_placed_count in enumerate(no_of_corr_placed_hints_per_row):
        corr_placed_positions = random.sample(range(len(corr_hints[row_no])), corr_placed_count)
        for corr_placed_position in corr_placed_positions:
            corr_placed_hints[row_no][corr_placed_position] = 1
        for position in range(len(corr_placed_hints[row_no])):
            if corr_placed_hints[row_no][position] == None:
                corr_placed_hints[row_no][position] = 0
    
    print(f'code: {code}')
    print_2d_array(corr_hints)
    print_2d_array(corr_placed_hints)
    print(no_of_corr_placed_hints_per_row)
    return corr_placed_hints

        

def _fill_up_problem(code:'str', corr_hints:'list[list]', 
                     corr_placed_hints:'list[list]', alphabet:'list'=ALPHABET_DEFAULT) -> 'Problem':
    """
    Fills up the problem with its values.
    """
    alphabet:'set' = set(alphabet)
    problem_buildr = ProblemBuilder().solution(code)
    get_correct_position:'dict[str,int]' = {}
    for i in range(len(code)):
        get_correct_position[code[i]] = i

    for r in range(len(corr_hints)):
        corr_count = len(corr_hints[r])
        corr_placed_count = len([k for k in corr_placed_hints[r] if k == 1])

        row = [None] * len(code)

        # Put every value in its correct place 
        for val in corr_hints[r]:
            corr_position = get_correct_position[val]
            row[corr_position] = val

        
        # Fill the remainder with unique random values
        remainder = Counter(row)[None]
        population = sorted(alphabet
                            .difference(code)
                            .difference((v for v in row if v is not None)))
        unique_random_values = random.sample(population, remainder)
        for j in range(len(row)):
            if row[j] is None:
                row[j] = unique_random_values.pop()

        corr_placed_values = set()
        for i in range(len(corr_placed_hints[r])):
            if corr_placed_hints[r][i] == 1:
                corr_placed_values.add(corr_hints[r][i])

        row = _u_scramble_except(row, do_not_scramble=corr_placed_values)

        rule = (RuleBuilder().are_correct_count(corr_count)
                            .are_correctly_placed(corr_placed_count)
                            .set_row(r)
                            .build())
        row.append(rule)
        problem_buildr.insert_new_row(row)
    return problem_buildr.build()


def _u_scramble_except(values:'list[Any]', do_not_scramble:'set[Any]'):
    """
    Scrambles the values in `values` except for those in `do_not_scramble`.
    Values in `values` but not in `do_not_scramble` end up in a different 
    position from where it is in `values` in the returned list.
    """
    if len(values) - len(do_not_scramble) == 1:
        raise ValueError('You cannot have just one displaced value in a list')
    scrambled = [None] * len(values)
    swapper:'int' = None # Position in scrambled that I can always swap with
    for i in range(len(values)):
        if values[i] in do_not_scramble:
            scrambled[i] = values[i]
            continue
        if swapper is None:
            scrambled[i] = values[i]
            swapper = i
            continue
        
        scrambled[i] = scrambled[swapper]
        scrambled[swapper] = values[i]
    return scrambled


def normalize_list(values:'list[int]', maximums:'list[int]'):
    """Alters the list of `values` in-place so that every `values[i]` <= `maximums[i]`
    and the sums of all values (`sum(values)`) remains the same after the
    alteration.
    It should be guaranteed that `sum(maximums)` >= `sum(values)` and that
    `len(values)` == `len(maximums)`\n
    In simple language, every value in the list `values` should be below or 
    same as the value in the same index in the list `maximums`; without 
    changing the sum of the list of `values`.\n
    Example:

    >>> normalize_list(values=[2, 5, 5], maximums=[3, 8, 2])
        [3, 7, 2]
    """
    running_diff = 0
    for i in range(len(values)):
        if values[i] > maximums[i]:
            diff = values[i] - maximums[i]
            running_diff += diff
            values[i] = maximums[i]
    for i in range(len(values)):
        if values[i] < maximums[i]:
            diff = maximums[i] - values[i] 
            values[i] += diff
            running_diff += diff
    return values


def _u_fairly_distribute_numbers(values:'list[int]', number:'int'):
    """Values is a list of integers. This function alters `values` so that
    the sum of all values (`sum(values)`) increases by `number` after the alteration.
    The distribution aims to keep the standard deviation of the `values` minimal.
    """
    values_sorted = sorted(values)
    curr_pos = 0
    values_sorted[curr_pos] += number
    next_larger = _u_find_pos_of_the_next_larger(values_sorted, curr_pos)
    while next_larger > curr_pos:
        total_distributed = 0
        for i in range(curr_pos + 1, next_larger):
            values_sorted[i] += 1
            total_distributed += 1
        values_sorted[curr_pos] -= total_distributed

        next_larger = _u_find_pos_of_the_next_larger(values_sorted, curr_pos)
    return values_sorted


def _u_find_pos_of_the_next_larger(values:'list[int]', start:'int'):
    """values is a sorted list of integers in ascending order; except one value `values[start]`
    is out of place. It has values smaller than itself to its right. 
    Returns the index of the value that is larger than or equal to `values[start]` in `values`"""
    result = start + 1
    while result < len(values) and values[result] < values[start]:
        result += 1

    if values[result] >= values[start]:
        return result
    return start