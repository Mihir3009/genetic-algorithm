###################### import different libraries for use ##############################
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
from os.path import join

############################################# Functions #################################

def rand():
    k11= round(random.uniform(0,1), 3)
    k22= round(random.uniform(0,1), 3)
    k33= round(random.uniform(0,1), 3)
    k23= round(random.uniform(0,1), 3)
    k13= round(random.uniform(0,1), 3)
    k12= round(random.uniform(0,1), 3)

    xm= round(random.uniform(0,1), 3)
    ym= round(random.uniform(0,1), 3)
    zm= round(random.uniform(0,1), 3)

    xs= round(random.uniform(0,1), 3)
    ys= round(random.uniform(0,1), 3)
    zs= round(random.uniform(0,1), 3)
    
    parameters= [k11, k22, k33, k23, k13, k12, xm, ym, zm, xs, ys, zs]
    
    return parameters

def fitness(xn, yn, zn):
    
    stronger= max(xn, yn, zn)
    
    if stronger==xn:
        fit= abs(xn - (yn+zn))
        return fit
    elif stronger==yn:
        fit= abs(yn - (xn+zn))
        return fit
    elif stronger==zn:
        fit= abs(zn - (yn+xn))
        return fit
    

def generate_population(size):
    
    population= []
    
    for i in range(0, size):
        param= rand()
        population.append(param)
    
    return population
    
