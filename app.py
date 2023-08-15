
from collections import Counter
from distutils.command import build
import itertools
import math
from typing import Any, Iterable






class Hypothesis:
    def __init__(self, row:int, indices:'list[int]', are_right:'bool',
                  are_rightly_placed:bool):
        self.row = row
        self.indices = indices
        self.are_right = are_right
        self.are_rightly_placed = are_rightly_placed
    
    def __str__(self):
        plural = len(self.indices) > 1
        values_as_str = "values" if plural else "value"
        are_as_str = "are" if plural else "is"

        string = f"In row {self.row}, {len(self.indices)} {values_as_str} "
        if self.are_right and self.are_rightly_placed:
            string += f"{are_as_str} correct and correctly placed "

        if self.are_right and not self.are_rightly_placed:
            string += f"{are_as_str} correct but wrongly placed "
        
        if not self.are_right:
            string += f"{are_as_str} wrong "
        
        string += f"in indices: {self.indices}."
        return string
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        this_obj = (self.row, self.are_right,
                    self.are_rightly_placed, self.indices)
        try:
            other_obj = (other.row, other.are_right, 
                        other.are_rightly_placed, other.indices)
        except AttributeError:
            return False
        return this_obj == other_obj
    
class HypothesisBuilder:
    def __init__(self) -> None:
        self.hypoth = Hypothesis(0, [], False, False)

    def row(self, row:'int') -> 'HypothesisBuilder':
        self.hypoth.row = row
        return self
    
    def indices(self, indices:'list[int]')  -> 'HypothesisBuilder':
        self.hypoth.indices = indices
        return self
    
    def indices_from_values(self, values:'list', grid:'list[list]', row:'int'):
        indexes = values_to_indices(grid, row, values)
        self.hypoth.indices = indexes
        return self
    
    def are_right(self, are_right:'bool')  -> 'HypothesisBuilder':
        self.hypoth.are_right = are_right
        return self
    
    def are_rightly_placed(self, are_rightly_placed:'bool') -> 'HypothesisBuilder':
        self.hypoth.are_rightly_placed = are_rightly_placed
        return self
    
    def build(self) -> 'Hypothesis':
        return self.hypoth
    

class Rule:
    def __init__(self, row:int, exclusively_correct:int,
                  correctly_placed:int):
        self.row = row
        
        self.correct = exclusively_correct
        self.correctly_placed = correctly_placed

    def __str__(self):
        def values_as_str(number):
            return "value" if number == 1 else "values"
        def are_as_str(number):
            return "is" if number == 1 else "are"
        
        string = f"In row {self.row}, {self.correct} {values_as_str(self.correct)} "
        string += f"{are_as_str(self.correct)} correct and {self.correctly_placed} "
        string += f" {values_as_str(self.correctly_placed)} {are_as_str(self.correctly_placed)} "
        string += f" correctly placed."
        return string

    def __repr__(self):
        return str(self)
    
class HypothesisFactory:
    def __init__(self):
        pass

    def fromCodeForRow(self, grid:'list[list[int]]', row:'int', code:'Iterable[int]'):
        """Generates the implied hypotheses by a solution of a grid(code) being
        correct; for a single row of the grid."""
        indices_of_vals = {v : i for i, v in enumerate(grid[row])}
        code_as_set:'set[int]' = set(code)
        
        corr_values = set(grid[row]).intersection(code_as_set)
        corr_values_indices = [indices_of_vals[val] for val in corr_values]

        corr_placed_pairs = set(enumerate(grid[row])).intersection(enumerate(code))
        corr_placed_indcs = [indx for indx, value in corr_placed_pairs]

        # CORRECT-BUT-WRONGLY-PLACED-based Hypotheses    
        corr_wrongly_placed_indices = set(corr_values_indices).difference(corr_placed_indcs)
        hypoth1 = (HypothesisBuilder()
                    .are_right(True)
                    .are_rightly_placed(False)
                    .row(row)
                    .indices(list(corr_wrongly_placed_indices))
                    .build()
                   )           
        # WRONG-based Hypotheses
        wrong_values = set(grid[row]).difference(corr_values)
        wrong_values_indices = [indices_of_vals[val] for val in wrong_values]
        hypoth2 = (HypothesisBuilder()
                    .are_right(False)
                    .are_rightly_placed(False)
                    .row(row)
                    .indices(wrong_values_indices)
                    .build())
        # CORRECTLY-PLACED-based Hypotheses
        hypoth3 = (HypothesisBuilder()
                    .are_right(True)
                    .are_rightly_placed(True)
                    .row(row)
                    .indices(corr_placed_indcs)
                    .build())

        return hypoth1, hypoth2, hypoth3

    def fromCode(self, grid:'list[list[int]]', code:'Iterable[int]'):
        """Generates all the hypotheses implied as correct by a solution(code)
        for the entire grid."""
        hypotheses = []
        for row_no in range(len(grid)):
            hypoth1, hypoth2, hypoth3 = self.fromCodeForRow(grid, row_no, code=code)
            hypotheses.append(hypoth1)
            hypotheses.append(hypoth2)
            hypotheses.append(hypoth3)
        return hypotheses


