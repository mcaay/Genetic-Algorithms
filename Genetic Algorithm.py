# This program is trying to find genetically the best algorithm 
# for creating a checkerboard pattern out of random configuration
# on a grid

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from random import randint, shuffle

##################################################################
###################### CONTROL PANEL #############################
##################################################################

# dimensions of the world
range_x = 32
range_y = 32

# how many different guys are created at the start
starting_guys_amount = 30

# into how many different worlds a guy will be dropped
# to see how he is doing
worlds_for_each_guy = 3

# how many years (iterations) a guy will spend in each world
iterations = 100

# what portion of the guys should survive each generation?
surviving_guys_portion = 0.4

# how many generations do we compute?
generations = 120

# what portion of the population should get a genetic mutation?
mutated_guys_portion = 0.5

# how many random bits do we mutate? (out of 512)
mutations = 15

# animation settings
fps = 2

##################################################################
##################################################################
##################################################################


################### Generating random guys #######################
starting_guys = []
for i in range(starting_guys_amount):
	starting_guys.append(np.binary_repr(randint(0, 2**512-1), width=512))

starting_guys_original = starting_guys.copy()
##################################################################


### function that goes through the life of one guy and checks ####
### how he did at the end ########################################
def one_life(guy_number):
	###### go through iterations (years of life of the guy) #####
	for t in range(iterations):
		genotype = (world*16 + np.roll(np.roll(world, 1, axis=0), 1, axis=1) + np.roll(np.roll(world, 1, axis=0), 0, axis=1)*2 + np.roll(np.roll(world, 1, axis=0), -1, axis=1)*4 + np.roll(np.roll(world, 0, axis=0), 1, axis=1)*8 + np.roll(np.roll(world, 0, axis=0), -1, axis=1)*32 + np.roll(np.roll(world, -1, axis=0), 1, axis=1)*64 + np.roll(np.roll(world, -1, axis=0), 0, axis=1)*128 + np.roll(np.roll(world, -1, axis=0), -1, axis=1)*256 ) 
		for y in range(range_y):
			for x in range(range_x):
				world[y, x] = int(starting_guys[guy_number][genotype[y, x]])

	#### evaluate fitness level for all cells and take an average ###
	fitness = -3*(world == np.roll(np.roll(world, 1, axis=0), 0, axis=1)) - 3*(world == np.roll(np.roll(world, 0, axis=0), -1, axis=1)) - 10 + 13*(world == np.roll(np.roll(world, 1, axis=0), -1, axis=1)) + 13*(world == np.roll(np.roll(world, -1, axis=0), -1, axis=1))
	fitness_averages[guy_number].append(np.average(fitness))
##################################################################
##################################################################


##################################################################
############### EVENTS IN ONE GENERATION #########################
##################################################################
def one_generation(generation):
	
	global starting_guys

	global fitness_averages
	fitness_averages = [[] for q in range(starting_guys_amount)]

	############### LIFES IN ONE GENERATION ##########################
	for try_number in range(worlds_for_each_guy):
		# Generating a random world 
		world_original = np.random.randint(0,2,(range_y,range_x))
		for guy in range(starting_guys_amount):
			global world 
			world = world_original.copy()
			one_life(guy)
	##################################################################


	############# sorting guys based on their fitness ################
	fitness_avg_of_avg = np.average(fitness_averages, axis=1)

	fitness_final = []
	for guy in range(starting_guys_amount):
		fitness_final.append([guy, fitness_avg_of_avg[guy]]) 

	def GetKey(item):
		return item[1]
	fitness_final = sorted(fitness_final, key=GetKey, reverse=True)

	global max_fitness_over_generations
	max_fitness_over_generations.append(fitness_final[0][1])
	##################################################################


	################## cutting away the losers #######################
	spared_amount = int(starting_guys_amount*surviving_guys_portion)
	fitness_final = fitness_final[:spared_amount]
	##################################################################


	####################### REPRODUCTION #############################
	# shuffling to randomly select parents from survivors
	#shuffle(fitness_final) #maybe not a good idea
	babies = ["" for q in range(starting_guys_amount)] 
	for i in range(starting_guys_amount):
		for j in range(512):
			# randomly choose a bit after bit from one of the parents
			# to make a baby
			if randint(0, 1):
				babies[i] = babies[i] + starting_guys[fitness_final[(2*i)%spared_amount][0]][j]
			else:
				babies[i] = babies[i] + starting_guys[fitness_final[(2*i+1)%spared_amount][0]][j]
	##################################################################
	

	###################### GENETIC MUTATIONS #########################
	for i in range(int(starting_guys_amount*mutated_guys_portion)):
		for j in range(mutations):
			gene = randint(0,511)
			babies[i] = babies[i][:gene] + str((int(babies[i][gene])+1)%2) + babies[i][gene+1:]
	##################################################################


	##################### BABIES INTO ADULTS #########################
	# If it's still not the last generation, turn babies into adults.
	# If it's the last, save last parents as winners and their fitness
	# levels.
	if generation != (generations-1):
		starting_guys = babies
	else: 
		global fitness_final_last
		fitness_final_last = fitness_final
		global winners
		winners = starting_guys
	##################################################################


##################################################################
##################################################################
##################################################################


##################################################################
####################### RUN THE PROGRAM ##########################
##################################################################
max_fitness_over_generations = []

# run all the generations
for g in range(generations):
	# show how many generations still need to be computed
	print(generations - g, "generations left")
	# run 1 whole generation
	one_generation(g)

# show how fit were the winners and then print them
print(fitness_final_last)
for i in range(starting_guys_amount):
	print(winners[i])

# make a plot of maximum fitness over subsequent generations
plt.plot(max_fitness_over_generations)
plt.show()
##################################################################
##################################################################
##################################################################


##################################################################
################# ANIMATION OF THE WINNER ########################
##################################################################
'''fig, ax = plt.subplots()
world = np.random.randint(0,2,(range_y,range_x))
mat = ax.matshow(world)


def animate(i):
	genotype = (world*16 + np.roll(np.roll(world, 1, axis=0), 1, axis=1) + np.roll(np.roll(world, 1, axis=0), 0, axis=1)*2 + np.roll(np.roll(world, 1, axis=0), -1, axis=1)*4 + np.roll(np.roll(world, 0, axis=0), 1, axis=1)*8 + np.roll(np.roll(world, 0, axis=0), -1, axis=1)*32 + np.roll(np.roll(world, -1, axis=0), 1, axis=1)*64 + np.roll(np.roll(world, -1, axis=0), 0, axis=1)*128 + np.roll(np.roll(world, -1, axis=0), -1, axis=1)*256 ) 
	for y in range(range_y):
		for x in range(range_x):
			world[y, x] = int(winners[fitness_final_last[0][0]][genotype[y, x]])

	mat.set_data(world)
	return [mat]

anim = animation.FuncAnimation(fig, animate, frames=iterations, interval=1000/fps, blit=True)
anim.save('Genetic Algorithm - Checkerboard Pattern.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])'''
##################################################################
##################################################################
##################################################################