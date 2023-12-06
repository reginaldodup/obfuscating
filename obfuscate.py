#!/usr/bin/env python3
import re

def get_unique_values(l):
    """Returns a list of unique values from a list"""
    l = set(l)
    l = list(l)
    return(sorted(l))

def get_class_names(code):
    """Finds all class names in a string and return it as a list"""
    pattern = r'class\s+(\w+)'
    matches = re.findall(pattern, code)
    return matches

def get_function_names(code):
    """Finds all function names in a string and return it as a list"""
    pattern = r'def\s+(?!__)(\w+)'
    matches = re.findall(pattern, code)
    return matches

def get_func_argument_names(code):
    """Finds all funciton arguments and return it as a list"""
    pattern = r'def\s+\w+\s?\(([^\)]*)\)'
    # pattern = r'def\s+\w+\s?\((.*)\)'
    matches = re.findall(pattern, code, re.DOTALL)
    match_list = []
    for item in matches:
        matche = re.sub(r'\s*\n*', '', item)    # Deal with line breaks
        matche = re.sub(r'=[^,]*', '', matche)  # Deal with default values
        matche = re.sub(r'\:[^,]*', '', matche) # Deal with annotations
        matche = re.split(r',', matche)
        for m in matche:
            match_list.append(m)
    # get only unique values
    match_list = get_unique_values(match_list)
    return match_list

def get_variable_names(code):
    """Find all variable names in a string and return it as a list"""
    pattern = r'\s*(\w+)\s*=\s*'
    matches = re.findall(pattern, code)
    # Remove dunder methods from list
    matches = [item for item in matches if '__' not in item]
    return matches

def get_iter_variable_names(code):
    """Finds all iterables variables and return it as a list"""
    pattern = r'for(.*)in'
    matches = re.findall(pattern, code)
    match_list = []
    for item in matches:
        matche = re.sub(r'\s*\n*', '', item)    # Deal with line breaks
        matche = re.split(r',', matche)
        for m in matche:
            match_list.append(m)
    # get only unique values
    match_list = get_unique_values(match_list)
    return match_list

def get_bin_representation(number):
    """Converts an integer to binary string and return it"""
    num = bin(number)
    num = num[::-1].replace('b', '0')
    num = f'{num:010}'
    num = num.replace('0', 'l')
    num = num[::-1]
    return num

def get_all_comments(code):
    """Finds all single line comments and return it as a list"""
    pattern = r'\s*#.*'
    matches = re.findall(pattern, code)
    return matches

if __name__ == '__main__':
    # print('Starting obfuscate...')
    with open('library.py', 'r') as f:
        code = f.read()

    print(re.sub(
            '.*(#.*)',
            '# comment',
            code
        ))
    # print('CASSES:\n', get_class_names(code))
    # print('\nFUNCTIONS:\n', get_function_names(code))
    # print('\nFUNCTION ARGS:\n', get_func_argument_names(code))
    # print('\nVARIABLE NAMES:\n', get_variable_names(code))
    # print('\nITERABLES:\n', get_iter_variable_names(code))
    # for i in range(10):
    #     print(f'{i:02}: {get_bin_representation(i)}')

    # class_names = get_class_names(code)
    # function_names = get_function_names(code)
    # func_arg_names = get_func_argument_names(code)
    # variable_names = get_variable_names(code)
    # iter_var_names = get_iter_variable_names(code)

    # all_names = (
    #     class_names + 
    #     function_names +
    #     func_arg_names +
    #     variable_names +
    #     iter_var_names 
    # )
    # all_names = get_unique_values(all_names)
    # dic_names = { 
    #     item:get_bin_representation(num) for item, num in zip(
    #         all_names, range(len(all_names))
    #         )
    # }
    # # Replace from list
    # for key in dic_names:
    #     # print(f'{key:20} -> {dic_names[key]}')
    #     code = re.sub(
    #                 f'\\b{key}\\b',
    #                 f'{dic_names[key]}',
    #                 code
    #             )
    # print(code)
    # with open('code.obs.py', 'w') as f:
    #     f.write(code)
