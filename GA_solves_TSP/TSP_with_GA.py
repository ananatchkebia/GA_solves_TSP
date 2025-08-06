import random
import pycountry
from countryinfo import CountryInfo
from math import radians, sin, cos, acos
import tkinter as tk
import matplotlib.pyplot as plt
import copy

Population_Size = 10
Generation_Number = 5
data = []
root = tk.Tk()
root.geometry("400x200")
title = tk.Label(root, text = "Randomly generation of N cities", font = ('Arial',18))
title.pack(pady = 10)
message = tk.Label(root, text = "Please enter value of N: ")
message.pack(pady = 10)
number_var = tk.StringVar()
get_countries_list = [country.name for country in pycountry.countries]

class SpecificWay_Individ:
     def __init__ (self,first_generation = False,countries = None):
         self.N_random_country = []
         self.latitudes = []
         self.longitudes = []
         if(first_generation):
             self.N_random_country.append(countries[0])
             counter = 1
             while(counter<len(countries)):
                 random_index = random.randint(0,len(countries)-1)
                 already_added = False
                 for country in self.N_random_country:
                    if(countries[random_index]==country): already_added = True
                 if(already_added):continue
                 self.N_random_country.append(countries[random_index])
                 counter += 1
             self.N_random_country.append(self.N_random_country[0])

     def Determination_Of_Latitudes_Longitudes(self):
         for country in self.N_random_country:
             country_info = CountryInfo(country)
             self.latitudes.append(country_info.latlng()[0])
             self.longitudes.append(country_info.latlng()[1])

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
         fitnessScoreAdditionalSum = 0
         for value in fitnessScoreAdditional.values():
            fitnessScoreAdditionalSum += value
         for key,value in fitnessScoreAdditional.items():
            self.fitness_scores[key] = value/fitnessScoreAdditionalSum

     def roulette_wheel(self):
         sum = 0
         for key,value in self.fitness_scores.items():
            sum += value
            self.population_fitness_probs_cumsum[key] = sum
         random_number = random.uniform(0,1)
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
         offspring = SpecificWay_Individ()
         offspring.N_random_country = copy.deepcopy(parent_1.N_random_country)
         for i in range(random_start_index,random_end_index+1):
             index=0
             for country in offspring.N_random_country:
                 if(country == parent_2.N_random_country[i]):
                     offspring.N_random_country[index] = offspring.N_random_country[i]
                     offspring.N_random_country[i] = country
                     break
                 index += 1
                 if(index == len(parent_1.N_random_country)-1):break
         print("offspring : ",offspring.N_random_country)
         return offspring

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
             data.append([])
             for individ in currentPopulation.population:
                 individ.Determination_Of_Latitudes_Longitudes()
                 data[i+1].append({"latitude":individ.latitudes,"longitude":individ.longitudes})
         print("generation ",Generation_Number)
         print("Distancies for current population:")
         currentPopulation.minimal_distance()
         currentPopulation.determination_Of_Fitness_Scores()

Population = Set_Of_Specific_Ways_Population(Population_Size)

def generate():
     N_random_country = []
     number = int(number_var.get())
     counter = 0
     while counter < number:
         random_country = random.randint(0,len(get_countries_list)-1)
         country_to_add = get_countries_list[random_country]
         country = CountryInfo(country_to_add)
         try:
            country.capital_latlng()
         except Exception as e:
            continue
         already_added_such_country = False
         for country in N_random_country:
             if(country == country_to_add):
                already_added_such_country = True
         if(already_added_such_country):continue
         N_random_country.append(country_to_add)
         counter =counter + 1

     for population_counter in range(Population_Size):
         Population.population.append(SpecificWay_Individ(first_generation=True,countries= N_random_country))
     print("Initial Population : ")
     for individ in Population.population:
        print("Individ ",individ.N_random_country)
     data.append([])
     for individ in Population.population:
         individ.Determination_Of_Latitudes_Longitudes()
         data[0].append({"latitude":individ.latitudes,"longitude":individ.longitudes})

     GeneticAlgorithm.applyGeneticAlgorithm(Population)

number = tk.Entry(root, textvariable=number_var)
number.pack(pady = 10)
button = tk.Button(root, text = "Generate", font =('Arial',18), command = generate)
button.pack(pady = 10)
root.mainloop()

fig, ax = plt.subplots()

for gen_num in range(len(data)):
     for i, graph_data in enumerate(data[gen_num]):
         ax.set_title(f'Generation: {gen_num+1} Individ: {i+1}')
         ax.plot(graph_data['latitude'], graph_data['longitude'])
         ax.set_xlabel('X-axis')
         ax.set_ylabel('Y-axis')
         plt.pause(0.5)
         plt.draw()
         ax.clear()
plt.show()