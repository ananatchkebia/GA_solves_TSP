import random
import sys
class SpecificWay:
    def __init__(self, sequence_of_cities, fitness_score):
        self.sequence_of_cities = sequence_of_cities
        self.fitness_score = fitness_score
        self.accumulative_fitness_value = None
    
class Population:
    
    #def __init__(self):
    #    self.population = []
    def __init__(self, cities = None, city_number = None , population_size = None, distancies = None):
        self.population = []
        if cities and city_number and population_size and distancies:
            for n in range(population_size):
                one_way = Population.random_sequence_of_cities(cities,city_number)
                one_way_object = SpecificWay(one_way, self.fitness_score_determination(one_way,cities,distancies))
                self.population.append(one_way_object)
    '''
    def _init__(self, *args):
        if len(args) == 0:
            self.population = []
        elif len(args) > 0:
            self.population = []
            for n in range(args[2]):
                one_way = Population.random_sequence_of_cities(args[0],args[1])
                one_way_object = SpecificWay(one_way, self.fitness_score_determination(one_way,args[0],args[3]))
                self.population.append(one_way_object)
    '''
    @staticmethod
    def random_sequence_of_cities(cities, N):
        '''
        Generating initial population of cities randomly selected from all 
        possible permutations  of the given cities
        Input:
        1- Cities list 
        2. Number of population 
        Output:
        Generated lists of cities
        '''
        init_pop = []
        while(len(init_pop) < N-1):
            random_number = random.randint(0, N-1)
            alreadyAdded = False
            for k in init_pop:
                if(k == cities[random_number]): 
                    alreadyAdded = True
            if not alreadyAdded:
                init_pop.append(cities[random_number])
        init_pop.append(init_pop[0])
        return init_pop
    def auxiliary_function(cities,city):
        for n in range(len(cities)):
            if(cities[n] == city): return n
    def fitness_score_determination(self,one_way,cities,distancies):
        fitness_score = 0
        for n in range(len(one_way)-1):
            dist = distancies[Population.auxiliary_function(cities,one_way[n])][Population.auxiliary_function(cities,one_way[n+1])]
            if(dist == sys.maxsize): continue
            fitness_score += dist
        return fitness_score
    def print_population(self):
        for individ in self.population:
            print(individ.sequence_of_cities)
            print(individ.fitness_score)
            print(individ.accumulative_fitness_value)
    def selection(self):
        sum = 0
        for way in self.population:
            sum += way.fitness_score
        for way in self.population:
            way.fitness_score = way.fitness_score/sum
        for n in range(len(self.population)):
            accumulative_fitness_value = self.population[0].fitness_score
            for counter in range(n):
                accumulative_fitness_value += self.population[counter].fitness_score
            self.population[n].accumulative_fitness_value = accumulative_fitness_value
        random_number = random.uniform(0,1)
        new_population = Population()
        for individ in self.population:
            if(individ.accumulative_fitness_value < random_number):
                new_population.population.append(individ)
        return new_population
        
def main():
    population_size = 10
    cities = ["Foti", "Batumi", "Ureki", "Qobuleti", "Gori", "Kutaisi", "Tbilisi", "Mtskheta", "Telavi", "Oni"]
    distancies = [[0,10,18,60,9,30,33,66,56,8],
                  [10,0,88,42,sys.maxsize,18,11,sys.maxsize,12,sys.maxsize],
                  [18,88,0,40,9,30,39,66,56,18],
                  [60,42,40,0,19,30,33,55,56,1],
                  [9,sys.maxsize,9,sys.maxsize,10,30,33,64,56,85],
                  [30,18,sys.maxsize,85,9,50,12,66,56,48],
                  [33,11,18,sys.maxsize,9,30,10,66,56,sys.maxsize],
                  [66,sys.maxsize,18,60,39,30,33,0,56,8],
                  [56,12,18,60,9,sys.maxsize,33,64,0,8],
                  [8,sys.maxsize,28,sys.maxsize,9,30,33,66,56,0]
                  ]
    new_obj = Population(cities = cities,city_number = len(cities),population_size = population_size,distancies = distancies)
    new_obj.print_population()
    new_population = new_obj.selection()
    new_obj.print_population()
    new_population.print_population()
        
    
if __name__ == "__main__":
    main()

