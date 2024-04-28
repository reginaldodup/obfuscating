# To be implemented

## Not necessarily in this order.

[x] Arg parsing
[x] Modify write to file function to receive file name, folder name and code to write
[x] Default ignore list ('.git', '__pycache__', etc...)
[ ] Modify code not to lose these defaults when user specify ignore list
[ ] Create json files with the corresponding changes
[x] Write files with the same structure as the target project but under a folder obs
[ ] Transform code to class and add the list items to a class attibute.
[x] Loop through all files in a folder / subfolder when creating the obfuscate list
[ ] Create a function that takes the json file and reverts the obfuscation
[x] Change the name of 'a' map to 'lll' written in the top of the files, as it becomes a bug
    if a user uses 'a' for a varible, function etc name.
[ ] Add ignore options to code
    - Ignore (function names, class names etc)
    - Ignore a list of specific names
    - Ignore names from file (optional, later)

## Bugs

[ ] The code does not work for annotated functions, fix it
    - Today we have a code that ignores built in type like int, float, string
      But it will not work with user defined types.
