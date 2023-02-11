import rich.console
import rich.text
import tempfile
import subprocess
import sys

# print(sys.argv)

tf = tempfile.NamedTemporaryFile("wt")
# console = rich.console.Console(record=True,width=80)
console = rich.console.Console(record=True,width=80,file=tf)


inputfile = sys.argv[1]
a = subprocess.check_output(f"zcat {inputfile} | groff -mandoc -Tutf8",shell=True)
b = a.decode("utf-8")


c = b.split("\x08")
d = list()

countAll = len(c)

for i in range(countAll):
    if i == 0 :
        d.append(c[i][:-1])
        continue
    
    charA = c[i-1][-1]
    charB = c[i][0]
    charO = ""
    if charA == charB:
        charO =f"\033[1m{charB}\033[0m"
    elif charA=="_":
        charO =f"\033[4m{charB}\033[0m"
    else:
        charO = charB
    
    if i == countAll-1:
        d.extend([charO,c[i][1:]])
    else:
        d.extend([charO,c[i][1:-1]])
    

console.print(rich.text.Text.from_ansi("".join(d)))

print(console.export_html())