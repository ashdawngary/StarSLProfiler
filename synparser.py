from typing import List


def cleanit(src):
    return delcomments(src.replace('Î»', chr(955))).replace("\n", " ").replace("\t", " ").replace("\r", " ")


def delcomments(src):
    q = list(src)
    keep = True
    final = []
    while len(q) > 0:
        nex = q.pop(0)
        if nex == ";":
            keep = False
        elif nex in ["\n", "\r"]:
            keep = True
        if keep:
            final.append(nex)
    return ''.join(final)


def treeifyexpr(expr):
    return treeify(list(cleanit(expr)))


def treeifysrc(source):
    return treeify(list("( " + cleanit(source) + " )"))


def tryint(x): # nothing but sketch
    try:
        int(x)
    except:
        return float(x)
    if float(x) != int(x):
        return float(x)
    else:
        return int(x)


def qcast(maybesym):
    try:
        float(maybesym[1:])
        return str(tryint(maybesym[1:]))
    except:
        pass
    if maybesym[1] == '#':
        return maybesym[1:]
    elif maybesym[1] == '"' and maybesym[-1] == '"':
        return maybesym[1:]
    else:
        return maybesym


def symbolize(para):
    start = ["list"]
    for i in para:
        if type(i) == str:
            start.append(qcast("'" + i))
        else:
            start.append(symbolize(i))
    return start


def treeify(src: List[str]):  # converts (f (g 3) 4) to [f, [g, 3], 4]
    # invariant: src is in the form (*)
    # print("processing: ", ''.join(src))
    if not src[0] in ["(", "["]:
        return ''.join(src)  # its an identifier.

    elements = [[]]
    src.pop()  # end
    src.pop(0)  # front
    while len(src) > 0:
        nextele = src.pop(0)
        if nextele == " ":
            elements.append([])
        elif nextele in ["(", "["]:
            stk = 1
            elements.append([])
            elements[-1].append(nextele)
            while stk > 0:
                nextele = src.pop(0)
                if nextele in ["(", "["]:
                    elements[-1].append(nextele)
                    stk += 1
                elif nextele in [")", "]"]:
                    elements[-1].append(nextele)
                    stk -= 1
                elif nextele in ["\""]:
                    ts = 1
                    elements[-1].append(nextele)
                    while ts > 0:
                        # print(''.join(elements[-1]),src)
                        nextele = src.pop(0)
                        elements[-1].append(nextele)
                        if nextele == "\"":
                            ts = 0
                else:
                    elements[-1].append(nextele)
        elif nextele in ["\""]:
            stk = 1
            elements[-1].append(nextele)
            while stk > 0:
                nextele = src.pop(0)
                elements[-1].append(nextele)
                if nextele == "\"":
                    stk = 0
        else:
            elements[-1].append(nextele)
    # (print "abcd") -> [["p" "r" "i" "n" "t"] ["\"" "a" "b" "c" "d" "\"]] -> ["print" "\"abcd\""]
    cleansed = filter(lambda x: len(x) > 0, elements)
    cleansed = list(map(treeify, cleansed))
    revised = []
    quotenex = False
    for para in cleansed:
        if quotenex:
            revised.append(symbolize(para))
            quotenex = False
        else:
            if para == "\'":
                quotenex = True
            else:
                revised.append(para)
    return revised
