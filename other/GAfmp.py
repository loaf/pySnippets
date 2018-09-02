# -*- coding: utf-8 -*-
'''
尝试用遗传算法解决一个示例性问题：求解函数 f(x) = x + 10*sin(5*x) + 7*cos(4*x) 在区间[0,9]的最大值
方法是，在[0,9]之间取90000个点，相当于对90000个x值，这些值中肯定有最大值，但我们不是直接计算，而是随机取100个，当作种子
然后对这100个中用上面的函数进行判断，做出取舍（最差的淘汰、被选中概率与适应函数的值大小成正比、精英机制……）
留下的作为父母，两两交配，产生下一代，产生过程中，对父母的染色体进行交叉配对，变按一定概率变异
'''
import matplotlib.pyplot as plt
import math
import random
import numpy as np

#对用一个二维矩阵表示一代种群，每一行代表一个个体（有一个染色体），是一个17位数组，表示一个17位的2进制数,为了计算方便，低位在前
def init():
    for i in range(0,population_size):
        for j in range(0,chromosome_size):
            generation[i,j]=round(random.random())
        generation[i,chromosome_size]=9#最后一列表示是否被 淘汰
    return generation

#对这代种群的每一个个体，分别计算适应度
def fitness(cur_gen):
    global parent_gen,child_gen
    parent_fitness=np.zeros([population_size,2])
    gv_x=0
    for i in range(population_size):
        for j in range(chromosome_size):
            if parent_gen[i,j] == 1:
                gv_x=gv_x+2**j #将每行转成合并成二进制，然后转成一个10进制
        gv=lower_bound+gv_x*(upper_bound-lower_bound)/(2**chromosome_size-1)#将这个10进制数映射到[0,9]，作为x
        gv_y=gv+10*math.sin(5*gv)+7*math.cos(4*gv) #用上面的x,调用函数，计算出y
        parent_fitness[i,0]=i
        parent_fitness[i,1]=gv_y

    sortV=parent_fitness[np.lexsort(-parent_fitness.T)] #按f(x)值排序
    parent_avg=sortV.mean(axis=0)[1] #此代的平均适应度
    parent_best_fitness=sortV[0,1]#此代的最优适应度
    parent_best_inv=0 #j最优个体，用10进制表示
    for i in range(chromosome_size):
        if parent_fitness[int(sortV[0,0],i)]==1:
            parent_best_inv=parent_best_inv+2**i
    #将此代的代数、平均适应度、最优适应度、最优个体保留到一个数列中
    gen_info.append([cur_gen,parent_avg,parent_best_fitness,parent_best_inv])

    #淘汰父代，保留80%
    for i in range(int(population_size*elitism_rate),population_size):
        parent_gen[i,chromosome_size]=-9

    if elitism_rate>0: #保留精英
        for i in range(int(population_size*elitism_rate)):
            child_gen[i]=parent_gen[i]



#评估,对个体按适应度大小进行排序，并且保存最佳个体
def rank(population_size, chromosome_size,cur_gen):
    global gen_info
    sortV = gen_fitness_Value[np.lexsort(-gen_fitness_Value.T)]
    gen_mean_Value=sortV.mean(axis=0)[1]
    gen_best_Value=sortV[0,1]

    gen_best_inv=0 #最优个体
    for i in range(17):
        if generation[int(sortV[0,0]),i]==1:
            gen_best_inv=gen_best_inv+2**i

    gen_info[cur_gen,0]=cur_gen
    gen_info[cur_gen,1]=gen_mean_Value
    gen_info[cur_gen,2]=gen_best_Value
    gen_info[cur_gen,3]=gen_best_inv

    print(gen_info)


    return
#轮盘赌选择
def selection(population_size,chromosome_size,elitism):
    ...
#单点交叉
def crossover(population_size, chromosome_size, cross_rate):
    ...

#单点变异操作
def mutation(population_size, chromosome_size, mutate_rate):
    return

def main():
    global elitism,population_size,chromosome_size,generation_size,cross_rate,mutate_rate,parent_gen

    parent_gen=init()

    for i in range(int(population_size*elitism_rate),population_size):
        random.random()
        parent_gen[i, chromosome_size] = -9
    print(parent_gen)


    for i in range(0,generation_size):
        #fitness(i)
        #rank(population_size,chromosome_size,i)
        # selection(population_size,chromosome_size,elitism)
        # crossover(population_size,chromosome_size,cross_rate)
        mutation(population_size,chromosome_size,mutate_rate)


    #print(gen_fitness_Value)





elitism = True #是否选择精英操作
elitism_rate=0.1 #精英比例
disuse_rate=0.2#淘汰比例
population_size = 100 #种群大小
chromosome_size = 17#染色体长度
generation_size = 5 #200最大迭代次数
cross_rate = 0.6#交叉概率
mutate_rate = 0.01#变异概率
lower_bound=0
upper_bound=9

gen_fitness_Value=np.zeros([population_size,2])#每一代的适应度值,之所以是二维，主要是加一个序号
gen_info=[]#保存每一代的平均适应度、最大适应度和最佳个体
generation= np.zeros([population_size,chromosome_size+1])
parent_gen=np.zeros([population_size,chromosome_size+1])
child_gen=np.zeros([population_size,chromosome_size+1])


if __name__ == '__main__':
    main()