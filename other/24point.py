# -*- coding: utf-8 -*-
import itertools
import random

def GenAllExpr(card_4, ops_iter):
    allexpr = []
    try:
        while True:

            l = list(ops_iter.__next__()) + card_4
            its = itertools.permutations(l, len(l))
            try:
                while True:
                    yield its.__next__()
            except StopIteration:
                pass
    except StopIteration:
        pass


def CalcRes(expr, isprint=False):
    opmap = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b,
             '/': lambda a, b: a / (b + 0.0)}
    expr_stack = []
    while expr:
        t = expr.pop(0)
        if type(t) == int:
            expr_stack.append(t)
        else:
            if len(expr_stack) < 2:
                return False
            else:
                a = expr_stack.pop()
                b = expr_stack.pop()
                if isprint:
                    print(a, t, b, '=', opmap[t](a, b))
                try:
                    expr_stack.append(opmap[t](a, b))
                except ZeroDivisionError:
                    return False
    return expr_stack[0]


if __name__ == "__main__":
    card =[4,4,7,7]
    print(card)

    ops = itertools.combinations_with_replacement('+-*/', 3)  # 一个24点的计算公式可以表达成3个操作符的形式
    print(list(ops))

    allexpr = GenAllExpr(card, ops)  # 数和操作符混合，得到所有可能序列
    for expr in allexpr:
        res = CalcRes(list(expr))
        if res and res == 24:
            CalcRes(list(expr), True)  # 输出计算过程
            print("Success")
            break