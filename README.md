# TSP problem solved with genetic algorithm

The travelling salesman problem, also known as the travelling salesperson
problem (TSP), asks the following question: "Given a list of cities and the distances
between each pair of cities, what is the shortest possible route that visits each city
exactly once and returns to the origin city?" It is an NP-hard problem so it cannot be
solved in polynomial time. But there are different algorithms to get solution which is near
to optimal solution. One of them is Genetic algorithm. These algorithms may not deliver
the best possible solution, but they can quickly identify good approximations.

In Computer Science genetic algorithm is inspired by the process of natural
selection. In a genetic algorithm, a population of potential solutions (called individuals,
creatures, organisms) to an optimization problem is evolved toward better solutions.
Each potential solution has a set of properties (chromosomes) which can be mutated.
Therefore, this program solves TSP problem using GA.

## Features

- Program has a simple graphical interface allowing us to randomly generate N
cities. we can pass N number, how many countries we want to have for TSP problem.
After clicking on “generate” button, program generates N random country from the world
and creates initial population.
- Population_size (number of individes in each population)
- Population for this problem is set of countries’ names (tsp problem has
constraint: first and last countries should be the same ones, otherwise all countries
should be unique in set)
- Individe for TSP problem is one specific way for traveler salesman (likelihood one
solution)
- Generation_Number (shows how many times do we reproduce new generation)
- During reproducing new generation cross_over() function is called in
“Population_size” times.
- Cross_over() function is method of class “Set_Of_Specific_Ways_Population”.
Cross_over() function calles roulette_wheel() function in two times to get good parents
for offspring and then using these parents creates new offspring. Here we should use
such cross_over method which creates valid offspring for traveling salesmen
problem(that countries in set remain unique and first and last country be same).
- 20 % of offsprings undergo mutation
- Mutation() method is in class “SpecificWay_Individ”. It simply chooses two random
genes in chromosome(country in specific way) and swaps them.
- Classes have other additional methods for program execution,testing and visualisation.
- class “SpecificWay_Individ” has Determination_Of_Latitudes_Longitudes() method to
determine latitudes and longitudes and add them in data[],which is necessary at the end
for visualisation of program sequential steps.
- fitness scores determination is necessary part of genetic algorithm(roulette
whille() and then cross_over() method are based on this),so in class
“Set_Of_Specific_Ways_Population” we have determination_Of_Fitness_Scores()
method,which uses distancies for each individes of population and determines
fitness_scoress,as individ with minimal distancies had greater probability.
- finally you can see visualisation of all 10 individes of all 5 generations.

## Technologies used

- OOP structure of Python programming language
- Tkinter libraries for GUI 
- Matplotlib library for visualisation
- Genetic Algorithm

## How to run and how to see what this program does
you can use any IDE that supports Python programming language,
ensure you have python installed and all requered python libraries, clone this repository, run "TSP_with_GA.py" file. 
enter number of countries, click on button "generate" and watch at CLI, there you will see initial population that is set of 10 individes,
then you will see distances for all 10 individes from first generation, possible minimal distance and total distance for whole generation,
then second generation is authomatically generated and you can see the same information for it and so on until last 10th generation will be generated and provided same information for it as well.
you can analize minimal and total distances for all generation and make some conclusions))
