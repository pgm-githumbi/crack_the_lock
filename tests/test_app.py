from typing import Iterable

import init
import unittest
from app import *




class TestHypothesis(unittest.TestCase):
    def setUp(self):
        self.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.grid1 = [[6, 7, 5], [4, 2, 8], [3, 5, 4], [2, 6, 8], [4, 5, 2]]
        self.hypoth1 = Hypothesis(0, [0, 1], True, False)
        self.hypoth2 = Hypothesis(1, [0, 1], False, False)
        self.hypoth3 = Hypothesis(2, [0, 1], False, False)
        self.hypoth4 = Hypothesis(0, [0], True, True)
        self.hypoth5 = Hypothesis(1, [1], True, True)
        self.hypoth6 = Hypothesis(2, [2], True, True)

        self.hyp1 = Hypothesis(0, [1, 2], True, True)
        self.hyp2 = Hypothesis(2, [0, 1], True, True)
        self.hyp3 = Hypothesis(1, [1], True, True)
        self.hyp4 = Hypothesis(3, [0], True, True)
        self.hyp5 = Hypothesis(3, [1], True, False)
        self.hyp6 = Hypothesis(1, [0, 1, 2], True, True)
        self.hyp7 = Hypothesis(2, [1, 2], True, True)
        self.hyp8 = Hypothesis(3, [2, 0], True, True)
        self.hyp9 = Hypothesis(1, [2, 1], True, False)
        self.hyp10 = Hypothesis(1, [2, 1], False, False)
        

    def test_conflict(self):
        self.assertFalse(conflict(self.grid,self.hypoth1,self.hypoth2))
        self.assertFalse(conflict(self.grid,self.hypoth1,self.hypoth3))
        self.assertFalse(conflict(self.grid,self.hypoth2,self.hypoth3))
        self.assertFalse(conflict(self.grid,self.hypoth4,self.hypoth5))
        self.assertFalse(conflict(self.grid,self.hypoth5,self.hypoth6))
        self.assertFalse(conflict(self.grid,self.hypoth4,self.hypoth6))

        self.assertTrue(conflict(self.grid1, self.hyp1, self.hyp2))
        self.assertTrue(conflict(self.grid1, self.hyp3, self.hyp4))
        self.assertFalse(conflict(self.grid1, self.hyp1, self.hyp5))
        self.assertTrue(conflict(self.grid1, self.hyp1, self.hyp6))
        self.assertTrue(conflict(self.grid1, self.hyp1, self.hyp7))
        # Same position, same values, different `are_rightly_placed` state
        self.assertTrue(conflict(self.grid1, self.hyp8, self.hyp9))
        self.assertTrue(conflict(self.grid1, self.hyp8, self.hyp10))
        # Same row, same values, different `are_right` state
        self.assertTrue(conflict(self.grid1, self.hyp9, self.hyp10))
    





class TestPermutations(unittest.TestCase):
    def setUp(self):
        self.items = [1, 2, 3]

    def test_permutations(self):
        expected_output = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
        out = permutations(self.items, 2)
        self.assertTrue(self._arePermutations(out, expected_output),
                        msg=f'out: {out}\nexpected_out:{expected_output}\n')
        
        
        expected_out = [[1, 2, 3], [1, 3, 2], [2, 1, 3], 
                        [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        out = permutations(self.items, 3)
        self.assertTrue(self._arePermutations(out, expected_out),
                        msg=f'out: {out}\nexpected_out:{expected_output}\n')

    def _arePermutations(self, items1, items2):
        hshdct:'dict[frozenset,set]' = {}
        for item in items1:
            item = tuple(item)
            key = frozenset(item)
            if group_set := hshdct.get(key, False):
                group_set.add(item)
            else:
                hshdct[key] = set()
                hshdct[key].add(item)

        for item in items2:
            item = tuple(item)
            key = frozenset(item)
            if (group_set := hshdct.get(key, None)) is None:
                return False
            if item in group_set:
                group_set.remove(item)
            else:
                return False
            
        return len(items1) == len(items2)


class TestCombinations(unittest.TestCase):
    def setUp(self) -> None:
        self.items = [1, 2, 3]
        return super().setUp()
    
    def test_combinations(self) -> None:
        
        exp_out = [[1, 2], [1, 3], [2, 3]]
        out = combinations(self.items, 2)
        self.assertTrue(self._areCombinations(out, exp_out))
        
        exp_out = [[1, 2, 3]]
        out = combinations(self.items, 3)
        self.assertTrue(self._areCombinations(out, exp_out))

    def _areCombinations(self, items1:'list[list[Any]]', 
                         items2:'list[list[Any]]') -> 'bool':
        hshst = set()
        for item in items1:
            hshst.add(frozenset(item))
        
        for item in items2:
            item = frozenset(item)
            if item not in hshst:
                return False
            hshst.remove(item)
        
        return len(items1) == len(items2)


    
        

class TestCorrectValues(unittest.TestCase):
    def setUp(self):
        self.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.hypotheses = [
            Hypothesis(0, [0], True, True),
            Hypothesis(0, [1], False, False),
            Hypothesis(0, [2], False, False),
            Hypothesis(1, [0], False, False),
            Hypothesis(1, [1], True, True),
            Hypothesis(1, [2], False, False),
            Hypothesis(2, [0], False, False),
            Hypothesis(2, [1], False, False),
            Hypothesis(2, [2], True, True)
        ]

    def test_known_correct_values(self):
        correct_values = known_correct_values(self.grid, self.hypotheses)
        self.assertSetEqual(correct_values, {1, 5, 9})

    def test_known_correctly_placed_values(self):
        correctly_placed_values = known_correctly_placed_values(self.grid,
                                                                self.hypotheses)
        self.assertSetEqual(correctly_placed_values,
                         {(0, 1),
                          (1, 5),
                          (2, 9)})


class TestValuesToIndices(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_values_to_indices(self):
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        row = 0
        values = [2, 3]
        self.assertTrue(values_to_indices(grid, row, values) == [1, 2])

    def test_values_to_indices_empty(self):
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        row = 0
        values = []
        self.assertTrue(values_to_indices(grid, row, values) == [])

    def test_values_to_indices_all(self):
        grid = [[1, 2], [2], [1]]
        row = 0
        values = [1, 2]
        self.assertTrue(values_to_indices(grid, row, values) == [0, 1])

    



if __name__ == '__main__':
    unittest.main()


    
  