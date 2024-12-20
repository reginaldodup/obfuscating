# obfuscating

obfuscate.py is a script to obfuscate python code.

It is capable of obfuscating scripts as well as entire projects.

## Example

Consider you have the following python code in a file called ```print.py```:

```{python}
print("Hello World")
# This is a comment
for i in range(10):
    print(f"We are counting {i}")
```

Running ```obfuscate.py print.py```` will:
- Create a folder ```obs``` for the obfuscated project.
- Create a json file to record the replaced names.
- Create a file ```print.py``` inside this folder with the following contents:

```
lll = "abcdefghijklmnopqrstuvwxyz"
lll+= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lll+= "1234567890"
lll+= "\""
lll+= '\''
lll+= r"[({<>})]-=*\|!@#$%^&/?+.,_: "
print(lll[33]+lll[4]+lll[11]+lll[11]+lll[14]+lll[91]+lll[48]+lll[14]+lll[17]+lll[11]+lll[3])
# CMTllllllllll
for llllllllll in range(10):
    print(lll[48]+lll[4]+lll[91]+lll[0]+lll[17]+lll[4]+lll[91]+lll[2]+lll[14]+lll[20]+lll[13]+lll[19]+lll[8]+lll[13]+lll[6]+lll[91]+f'{llllllllll}')
```

And it will run exactly as the previous one.
