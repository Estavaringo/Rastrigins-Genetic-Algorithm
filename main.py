import individual as indv
import numpy as np

SIZE_OF_POPULATION = 50
NUMBER_OF_ITERATIONS = 250
CHANCE_OF_MUTATION = 0.01
CHANCE_OF_CROSSOVER = 0.7

def rastrigins(x,y):
    return 20 + np.power(x,2) + np.power(y,2) - 10 * (np.cos(2*np.pi*x) + np.cos(2*np.pi*y))

def get_chromosome_value(individual):
    chromosomes = [individual.chromosome[i * 10:(i + 1) * 10] for i in range((len(individual.chromosome) + 10 - 1) // 10 )] 
    x = 0
    y = 0
    for bit in chromosomes[0]:
        x = (x << 1) | bit
    for bit in chromosomes[1]:
        y = (y << 1) | bit
        
    x = (x * 0.00978) - 5
    y = (y * 0.00978) - 5

    return x,y

def fitness(individual):
    #recupera os valores contidos no chromossomo do individuo
    x,y = get_chromosome_value(individual)
    individual.rastrigins = rastrigins(x,y)    
    individual.fitness = abs(1/(individual.rastrigins+0.000001)) #SUM IS TO NOT DIVIDE BY ZERO ACCIDENTALY

def grade(population):
    sum = 0
    for individual in population:
        sum = sum + individual.fitness
    return sum / SIZE_OF_POPULATION

def calculate_individual_chance_by_fitness(population):
    sum = 0
    for individual in population:
        sum = sum + individual.fitness
    for individual in population:
        individual.chance = individual.fitness / sum

def calculate_individual_chance_by_rank(population):
    sum = 0
    for individual in population:
        sum = sum + individual.fitness_by_rank
    for individual in population:
        individual.chance = individual.fitness_by_rank / sum

def update_fitness_by_rank(population):
    
    x = SIZE_OF_POPULATION
    
    for individual in population:        
        individual.fitness_by_rank = 1/x
        x = x - 1

def clone(individual):
    new_individual = create_individual()
    new_individual.chromosome = individual.chromosome
    return new_individual

def crossover(a,b):
    if np.random.random() < CHANCE_OF_CROSSOVER:
        i = np.random.randint(0,20)
        new_individual = create_individual()
        for x in range(i):
            new_individual.chromosome[x] = a.chromosome[x]
        for x in range(19-i):
            new_individual.chromosome[x] = b.chromosome[x]  
        return new_individual
    else:
        if np.random.randint(0,2) == 1:
            return clone(a)
        else:
            return clone(b)

def crossover_with_mutation(a,b):
    if np.random.random() < CHANCE_OF_CROSSOVER:
        i = np.random.randint(0,20)
        new_individual = create_individual()
        for x in range(i):
            new_individual.chromosome[x] = b.chromosome[x]
        for x in range(19-i):
            new_individual.chromosome[x] = a.chromosome[x]  
        if np.random.random() < CHANCE_OF_MUTATION:
            new_individual = mutate(new_individual)
        return new_individual
    else:
        if np.random.randint(0,2) == 1:
            return a
        else:
            return b

def mutate(individual):
    i = np.random.randint(0,20)
    if individual.chromosome[i] == 1:
        individual.chromosome[i] = 0
    else:
        individual.chromosome[i] = 1
    return individual

def create_individual():
    return indv.Individual()

def create_popupalion():
    new_population = []
    for x in range(SIZE_OF_POPULATION):
        new_population.append(create_individual())
    return new_population

def individual_selection(population):
    probabilities = [ind.chance for ind in population]
    return np.random.choice(population,None,True,probabilities)        

def generate_new_population(population):
    new_population = []
    for x in range(SIZE_OF_POPULATION):
        a = individual_selection(population)
        b = individual_selection(population)
        new_individual = crossover(a,b)
        if np.random.random() < CHANCE_OF_MUTATION:
            new_individual = mutate(new_individual)
        new_population.append(new_individual)
    return new_population

def main():
    population = create_popupalion()


    for x in range(NUMBER_OF_ITERATIONS):
        
        print("------------- GENERATION " + str(x) + " ---------------")
        
        for individual in population:
            fitness(individual)
            
        #CALCULA MEDIA DOS FITNESS
        average_fitness = grade(population)
                
        population.sort(key=lambda x: x.fitness)

        update_fitness_by_rank(population)


        #calculate_individual_chance_by_fitness(population)
        calculate_individual_chance_by_rank(population)
        
        print("Average fitness: " + str(average_fitness))
        print()
        print("Melhor individuo:")
        print("Function result: " + str(population[SIZE_OF_POPULATION-1].rastrigins))
        print("Fitness: " + str(population[SIZE_OF_POPULATION-1].fitness))
        print("Chance: " + str(population[SIZE_OF_POPULATION-1].chance))
        print()

        #for individual in population:
        
        #    print()
        #    print()

        #    print("Function result: " + str(individual.rastrigins))
        #    print("Fitness: " + str(individual.fitness))
        #    print("Rank Fitness: " + str(individual.fitness_by_rank))
        #    print("Chance: " + str(individual.chance))
        #    print(individual.chromosome)

        if x != NUMBER_OF_ITERATIONS-1 :
            population = generate_new_population(population)   
    
    print("------------- POPULACAO FINAL ---------------")
    for individual in population:
        
        print()
        print()

        print("Function result: " + str(individual.rastrigins))
        print("Fitness: " + str(individual.fitness))
        print("Rank Fitness: " + str(individual.fitness_by_rank))
        print("Chance: " + str(individual.chance))
        print(individual.chromosome)

main()