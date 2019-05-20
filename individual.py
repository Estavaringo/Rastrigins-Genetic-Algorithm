import numpy as np

CHROMOSOME_SIZE = 20

class Individual():

    def __init__(self):
        self.chromosome = []
        self.fitness = 0
        self.fitness_by_rank = 0
        self.rastrigins = 0
        self.chance = 0

        for x in range(CHROMOSOME_SIZE):
            self.chromosome.append(np.random.randint(0,2))
        
         
