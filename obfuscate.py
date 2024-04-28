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
    pattern = '(f?r?"[^\"\n]+")' # double quote style
    matches = re.findall(pattern, code)
    pattern = "(f?r?'[^\'\n]+')" # single quote style
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
                    concat_string += f'lll[{a[tstring[i]]}]'
                else:
                    concat_string += f'+lll[{a[tstring[i]]}]'
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
            mapped_str  = f'lll[{a[s[i]]}]'
        else:
            mapped_str += f'+lll[{a[s[i]]}]'
    return mapped_str

def get_a_map(a=""):
    # /!\ Change the name of this variable as it 
    # does not allow users to set a variable a
    # /!\ Do not forget to change also in the write_code_to_file /!\
    a =  "abcdefghijklmnopqrstuvwxyz"
    a += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a += "1234567890"
    a += "\"'"
    a += r"[({<>})]-=*\|!@#$%^&/?+.,_: "
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
            if m not in ['__main__', 'int', 'float', 'list', 'string']:
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
    match_list = []
    for m in matches:
        if m not in ['__main__', 'int', 'float', 'list', 'string']:
            match_list.append(m)
    return match_list

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

def write_code_to_file(code, file_name):
    """Writes obfuscated code to file"""
    file_dir = os.path.dirname(file_name)
    target_dir = os.path.join('obs', file_dir)
    if not os.path.exists(target_dir):
        print(f'Creating {target_dir}...') 
        os.makedirs(target_dir)
    # To be replaced in main by a tree structure file writing
    print(f'Writing {os.path.join("obs", file_name)}')
    with open(os.path.join('obs', file_name), 'w') as f:
        f.write('lll = "abcdefghijklmnopqrstuvwxyz"\n')
        f.write('lll+= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"\n')
        f.write('lll+= "1234567890"\n')
        f.write('lll+= "\\\""\n')
        f.write("lll+= '\\\''\n")
        f.write('lll+= r"[({<>})]-=*\\|!@#$%^&/?+.,_: "\n')
        f.write(code)
        
def obfuscate(file_list, replacement_dic):
    """Obfuscate a list of file basd on a replacement dictionary"""
    for file_name in file_list:
        with open(file_name, 'r') as f:
            code = f.read()
        
        # Use replace instead of regex sub because of special chars (-.\) etc...
        for key in replacement_dic['comments']:
            code = code.replace(key, replacement_dic['comments'][key])

        # Use replace instead of regex sub because of special chars (-.\) etc...
        for key in replacement_dic['strings']:
            code = code.replace(key, replacement_dic['strings'][key])

        for key in replacement_dic['doc_strings']:
            code = re.sub( key, replacement_dic['doc_strings'][key], code)

        # Replace from list
        for key in replacement_dic['names']:
            code = re.sub(
                f'\\b{key}\\b',
                f'{replacement_dic["names"][key]}',
                code
            )
        write_code_to_file(code, file_name)
        # print(f'{file_name = }')
        # print(f'{os.path.dirname(file_name) = }')
        # print(f'{os.path.join("obs", file_name)}')
        # print(code)
    pass

def get_replacement_dic(file_list):
    """Gets all replacement and returns it as a dictionary"""
    
    # Initializing lists
    all_comments = []
    string_list = []
    all_doc_strings = []
    class_names = []
    function_names = []
    func_arg_names = [] 
    variable_names = [] 
    iter_var_names = [] 

    for file_name in file_list:
        with open(file_name, 'r') as f:
            code = f.read()

        print(f'Getting replacements for file: {file_name}')

        # Getting lists
        all_comments += get_all_comments(code)
        string_list += get_all_strings(code)
        all_doc_strings += get_all_doc_strings(code)
        class_names += get_class_names(code)
        function_names += get_function_names(code)
        func_arg_names += get_func_argument_names(code)
        variable_names += get_variable_names(code)
        iter_var_names += get_iter_variable_names(code)

    # Get unique values
    all_comments = get_unique_values(all_comments)
    string_list = get_unique_values(string_list)
    all_doc_strings = get_unique_values(all_doc_strings)
    all_names = (
        class_names + 
        function_names +
        func_arg_names +
        variable_names +
        iter_var_names 
    )
    all_names = get_unique_values(all_names)

    # Make a dictionary for replacement
    all_comments_dic = { 
        all_comments[i] : '# CMT' + get_bin_representation(i) for i in range(len(all_comments))
    }
    string_dic = { 
        text_str:tstring_to_concat(text_str) for text_str in string_list 
    }
    all_doc_strings_dic = { 
        all_doc_strings[i]:f'DOCS{get_bin_representation(i)}' for i in range(len(all_doc_strings))
    }
    dic_names = { 
        item:get_bin_representation(num) for item, num in zip(
            all_names, range(len(all_names))
        )
    }
    
    replacement_dic = dict(
        comments = all_comments_dic,
        strings = string_dic,
        doc_strings = all_doc_strings_dic,
        names = dic_names 
    )
    # print(json.dumps(replacement_dic, indent=2))
    return replacement_dic


if __name__ == '__main__':


    parser = argparse.ArgumentParser(
        description='''Obfuscates python code.'''
    )

    # /!\ modify name to receive one or more files [list]
    # in case we want to obfuscate only some files in a folder
    # /!\ Replace all this by -f, -d, -r options instead
    parser.add_argument('name', metavar='',  help='name: file name or expression')
    parser.add_argument(
        '-t', 
        '--type', 
        nargs='?', 
        default='f', 
        help='Type of target: f=file d=folder (all py files inside a folder) r=regex'
    )
    # All items passed after the -i flag are saved as an array
    parser.add_argument(
        '-i',  
        '--ignore', 
        nargs='+', 
        default=['.git', '.pytest_cache',  '__pycache__'], 
        help='Regex of files/folders to be ignored'
    )
    # Add verbose option for print statements

    args = parser.parse_args()

    cwd = os.getcwd()

    if args.type == 'f':
        # obfuscate_files(args.name)
        file_list = [args.name]
    elif args.type == 'd':
        print(f'Obfuscating python files under folder: {args.name}\n-----')
        file_list = []
        # for root, dirs, files in os.walk(cwd, topdown=False):
        for root, dirs, files in os.walk(args.name, topdown=False):
            ignore_root = False
            for item in args.ignore:
                if item in root:
                    ignore_root = True
                    break
            if not ignore_root:
                # print(f'\nROOT: {root}\n-----') 
                for file in files:
                    if '.py' == file[-3::]:
                        file_list.append(os.path.join(root, file))
    elif args.type == 'r':
        # To be implemented
        # should create a file_list as all the others
        print('Obfuscating python files matching regex pattern')
    else:
        print('Type not supported!')
       
    # print(file_list)
    replacement_dic = get_replacement_dic(file_list)
    obfuscate(file_list, replacement_dic)

    
