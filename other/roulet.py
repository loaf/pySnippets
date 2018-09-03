#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Perform 3 kinds of roulette wheel selections for Evolutionary Algorithms (EAs).

After plotting time efficiency curve, it shows that the Stochastic Acceptance has
the minimum total running time, followed by basic and bisecting search roulette wheel selection algorithms.

-----------------------------------
Created on Mon Feb 29, 2016
@author: mangwang
-----------------------------------
"""


import random
import numpy as np

if __name__ == "__main__":
    fitness = np.array([[4, 2.0], [3, 1.8], [0, 1.4], [1, 1.2], [2, 1.0], [6, 0.7], [7, 0.3], [5, 0.1]])
    sumFits=fitness.sum(axis=0)[1]
    sum2=sum(fitness[1:,1])
    print(sumFits,sum2)

    i=0
    while i<5:
        rndPoint = random.uniform(0, sumFits)
        accumulator=0
        retInd=0
        for ind,val in enumerate(fitness):
            accumulator += val[1]
            if accumulator>=rndPoint:
                retInd=val[0]
                break

        print(sumFits,rndPoint,accumulator,retInd,ind)
        i+=1

