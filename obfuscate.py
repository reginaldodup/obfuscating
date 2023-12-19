#!/usr/bin/env python3
import re
import json
import argparse
import os


def get_all_comments(code):  
    """Finds all single line comments and return it as a list"""
    pattern = r'\.*(#.*)'
    matches = re.findall(pattern, code)
    # Deal with shebang line
    matches = [ item for item in matches if item[:2] not in ['#!'] ]
    return matches

def get_all_strings(code):
    """Finds all single line strings and return it as a list"""
    pattern = '(f?r?"[^\"\n]+")'
    matches = re.findall(pattern, code)
    pattern = "(f?r?'[^\'\n]+')"
    matches+= re.findall(pattern, code)
    doc_strings = get_all_doc_strings(code)
    # Remove doc strings
    matches = [ item for item in matches if item[1:-1] not in doc_strings ]
    # Deal with __main__ and with annotations
    matches = [ item for item in matches \
                if item[1:-1] not in ['__main__', 'int', 'float', 'list', 'string'] ]
    return matches

def tstring_to_concat(tstring):
    """Transforms a string to a concatenation of elements of the a array"""
    if tstring[0] == 'f' or tstring[0] == 'r':
        tstring = tstring[2:-1]
    else:
        tstring = tstring[1:-1]
    concat_string = ''
    braces = False
    a = get_a_map()
    for i in range(len(tstring)):
        if tstring[i] == '{':
            braces = True
            if i == 0:
                concat_string += 'f\'{'
            else:
                concat_string += '+f\'{'
        elif tstring[i] == '}':
            braces = False
            concat_string += '}\''
        else:
            if braces:
                concat_string += tstring[i]
            else:
                if i==0:
                    concat_string += f'a[{a[tstring[i]]}]'
                else:
                    concat_string += f'+a[{a[tstring[i]]}]'
    return concat_string

def get_all_doc_strings(code):
    """Finds all doc strings and returns it as a list"""
    pattern = 'f?r?"""([^\"]+)"""'
    matches = re.findall(pattern, code, re.DOTALL)
    pattern = "f?r?'''([^\']+)'''"
    matches+= re.findall(pattern, code, re.DOTALL)
    return matches

def string_to_concatenated_from_array(a, s):
    a = a
    mapped_str = ""
    for i in range(len(s)):
        if mapped_str == "":
            mapped_str  = f'a[{a[s[i]]}]'
        else:
            mapped_str += f'+a[{a[s[i]]}]'
    return mapped_str

def get_a_map(a=""):
    a =  "abcdefghijklmnopqrstuvwxyz"
    a += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a += "1234567890"
    a += "\"'"
    a += r"[({<>})]-=*\|!@#$%^&/?+.,_ "
    return {a[i]:i for i in range(len(a))}

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

def write_code_to_file(code):
    """Writes obfuscated code to file"""
    with open('code.obs.py', 'w') as f:
        f.write('a = "abcdefghijklmnopqrstuvwxyz"\n')
        f.write('a+= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"\n')
        f.write('a+= "1234567890"\n')
        f.write('a+= "\\\""\n')
        f.write("a+= '\\\''\n")
        f.write('a+= r"[({<>})]-=*\\|!@#$%^&/?+.,_ "\n')
        f.write(code)
        
def obfuscate_file(file_name):

    with open(file_name, 'r') as f:
        code = f.read()

    # Comments
    # -------------------
    all_comments = get_all_comments(code)
    # all_comments = { i:all_comments[i] for i in range(len(all_comments))}
    all_comments_dic = { all_comments[i] : '# CMT' + get_bin_representation(i) for i in range(len(all_comments))}
    # print(json.dumps(all_comments_dic, indent=2))
    # Use replace instead of regex sub because of special chars (-.\) etc...
    for key in all_comments_dic:
        code = code.replace(key, all_comments_dic[key])

    # print('\nALL COMMENTS')
    # print('------')
    # print(json.dumps(all_comments, indent=2))
    
    # Strings
    # -------------------
    string_list = get_all_strings(code)
    # print(string_list)
    string_dic = { text_str:tstring_to_concat(text_str) for text_str in string_list }
    # print('\nSTRINGS')
    # print('------')
    # print(json.dumps(string_dic, indent=2))

    # Use replace instead of regex sub because of special chars (-.\) etc...
    for key in string_dic:
        code = code.replace(key, string_dic[key])
        # code = re.sub(key, string_dic[key], code)

    # Doc Strings
    # -------------------
    all_doc_strings = get_all_doc_strings(code)
    # all_doc_strings = { i:all_doc_strings[i] for i in range(len(all_doc_strings)) }
    all_doc_strings_dic = { all_doc_strings[i]:f'DOCS{get_bin_representation(i)}' for i in range(len(all_doc_strings))}

    print('\nALL DOC STRINGS:')
    print('------')
    print(json.dumps(all_doc_strings_dic, indent=2))

    for key in all_doc_strings:
        code = re.sub( key, all_doc_strings_dic[key], code)
    # print(json.dumps(all_doc_strings, indent=2))

    # Other names
    # -------------------
    class_names = get_class_names(code)
    function_names = get_function_names(code)
    func_arg_names = get_func_argument_names(code)
    variable_names = get_variable_names(code)
    iter_var_names = get_iter_variable_names(code)

    all_names = (
        class_names + 
        function_names +
        func_arg_names +
        variable_names +
        iter_var_names 
    )
    all_names = get_unique_values(all_names)
    dic_names = { 
        item:get_bin_representation(num) for item, num in zip(
            all_names, range(len(all_names))
        )
    }
    # Replace from list
    for key in dic_names:
        # print(f'{key:20} -> {dic_names[key]}')
        code = re.sub(
            f'\\b{key}\\b',
            f'{dic_names[key]}',
            code
        )
    write_code_to_file(code)

    print('\nALL NAMES')
    print('------')
    print(json.dumps(dic_names, indent=2))

if __name__ == '__main__':


    parser = argparse.ArgumentParser(
        description='''Obfuscates python code.'''
    )

    parser.add_argument('name' , metavar='',  help='name: file name or expression')
    parser.add_argument('-t', '--type'   , nargs='?', default='f', help='Type of target: f=file d=folder (all py files inside a folder) r=regex')
    # All items passed after the -i flag are saved as an array
    parser.add_argument('-i',  '--ignore', nargs='+', default=[''], help='Regex of files/folders to be ignored')

    args = parser.parse_args()

    cwd = os.getcwd()

    if args.type == 'f':
        file_name = args.name
        obfuscate_file(file_name)
    elif args.type == 'd':
        print('Obfuscating python files under folder')
        for root, dirs, files in os.walk(cwd, topdown=False):
            print(root, files) 
        print(args.ignore)
    elif args.type == 'r':
        print('Obfuscating python files matching regex pattern')
    else:
        print('Type not supported!')
        
