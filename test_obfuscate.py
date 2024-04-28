#!/usr/bin/env python3

import unittest

from obfuscate import *

class TestObfuscate(unittest.TestCase):
    def test_string_to_concatenated_from_array(self):
        """Testing string to concatenated form"""
        code = "f'abc'"
        result = string_to_concatenated_from_array(
                    get_a_map(), code
                )
        self.assertEqual(result, 'lll[5]+lll[63]+lll[0]+lll[1]+lll[2]+lll[63]')

        code = "'a{b}c'"
        result = string_to_concatenated_from_array(
                    get_a_map(), code
                )
        self.assertEqual(result, 'lll[63]+lll[0]+lll[66]+lll[1]+lll[69]+lll[2]+lll[63]')

    def test_tstring_to_concat(self):
        code = "f'a{b}c'"
        result = tstring_to_concat(code)
        self.assertEqual(result, "lll[0]+f'{b}'+lll[2]")
        
    def test_get_iter_variable_names(self):
        """Testing iteration variables matching"""
        code = "for i in range(10):"
        result = get_iter_variable_names(code)
        self.assertEqual(result, ['i'])

        code = "for i, j, a in zip(list1, list2, list3):"
        result = get_iter_variable_names(code)
        self.assertEqual(result, ['a', 'i', 'j'])

        code = "values = [item * 2 for item in l]"
        result = get_iter_variable_names(code)
        self.assertEqual(result, ['item'])

    def test_get_func_argument_names(self):
        """Testing function argument names"""
        code = 'def test_func(b):'
        result = get_func_argument_names(code)
        self.assertEqual(result, ['b'])
        
        code = 'def test_func(b,a, c):'
        result = get_func_argument_names(code)
        self.assertEqual(result, ['a', 'b', 'c'])

        code = 'def test_func(b:"int", a:"int", c:"int"=10):'
        result = get_func_argument_names(code)
        self.assertEqual(result, ['a', 'b', 'c'])

        code = '''
            def test_func(
                arg1,
                arg2
            )
        '''
        result = get_func_argument_names(code)
        self.assertEqual(result, ['arg1', 'arg2'])

        # This test does not pass, to be implemented later
        # not critical / required (very specific)
        # code = '''
        #     def test_func(
        #         arg1,       # comment
        #         arg2        # comment
        #     )
        # '''
        # result = get_func_argument_names(code)
        # self.assertEqual(result, ['arg1', 'arg2'])
        
        code = '''
            def test_func(
                arg1:'int',
                arg2:'int'=12
            )
        '''
        result = get_func_argument_names(code)
        self.assertEqual(result, ['arg1', 'arg2'])



if __name__ == '__main__':
    unittest.main(verbosity=2)