#----------------------------------------------------------------
# Public API
#----------------------------------------------------------------
        
def lock_cracker(grid:'list[list[int]]', rules:'list[Rule]'):
    # print_grid(grid)
    yield from _lock_cracker(grid, rules, hypotheses=[], row=0)

#----------------------------------------------------------------
# Private APIs
#----------------------------------------------------------------

def _lock_cracker(grid:'list[list[int]]', rules:'list[Rule]', 
                 hypotheses:'list[Hypothesis]', row:'int'):
    codes:'set[set[int, int]]' = set()
    if anomaly(grid, hypotheses):
        return None
    
    if row == len(grid):
        for soln in build_solutions(grid, hypotheses):
            if soln not in codes:
                codes.add(soln)
                yield soln
        return 
    
    for guessed_hypoths in guess_hypotheses(grid, row_no=row, rules=rules,):
        full_hypoth_set = hypotheses.copy()
        full_hypoth_set.extend(guessed_hypoths)
        
        for _code in _lock_cracker(grid, rules, full_hypoth_set, row + 1):
            if _code not in codes:
                yield _code
        del full_hypoth_set



def guess_hypotheses(grid:'list[list]', row_no:'int', rules:'list[Rule]'):
    # Attempt every possibility to fill the gap between known correct
    # values and how many rules say are correct.
    # Same applies for correctly placed
    for assumed_corr in itertools.combinations(grid[row_no], r=rules[row_no].correct):
        total_incorr_in_row = set(grid[row_no]).difference(assumed_corr)
        for assumed_corr_placed in itertools.combinations(assumed_corr, r=rules[row_no].correctly_placed):

            assum_corr_but_wrngly_placed = list(set(assumed_corr)
                                                .difference(assumed_corr_placed))
            
            h1 = (HypothesisBuilder()
                            .are_right(True)
                            .are_rightly_placed(True)
                            .row(row_no)
                            .indices_from_values(assumed_corr_placed, 
                                                 grid, row_no)
                            .build())
            h2 = (HypothesisBuilder()
                            .are_right(True)
                            .are_rightly_placed(False)
                            .row(row_no)
                            .indices_from_values(assum_corr_but_wrngly_placed,
                                                  grid, row_no)
                            .build())
            h3 = (HypothesisBuilder()
                            .are_right(False)
                            .are_rightly_placed(False)
                            .row(row_no)
                            .indices_from_values(total_incorr_in_row, grid, row_no)
                            .build())
             
            yield h1, h2, h3
            

            
    
def anomaly(grid:'list[list[int]]', hypothesis:'list[Hypothesis]'):
    """Returns whether any hypotheses in `hypotheses` make contradictory
    claims"""
    for i in range(len(hypothesis)):
        hypoth1 = hypothesis[i]
        for j in range(i + 1, len(hypothesis)):
            hypoth2 = hypothesis[j]
            if conflict(grid, hypoth1, hypoth2):
                return True
    if len(known_correct_values(grid, hypothesis)) > code_len(grid):
        return True
    if len(known_correctly_placed_values(grid, hypothesis)) > code_len(grid):
        return True
    if conflict_v1(grid, hypothesis):
        return True
    return False

