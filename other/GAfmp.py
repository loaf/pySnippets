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
import pandas as pd

#对用一个二维矩阵表示一代种群，每一行代表一个个体（有一个染色体），是一个17位数组，表示一个17位的2进制数,为了计算方便，低位在前
def init():
    for i in range(0,population_size):
        for j in range(0,chromosome_size):
            generation[i,j]=round(random.random())
        generation[i,chromosome_size]=5#最后一列表示是否被 淘汰
    return generation

#对这代种群的每一个个体，分别计算适应度,得到一个标注后的本代矩阵和一个包括所有代的信息列表gen_info
def fitness(cur_gen):
    global parent_gen,gen_info
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
    parent_min_fitness=sortV[population_size-1,1] #此代的最差适应度

    #df1=pd.DataFrame(parent_fitness)
    #df2=pd.DataFrame(sortV)
    #df1.to_csv("../../temp/parent_fitness.csv")
    #df2.to_csv("../../temp/sortV.csv")

    parent_best_inv = 0  ##此代最好个体的十进制表示
    for i in range(chromosome_size):
        if parent_gen[int(sortV[0,0]),i]==1:
            parent_best_inv=parent_best_inv+2**i

    #将此代的代数、平均适应度、最优适应度、最优个体保留到一个数列中
    gen_info.append([cur_gen,parent_avg,parent_best_fitness,parent_best_inv,parent_min_fitness])

    #淘汰父代，前10%直接保留，后面的对每一行，轮盘赌决定是否保留
    for i in range(int(population_size*elitism_rate)):
        parent_gen[int(sortV[i,0]), chromosome_size] = 9

    sumFitness=sum(sortV[int(population_size*elitism_rate):,1])+(population_size-int(population_size*elitism_rate))*abs(parent_min_fitness)
    accumulator = 0 #累积概率
    for i in range(int(population_size*elitism_rate),population_size):
        rndValue=random.random() #取一个[0,1)之间的随机数
        accumulator += (sortV[i, 1] + abs(parent_min_fitness))/sumFitness

        if rndValue>= accumulator:
            parent_gen[int(sortV[i,0]), chromosome_size] = 8
        else:
            parent_gen[int(sortV[i,0]), chromosome_size] = -8

    #df=pd.DataFrame(parent_gen)
    #df.to_csv("../../temp/gen.csv")

    temp_gen = parent_gen[parent_gen[:, chromosome_size] > 0, :]
    rnd = math.floor(random.uniform(0, len(temp_gen) - 2))
    chromosome_Father = temp_gen[rnd, 0:17]
    chromosome_Mather = temp_gen[rnd + 1, 0:17]
    cross_position = math.ceil(random.uniform(1, chromosome_size - 1))
    child1 = chromosome_Father[:cross_position]
    child1.extend(chromosome_Mather[cross_position:])
    child2 = chromosome_Mather[:cross_position]
    child2.extend(chromosome_Father[cross_position:])
    print(chromosome_Father,chromosome_Mather)
    print(child1,child2)

    #对于所有的染色体数据按变异概率进行变异

#单点交叉,每次从父代中随机取2个作为父母，按交叉概率进行染色体交换,方法为，取一个随机数，如果大于交叉概率，不做操作
#交叉方式是，随机取一个[2,16）的值，作为交叉开始点，将开始点后的数据互换，执行100次，填到child_gen中
def crossover(curGen, cross_rate):
    temp_gen=parent_gen[parent_gen[:,chromosome_size]>0,:] #将保留下来的父代放到一个临时数组中
    for i in range(population_size): #执行100次，填满child_gen
        rnd=math.floor(random.uniform(0,len(temp_gen)-2)) #从有效数组中取一个值，如果一共有40行，则范围是[0,38)，为了省事，直接取相邻的两条做父母
        chromosome_Father=temp_gen[rnd,0:17]
        chromosome_Mather=temp_gen[rnd+1,0:17]
        if random.random()<cross_rate:
            cross_position=math.ceil(random.uniform(1,chromosome_size-1)) #第3位到17位取一个随机位
            child1=chromosome_Father[:cross_position]+chromosome_Mather[cross_position:]
            child2=chromosome_Mather[:cross_position]+chromosome_Father[cross_position:]
        print(chromosome_Father)
    return

#单点变异操作，对于每一行个体，取一个随机数，如果小于变异概率，则该条发生变异，然后在此中，随机取一个[0,16)的位置上求反操作
def mutation(mutate_rate):
    return

def main():
    global elitism,population_size,chromosome_size,generation_size,cross_rate,mutate_rate,parent_gen

    parent_gen=init()
    fitness(1)

    #for i in range(0,generation_size):
        #fitness(i)
        #rank(population_size,chromosome_size,i)
        # selection(population_size,chromosome_size,elitism)
        # crossover(population_size,chromosome_size,cross_rate)
        #mutation(population_size,chromosome_size,mutate_rate)

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