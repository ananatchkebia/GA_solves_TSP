import random
import sys
import awoc
from countryinfo import CountryInfo
from math import radians, sin, cos, acos
import tkinter as tk

Population_Size = 10
Generation_Number = 5
root = tk.Tk()
root.geometry("400x200")
title = tk.Label(root, text = "Randomly generation of N cities", font = ('Arial',18))
title.pack(pady = 10)
message = tk.Label(root, text = "Please enter value of N: ")
message.pack(pady = 10)
number_var = tk.StringVar()

my_world = awoc.AWOC()
get_countries_list = my_world.get_countries_list()

class SpecificWay_Individ:
    def __init__ (self,first_generation = False):
        number = int(number_var.get())
        counter = 0  
        self.N_random_country = []
        if(first_generation):
            while counter < number:
                random_country = random.randint(0,len(get_countries_list)-1)
                country_to_add = get_countries_list[random_country]            
                country = CountryInfo(country_to_add)
                try:
                    country.capital_latlng()
                except Exception as e:                
                    continue
                already_added_such_country = False
                for country in self.N_random_country:
                    if(country == country_to_add):
                        already_added_such_country = True
                if(already_added_such_country):continue     
                self.N_random_country.append(country_to_add)
                counter =counter + 1
            self.N_random_country.append(self.N_random_country[0])
            
    def Sum_Of_Distancies(self):
        sum_of_distancies = 0
        for i in range(len(self.N_random_country)-1):
            country_i = CountryInfo(self.N_random_country[i])
            country_i1 = CountryInfo(self.N_random_country[i+1])
            mlat = radians(float(country_i.latlng()[0]))
            mlon = radians(float(country_i.latlng()[1]))
            plat = radians(float(country_i1.latlng()[0]))
            plon = radians(float(country_i1.latlng()[1]))
            dist = 6371.01 * acos(sin(mlat)*sin(plat) + cos(mlat)*cos(plat)*cos(mlon - plon))
            sum_of_distancies += dist
        return sum_of_distancies
    
    def Mutation(self):
        random_index_1 = random.randint(1,len(self.N_random_country)-2)
        random_index_2 = random.randint(1,len(self.N_random_country)-2)
        while(random_index_1 == random_index_2):          
            random_index_1 = random.randint(1,len(self.N_random_country)-2)
            random_index_2 = random.randint(1,len(self.N_random_country)-2)
        temp = self.N_random_country[random_index_1]
        self.N_random_country[random_index_1] = self.N_random_country[random_index_2]
        self.N_random_country[random_index_2] = temp
        