def conflict_v1(grid:'list[list[int]]', hypotheses:'list[Hypothesis]'):
    """Returns whether any hypotheses in `hypotheses` make contradicting
    claims"""
    codely:'list[set]' = [set() for _ in range(code_len(grid))]
    # Codely represents a code.
    # For every position in `codely` insert all of the correct_values that
    # can not be inserted into the same position in the code
    relevant_hypotheses = (h for h in hypotheses if h.are_right and not h.are_rightly_placed)
    for hypoth in relevant_hypotheses:
        for indx in hypoth.indices:
            value = grid[hypoth.row][indx]
            # Value is wrongly placed so it can't be inserted
            # into its current position.
            codely[indx].add(value)
    # We have a problem if there's a position that can not accept
    # more values than the remaining number of positions; as this
    # would mean we have extra values with no position to be inserted
    # into.
    for i in range(len(codely)):
        remaining_positions = len(codely) - 1
        if len(codely[i]) > remaining_positions:
            return True
    return False


def conflict(grid:'list[list[int]]', hypoth1:'Hypothesis', hypoth2:'Hypothesis'):
    # BUG: When hypoth1 and hypoth2 are exactly the same, this function
    # claims there's a conflict. Am getting around it for now.
    hyp1_vals = {grid[hypoth1.row][index] for index in hypoth1.indices}
    hyp2_vals = {grid[hypoth2.row][index] for index in hypoth2.indices}
    if hypoth1.are_right != hypoth2.are_right:
        # Same values, one said to be right while the other wrong
        if hyp1_vals.intersection(hyp2_vals) != set():
            return True
        
    if hypoth1.are_right is True and hypoth2.are_right is True:
        # Values said to be right exceed length of the code
        if code_len(grid) < len(hyp1_vals.union(hyp2_vals)):
            return True
        
    h1map_indx2val:'set[tuple[int, int]]' = set()
    h2map_indx2val:'set[tuple[int, int]]' = set()
    for index in hypoth1.indices:
        h1map_indx2val.add((index, grid[hypoth1.row][index]))    
    for index in hypoth2.indices:
        h2map_indx2val.add((index, grid[hypoth2.row][index]))

    if hypoth1.are_rightly_placed != hypoth2.are_rightly_placed:
        # Same pos, same value one is rightly placed while the other not.
        if h1map_indx2val.intersection(h2map_indx2val) != set():
            return True
        
    if hypoth1.are_rightly_placed is True and hypoth2.are_rightly_placed is True:
        # Different values assigned the same position both said to be
        # correctly placed
        in_both = set(hypoth1.indices).intersection(hypoth2.indices)
        for index in in_both:
            if grid[hypoth1.row][index] != grid[hypoth2.row][index]:
                return True

    indices_of_hypoth1_vals:'dict[int,int]' = {grid[hypoth1.row][index] : index 
                                               for index in hypoth1.indices}
    indices_of_hypoth2_vals:'dict[int,int]' = {grid[hypoth2.row][index] : index
                                               for index in hypoth2.indices}
    
    if hypoth1.are_rightly_placed is True and hypoth2.are_rightly_placed is True:   
        # Same values different positions said to both be rightly placed
        for val_in_h1 in hyp1_vals:
            # Check if val_in_h1 is in hypoth2
            if val_in_h1 in hyp2_vals:
                # They have to be in the same position
                pos_in_h1:'int' = indices_of_hypoth1_vals[val_in_h1]
                pos_in_h2:'int' = indices_of_hypoth2_vals[val_in_h1]
                if pos_in_h1 != pos_in_h2:
                    return True
                
        for val_in_h2 in hyp2_vals:
            # Check if val_in_h2 is in hypoth1
            if val_in_h2 in hyp1_vals:
                # They have to be in the same position
                pos_in_h1:'int' = indices_of_hypoth1_vals[val_in_h2]
                pos_in_h2:'int' = indices_of_hypoth2_vals[val_in_h2]
                if pos_in_h1 != pos_in_h2:
                    return True
        
    return False

