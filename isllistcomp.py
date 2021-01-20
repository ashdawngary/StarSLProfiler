from casting import trynum
from defines import handle_define
from lamstructs import pythoniclam, pythonlamwcontext
from listops import quicklist, intify
from printing import topylist
from shortcuts import num
from synparser import treeifyexpr

foldr_src = treeifyexpr(
    "(define (foldr f base lox) (cond [(empty? lox) base] [(cons? lox) (f (first lox) (foldr f base (rest lox)))]))")
compose_src = treeifyexpr(
    "(define (compose f g) (lambda (x) (f (g x))))")
filter_src = treeifyexpr(
    "(define (filter pred lox) (cond [(empty? lox) empty] [(cons? lox) (if (pred (first lox)) (cons (first lox) (filter pred (rest lox))) (filter pred (rest lox))])))")
map_src = treeifyexpr("(define (map f l) (cond [(empty? l) empty] [(cons? l) (cons (f (first l)) (map f (rest l)))]))")
andmap_src = treeifyexpr(
    "(define (andmap f l) (cond [(empty? l) #t] [(cons? l) (and (f (first l)) (andmap f (rest l)))]))")
ormap_src = treeifyexpr(
    "(define (ormap f l) (cond [(empty? l) #f] [(cons? l) (or (f (first l)) (ormap f (rest l)))]))")
blist_src = treeifyexpr("(define (build-list n f) (map f (ztnmi n)))")


def apply(gc, params):
    return params.pop(0).exec(gc, topylist(params[0]))


def export_listcomp(context):
    listcomps = [foldr_src, compose_src, filter_src, map_src, andmap_src, ormap_src, blist_src]
    for comp in listcomps:
        context = handle_define(context, comp)
    context["apply"] = pythonlamwcontext(apply, "apply")
    context["ztnmi"] = pythoniclam(lambda x: quicklist(list(map(num, list(range(intify(trynum(x)["value"])))))), "ztnmi")
    return context
