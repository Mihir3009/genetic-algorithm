# Genetic Algorithm

Genetic Algorithm (GA) uses a process of evolution and naturalselection theory to solve complex artificial search problems, andis part of evolutionary computing algorithms. Here, we implemeted the GA to solve the Richardson arm race model and find optimal parameters.

## OuickStart

To use the implemented GA for Richardson arm race model, please use following cmd to clone the code:

```
$ git clone https://github.com/Mihir3009/genetic-algorithm.git
```

### Setup Environment

1. python3.6 <br /> Reference to download and install : https://www.python.org/downloads/release/python-360/
2. Install requirements <br /> 
```
$ pip3 install -r requirements.txt
```

## Run the GA
1. Use default setting as given below:
```
--generation=50 
--population_size=100 
--crossover_rate=0.7 
--mutation_rate=0.1 
--Initial_x=0 
--Initial_y=0 
--Initial_z=0 
--output_dir=./output 
```
To run algorithm, use command:
```
$ sh run.sh
```

2. To change the parameter setting, you need to use command:

```
$ python3 genetic_model.py --generation= # of generation (int)
--population_size= size of population (int) 
--crossover_rate= this rate is between [0,1] (float)
--mutation_rate= this rate is between [0,1] (float)
--Initial_x= initialize x parameter (float) 
--Initial_y= initialize y parameter (float) 
--Initial_z= initialize z parameter (float) 
--output_dir= path of output directory (String)
```

## Working of the GA
To understand the algorithm, please visit 
