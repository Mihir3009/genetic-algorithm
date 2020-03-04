#!/bin/bash

#python3 model.py --iterations=40 --Initial_x=0 --Initial_y=0 --Initial_z=0

python3 genetic_model.py --generation=50 --population_size=100 --crossover_rate=0.7 --mutation_rate=0.1 --Initial_x=0 --Initial_y=0 --Initial_z=0 --output_dir=./output