def build_solutions(grid:'list[list[int]]',  
                    hypotheses:'list[Hypothesis]'):
    """Returns a possible solution to the grid given a list of hypotheses"""
    solution = [None] * code_len(grid)
    for pos, value in known_correctly_placed_values(grid, hypotheses):
        solution[pos] = value
    remaining_empty_spaces = Counter(solution)[None]
    if remaining_empty_spaces == 0:
        yield tuple(solution)
        return
    corrects = known_correct_values(grid, hypotheses)
    _solns = set((s for s in solution if s is not None))
    corrects = (c for c in corrects if c not in _solns)
    for values in itertools.permutations(corrects, r=remaining_empty_spaces):
        pos_in_values = 0
        for i in range(len(solution)):
            if solution[i] is None:
                solution[i] = values[pos_in_values]
                pos_in_values += 1

        # Hypoths implied by solution being right
        implied_hypoths = (HypothesisFactory().fromCode(grid, code=solution))
        if not anomaly(grid, hypothesis=[*hypotheses, *implied_hypoths]):
            yield tuple(solution)

        values_set = set(values)
        for i in range(len(solution)):
            if solution[i] in values_set:
                solution[i] = None
    return

def values_to_indices(grid:'list[list[int]]', row:'int', 
                      values:'list[int]'):
    """Utility function to turn a row of values in `grid[row]`
    to a list of their indices withing the grid's row. The row is 
    not ordered in the order it appears in `grid` and may 
    not contain every value present in `grid[row]`"""           
    hshmap:'dict[int, int]' = dict()
    indices = []
    for i in range(len(grid[row])):
        hshmap[grid[row][i]] = i
    for val in values:    
        indices.append(hshmap[val])
    return indices

def code_len(grid:'list[list[int]]'):
    return len(grid[0])
    


def correctly_placed_vals_in_row(grid:'list[list[int]]', 
                                   hypotheses:'list[Hypothesis]', row:'int'
                                   ):
    """ Returns all values within `row` known to be correct from
    the list of `hypotheses`. The `hypotheses` should have no 
    contradictions; \n
    i.e `anomaly(grid, hypotheses)` returns `False`"""
    all_corr_placed = known_correctly_placed_values(grid, hypotheses)
    corr_placed = set()
    vals_in_row = set(grid[row])
    for index, value in all_corr_placed:
        if value in vals_in_row:
            if value == grid[row][index]:
                corr_placed.add(value)
    return corr_placed
    

    

def known_correct_values(grid:'list[list[int]]', 
                 hypotheses:'list[Hypothesis]') -> 'set[int]':
    """Returns a set of values the `hypotheses` say belong
    to the final code.\n 
    The list of hypotheses should have no contradictions. i.e
    `anomaly(grid, hypotheses)` should returns False."""
    def inner(position:'int'=0) -> 'tuple[set[Any], set[Any]]':
        if position == len(hypotheses):
            return set(), set()
        
        correct, incorrect = set(), set()
        cur_hypothesis = hypotheses[position]
        row_no = cur_hypothesis.row

        if cur_hypothesis.are_right:
            for index in cur_hypothesis.indices:
                correct.add(grid[row_no][index])
        if not cur_hypothesis.are_right:
            for index in cur_hypothesis.indices:
                incorrect.add(grid[row_no][index])
        
        inner_correct, inner_incorrect = inner(position + 1)
        return correct.union(inner_correct), incorrect.union(inner_incorrect)
    
    return inner()[0]



def known_correctly_placed_values(grid:'list[list[int]]',
                                  hypotheses:'list[Hypothesis]') :
    """Returns a set of tuples of (`index`, `value`) where the
    `index` is the position in the final code the value belongs."""
    def inner(position:'int'=0) -> 'set[tuple[int, int]]':
        if position == len(hypotheses):
            return set()
        
        correctly_placed = set()
        cur_hypothesis = hypotheses[position]
        row_no = cur_hypothesis.row

        if cur_hypothesis.are_rightly_placed:
            for index in cur_hypothesis.indices:
                correctly_placed.add((index, grid[row_no][index]))

        return correctly_placed.union(inner(position + 1))
    
    return inner(0)
