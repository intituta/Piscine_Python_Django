#!/usr/bin/python3

import os
import sys
import re
from settings import name, lastname, title, age, profession

def main():
    if (len(sys.argv) != 2):
        return print("bad argument")
    path = sys.argv[1]
    regex = re.compile(".*\.template")
    if not regex.match(path):
        return print("bad format")
    if not os.path.isfile(path):
        return print("not file")
    f = open(path, "r")
    template = "".join(f.readlines())
    f.close()
    file = template.format(
        name=name, lastname=lastname, title=title,
        age=age, profession=profession)
    regex = re.compile("(\.template)")
    path = "".join([path[0:regex.search(path).start()], ".html"])
    f = open(path, "w")
    f.write(file)
    f.close()

if __name__ == '__main__':
    main()
