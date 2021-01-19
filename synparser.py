from typing import List


def treeifyexpr(expr):
    return treeify(list(expr))


def treeifysrc(source):
    return treeify(list("( " + source + " )"))


def treeify(src: List[str]):  # converts (f (g 3) 4) to [f, [g, 3], 4]
    # invariant: src is in the form (*)
    #print("processing: ", ''.join(src))
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
                        #print(''.join(elements[-1]),src)
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
    return list(map(treeify, cleansed))
