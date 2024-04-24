import random
import sys
import awoc

from countryinfo import CountryInfo
from math import radians, sin, cos, acos
class SpecificWay_Individ:
    def __init__(number,get_countries_list):
        counter = 0  
        N_random_country = []
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
        N_random_country.append(N_random_country[0])
        return N_random_country
    
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
#class Population:
  
Population = {}
def generate():
    my_world = awoc.AWOC()
    get_countries_list = my_world.get_countries_list()
    number = int(number_var.get())
    Population_Number = 10
    for population_counter in range(Population_Number):   
        Population[population_counter+1] = SpecificWay_Individ(number,get_countries_list)
    for key,value in Population.items():
        print("Population ",key," ",value)
    Distancies = {}
    for key,value in Population.items():
        Distancies[key] = value.Sum_Of_Distancies()
    for key,value in Distancies.items():
        print(key," %.2fkm" % value)
        
import tkinter as tk

root = tk.Tk()
root.geometry("800x500")
title = tk.Label(root, text = "Randomly generation of N cities", font = ('Arial',18))
title.pack(pady = 10)
message = tk.Label(root, text = "Please enter value of N: ")
message.pack(pady = 10)
number_var = tk.StringVar()


number = tk.Entry(root, textvariable=number_var)
number.pack(pady = 10)
button = tk.Button(root, text = "Generate", font =('Arial',18), command = generate)
button.pack(pady = 10)    
root.mainloop()






