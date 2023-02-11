# Dream mandoc to html


import rich.console
import rich.text
import tempfile
import subprocess

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("filename")


console_tempfile = tempfile.TemporaryFile()

console = rich.console.Console(record=True,width=80,file=console_tempfile)
# console = rich.console.Console(record=True,width=80)

zcatOutputTemp = tempfile.TemporaryFile()




def dataprocess(input:bytes)->str:
    b = input.decode("utf-8")

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
    return "".join(d)

    



if __name__ == "__main__":
    args = parser.parse_args()
    # print(args.filename)
    # inputfile = ""
    zcatOutput = subprocess.check_output(["zcat", args.filename])
    zcatOutputTemp.write(zcatOutput)
    zcatOutputTemp.flush()
    zcatOutputTemp.seek(0)
    groffOutput = subprocess.check_output(["groff","-mandoc","-Tutf8"],stdin=zcatOutputTemp)

    # a = subprocess.check_output(f"zcat {args.filename} | groff -mandoc -Tutf8",shell=True)
    console.print(rich.text.Text.from_ansi(dataprocess(groffOutput)))
    # console.print(rich.text.Text.from_ansi(dataprocess(a)))
    print(console.export_html())