def tournament_selection(df, size, randomize):
    
    rand = [] 
  
    for i in range(randomize): 
        rand.append(random.randint(0, (size//2)-1))
    
    candidates= [df.iloc[rand[i]].values.tolist() for i in range(randomize)]
    candidates= sorted(candidates, key = lambda x: x[12])
    return candidates[0], candidates[1]
    
def generate_new_population(size, df, c_thresold, m_thresold):
    
    new_population=[]
    
    df= df.iloc[0:(size//2),:]
    
    for i in range(0, size):
        
        candidate1, candidate2 = tournament_selection(df, size, 10)
        rand_no = random.randint(1,10)
        
        #print("[Iter: " + str(i) + " ]")
        
        if rand_no<=c_thresold and rand_no<=m_thresold:
            #print("Inside both")
            cross_candidate1, cross_candidate2= crossover(candidate1, candidate2)
            mutated1= mutation(cross_candidate1)
            mutated2= mutation(cross_candidate2)
            coin= random.randint(0,1)
            if coin==0:
                new_population.append(mutated1)
            else:
                new_population.append(mutated2)
        
        elif rand_no<=c_thresold and rand_no>m_thresold:
            #print("Inside cross")
            cross_candidate1, cross_candidate2= crossover(candidate1, candidate2)
            coin= random.randint(0,1)
            if coin==0:
                new_population.append(cross_candidate1)
            else:
                new_population.append(cross_candidate2)
        
        elif rand_no>c_thresold and rand_no<=m_thresold:
            #print("Inside mute")
            mutated1= mutation(candidate1)
            mutated2= mutation(candidate2)
            coin= random.randint(0,1)
            if coin==0:
                new_population.append(mutated1)
            else:
                new_population.append(mutated2)
        
        else:
            #print("Inside else")
            coin= random.randint(0,1)
            if coin==0:
                new_population.append(candidate1)
            else:
                new_population.append(candidate2)
    #print(len(new_population))
    new_df = pd.DataFrame(new_population, columns=['k11', 'k22', 'k33', 'k23', 'k13', 'k12', 'xm', 'ym', 'zm', 'x_s', 'y_s', 'z_s', 'fitness'])
    return new_df


def crossover(candidate1, candidate2):
    
    pos= random.randint(1,10)
    first1= candidate1[0:pos]
    second1= candidate2[pos:13]
    cross_candidate1= first1 + second1
    
    first2= candidate2[0:pos]
    second2= candidate1[pos:13]
    cross_candidate2= first2 + second2
    
    return cross_candidate1, cross_candidate2


def mutation(candidate):
    
    val1= round(random.uniform(0,1), 3)
    val2= round(random.uniform(0,1), 3)
    pos= random.randint(0,11)
    coin= random.randint(0,1)
    
    if coin==0:
        candidate[pos] = val1
    else:
        candidate[pos] = val2
        
    return candidate

##################################### Main Function ####################################

def main():
    parser= argparse.ArgumentParser()
    
    # Required Argument
    parser.add_argument("--generation",
                        default="",
                        type=int,
                        required=True,
                        help="How many generation you want to produce or how many epochs you want to run your program")
    
    parser.add_argument("--population_size",
                        default="",
                        type=int,
                        required=True,
                        help="Decide the size of population")
                        
    parser.add_argument("--output_dir",
                        default="",
                        type=str,
                        help="give a path to output directory")
    
    #Other Parameters
    parser.add_argument("--crossover_rate",
                        default=0.3,
                        type=float,
                        help="Initialize value of crossover rate between [0,1]")
    
    parser.add_argument("--mutation_rate",
                        default=0.2,
                        type=float,
                        help="Initialize value of mutation rate between [0,1]")
                        
    parser.add_argument("--Initial_x",
                        default=0,
                        type=float,
                        help="Initialize value of x between [0,1]")
    
    parser.add_argument("--Initial_y",
                        default=0,
                        type=float,
                        help="Initialize value of y between [0,1]")
    
    parser.add_argument("--Initial_z",
                        default=0,
                        type=float,
                        help="Initialize value of z between [0,1]")
    
    args= parser.parse_args()
    fit=[]
    
    # Generate population
    size= args.population_size
    population= generate_population(size)
    df = pd.DataFrame(population, columns=['k11', 'k22', 'k33', 'k23', 'k13', 'k12', 'xm', 'ym', 'zm', 'x_s', 'y_s', 'z_s'])
    for i in range(0, args.generation):
        
        fitness_temp= []
        
        for j in range(0, size):
            x_temp= []
            y_temp= []
            z_temp= []              
            x_temp.append(args.Initial_x)
            y_temp.append(args.Initial_y)
            z_temp.append(args.Initial_z)
            for k in range(0, args.generation):
                stronger= max(x_temp[k], y_temp[k], z_temp[k])

                if stronger==x_temp[k] or stronger==0:
                    xn= x_temp[k] + (df.iloc[j,0]*(df.iloc[j,9]-x_temp[k]) + df.iloc[j,3]*(y_temp[k]+z_temp[k]))*(df.iloc[j,6]-x_temp[k])
                    yn= y_temp[k] + (df.iloc[j,1]*(df.iloc[j,10]-y_temp[k]) + df.iloc[j,4]*(x_temp[k]-z_temp[k]))*(df.iloc[j,7]-y_temp[k])
                    zn= z_temp[k] + (df.iloc[j,2]*(df.iloc[j,11]-z_temp[k]) + df.iloc[j,5]*(x_temp[k]-y_temp[k]))*(df.iloc[j,8]-z_temp[k])
        
                elif stronger==y_temp[k]:
                    xn= x_temp[k] + (df.iloc[j,0]*(df.iloc[j,9]-x_temp[k]) + df.iloc[j,3]*(y_temp[k]-z_temp[k]))*(df.iloc[j,6]-x_temp[k])
                    yn= y_temp[k] + (df.iloc[j,1]*(df.iloc[j,10]-y_temp[k]) + df.iloc[j,4]*(x_temp[k]+z_temp[k]))*(df.iloc[j,7]-y_temp[k])
                    zn= z_temp[k] + (df.iloc[j,2]*(df.iloc[j,11]-z_temp[k]) + df.iloc[j,5]*(y_temp[k]-x_temp[k]))*(df.iloc[j,8]-z_temp[k])
        
                elif stronger==z_temp[k]:
                    xn= x_temp[k] + (df.iloc[j,0]*(df.iloc[j,9]-x_temp[k]) + df.iloc[j,3]*(z_temp[k]-y_temp[k]))*(df.iloc[j,6]-x_temp[k])
                    yn= y_temp[k] + (df.iloc[j,1]*(df.iloc[j,10]-y_temp[k]) + df.iloc[j,4]*(z_temp[k]-x_temp[k]))*(df.iloc[j,7]-y_temp[k])
                    zn= z_temp[k] + (df.iloc[j,2]*(df.iloc[j,11]-z_temp[k]) + df.iloc[j,5]*(x_temp[k]+y_temp[k]))*(df.iloc[j,8]-z_temp[k])

                x_temp.append(xn)
                y_temp.append(yn)
                z_temp.append(zn)
            
            fitness_val = fitness(x_temp[args.generation-1], y_temp[args.generation-1], z_temp[args.generation-1])
            fitness_temp.append(fitness_val)
        
        x_temp= []
        y_temp= []
        z_temp= []              
        x_temp.append(args.Initial_x)
        y_temp.append(args.Initial_y)
        z_temp.append(args.Initial_z)
        
        df['fitness']= fitness_temp
        df= df.sort_values(by=['fitness'])
        
    
        for k in range(0, args.generation):
            stronger= max(x_temp[k], y_temp[k], z_temp[k])
    
            if stronger==x_temp[k] or stronger==0:
                xn= x_temp[k] + (df.iloc[0,0]*(df.iloc[0,9]-x_temp[k]) + df.iloc[0,3]*(y_temp[k]+z_temp[k]))*(df.iloc[0,6]-x_temp[k])
                yn= y_temp[k] + (df.iloc[0,1]*(df.iloc[0,10]-y_temp[k]) + df.iloc[0,4]*(x_temp[k]-z_temp[k]))*(df.iloc[0,7]-y_temp[k])
                zn= z_temp[k] + (df.iloc[0,2]*(df.iloc[0,11]-z_temp[k]) + df.iloc[0,5]*(x_temp[k]-y_temp[k]))*(df.iloc[0,8]-z_temp[k])
        
            elif stronger==y_temp[k]:
                xn= x_temp[k] + (df.iloc[0,0]*(df.iloc[0,9]-x_temp[k]) + df.iloc[0,3]*(y_temp[k]-z_temp[k]))*(df.iloc[0,6]-x_temp[k])
                yn= y_temp[k] + (df.iloc[0,1]*(df.iloc[0,10]-y_temp[k]) + df.iloc[0,4]*(x_temp[k]+z_temp[k]))*(df.iloc[0,7]-y_temp[k])
                zn= z_temp[k] + (df.iloc[0,2]*(df.iloc[0,11]-z_temp[k]) + df.iloc[0,5]*(y_temp[k]-x_temp[k]))*(df.iloc[0,8]-z_temp[k])
        
            elif stronger==z_temp[k]:
                xn= x_temp[k] + (df.iloc[0,0]*(df.iloc[0,9]-x_temp[k]) + df.iloc[0,3]*(z_temp[k]-y_temp[k]))*(df.iloc[0,6]-x_temp[k])
                yn= y_temp[k] + (df.iloc[0,1]*(df.iloc[0,10]-y_temp[k]) + df.iloc[0,4]*(z_temp[k]-x_temp[k]))*(df.iloc[0,7]-y_temp[k])
                zn= z_temp[k] + (df.iloc[0,2]*(df.iloc[0,11]-z_temp[k]) + df.iloc[0,5]*(x_temp[k]+y_temp[k]))*(df.iloc[0,8]-z_temp[k])

            x_temp.append(xn)
            y_temp.append(yn)
            z_temp.append(zn)
        
        fit.append(df.iloc[0,12])
        print("Production of Generation " + str(i+1) + " is finished.")
        
        if i!=(args.generation - 1):
            df = generate_new_population(size, df, args.crossover_rate*10, args.mutation_rate*10)
            print("New Generation " + str(i+2) + " is created.")
        print("#---------------------------------------------#")
    print("\n\n*----------------------------------------------------------*")
    print("You got the best generation after crossover and mutation!!!")
    print("*----------------------------------------------------------*")
    
    dir= args.output_dir
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    df=df.iloc[0:1,:]
    df.to_csv(join(dir,'results.csv'))
    
    plt.plot(fit, 'b')
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.savefig(join(dir,'Model_Fit.png'))
    plt.show()
    
    plt.plot(x_temp,'r', label="Country x")
    plt.plot(y_temp,'b', label="Country y")
    plt.plot(z_temp,'g', label="Country z")
    plt.legend(loc="upper right")
    plt.ylim(0, 1.2)
    plt.xlabel('Generations')
    plt.ylabel('Arm Race')
    plt.savefig(join(dir,'Model_GA.png'))
    plt.show()
    
main()