class Set_Of_Specific_Ways_Population:
    def __init__ (self,Population):
        self.population = []
        self.fitness_scores = {}
        self.population_fitness_probs_cumsum = {}
        
    def distancies_for_all_individes(self):
        Distancies = []
        for individ in self.population:
            Distancies.append(individ.Sum_Of_Distancies())
        for distance in Distancies:
            print(" %.2fkm" % distance)
        return Distancies
    
    def minimal_distance(self):
        Distancies = self.distancies_for_all_individes()
        minimalDistance = Distancies[0]
        for distance in Distancies:
            if(distance<=minimalDistance): minimalDistance = distance
        print("minimal distance for current population: ", minimalDistance)
    
    def determination_Of_Fitness_Scores(self):
        sumOfAllIndividesDistancies = 0
        fitnessScoreAdditional = {}
        for individes in self.population:
            sumOfAllIndividesDistancies += individes.Sum_Of_Distancies()
        print("sum of all individes distancies : ",sumOfAllIndividesDistancies)
        for individes in self.population:
            fitnessScoreAdditional[individes] = sumOfAllIndividesDistancies/individes.Sum_Of_Distancies()
        #print("additional fitness scores:")
        #for key,value in fitnessScoreAdditional.items():
        #    print(key.N_random_country,' ',value)
        fitnessScoreAdditionalSum = 0
        for value in fitnessScoreAdditional.values():
            fitnessScoreAdditionalSum += value
        #print("sum of additional fitness scores : ",fitnessScoreAdditionalSum)
        for key,value in fitnessScoreAdditional.items():
            self.fitness_scores[key] = value/fitnessScoreAdditionalSum
        #print("fitness scores:")
        #for key,value in self.fitness_scores.items():
         #   print(key.N_random_country,' ',value) 
    
    def roulette_wheel(self):
        sum = 0
        for key,value in self.fitness_scores.items():
            sum += value
            self.population_fitness_probs_cumsum[key] = sum
        #print("population_fitness_probs_cumsum : ")
        #for key,value in self.population_fitness_probs_cumsum.items():
         #   print(key.N_random_country," ",value)
        random_number = random.uniform(0,1)
        #print("random number : ",random_number)
        for key,value in self.population_fitness_probs_cumsum.items():
            if(value>random_number): 
                return key
            
    def cross_over(self):
        number = int(number_var.get())
        parent_1 = self.roulette_wheel()
        parent_2 = self.roulette_wheel()
        print("parent 1 : ",parent_1.N_random_country)
        print("parent 2 : ",parent_2.N_random_country)
        random_start_index = random.randint(1,len(parent_1.N_random_country)-2)
        random_end_index = random.randint(1,len(parent_1.N_random_country)-2)        
        if(random_start_index>=random_end_index):
            temp = random_start_index
            random_start_index=random_end_index
            random_end_index = temp
        #print("random start index : ",random_start_index)
        #print("random end index : ",random_end_index)
        offspring1 = SpecificWay_Individ()
        for index in range(random_start_index):
            offspring1.N_random_country.append(parent_1.N_random_country[index])
        for index in range(random_start_index,random_end_index+1):
            offspring1.N_random_country.append(parent_2.N_random_country[index])
        for index in range(random_end_index+1,number+1):
            offspring1.N_random_country.append(parent_1.N_random_country[index])
        offspring2 = SpecificWay_Individ()
        for index in range(random_start_index):
            offspring2.N_random_country.append(parent_2.N_random_country[index])
        for index in range(random_start_index,random_end_index+1):
            offspring2.N_random_country.append(parent_1.N_random_country[index])
        for index in range(random_end_index+1,number+1):
            offspring2.N_random_country.append(parent_2.N_random_country[index])
        print("offspring 1 : ",offspring1.N_random_country," ",offspring1.Sum_Of_Distancies())
        print("offspring 2 : ",offspring2.N_random_country," ",offspring2.Sum_Of_Distancies())
        if(offspring1.Sum_Of_Distancies()<offspring2.Sum_Of_Distancies()): return offspring1
        else: return offspring2
        
class GeneticAlgorithm:
    @staticmethod
    def applyGeneticAlgorithm(initialPopulation):
        number = int(number_var.get())
        currentPopulation = initialPopulation
        for i in range(Generation_Number-1):
            print("generation ",i+1)
            nextPopulation = Set_Of_Specific_Ways_Population(Population_Size)
            print("Distancies for current population:")
            currentPopulation.minimal_distance()
            currentPopulation.determination_Of_Fitness_Scores()
            for counter in range(Population_Size):
                print("child ",counter+1)
                nextPopulation.population.append(currentPopulation.cross_over())
                random_number_for_mutation = random.uniform(0,1)
                if(random_number_for_mutation<0.2):
                    nextPopulation.population[counter].Mutation()
                    print("current child underwent mutation.")
                
            currentPopulation = nextPopulation
        print("generation ",Generation_Number)
        print("Distancies for current population:")
        currentPopulation.minimal_distance()
        currentPopulation.determination_Of_Fitness_Scores()
            
Population = Set_Of_Specific_Ways_Population(Population_Size)
       
def generate():
    for population_counter in range(Population_Size): 
        Population.population.append(SpecificWay_Individ(first_generation=True))
    print("Initial Population : ")
    for individ in Population.population:
        print("Individ ",individ.N_random_country)   
    GeneticAlgorithm.applyGeneticAlgorithm(Population)    
    
number = tk.Entry(root, textvariable=number_var)
number.pack(pady = 10)
button = tk.Button(root, text = "Generate", font =('Arial',18), command = generate)
button.pack(pady = 10)    
root.mainloop()

