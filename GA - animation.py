# This program is animating the winner algorithm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from random import randint, shuffle


##################################################################
###################### CONTROL PANEL #############################
##################################################################
# dimensions of the world
range_x = 100
range_y = 100

# how many years (iterations) a guy will spend in each world
iterations = 500

# animation settings
fps = 20

# and the winners is:
winner = "01100010101110010100100100110101000111001011010111111100100101100000010010111111101000101001001010110101111000000001001011011100100101100111011010111011110101101111100011111111101101111111111001001001001110100110101110110001101101101111001111111110111100010011001000100111001110111010110011011100111100110111101111000110111101000111101110000000010100001000000001100011101100100011100110110111101111101101101111000000011010011011101000010011101100001100110010101000101010010110100101111011111111101001001011110111"
##################################################################
##################################################################
##################################################################


##################################################################
################# ANIMATION OF THE WINNER ########################
##################################################################
fig, ax = plt.subplots()
world = np.random.randint(0,2,(range_y,range_x))
mat = ax.matshow(world, cmap='gray')


def animate(i):
	genotype = (world*16 + np.roll(np.roll(world, 1, axis=0), 1, axis=1) + np.roll(np.roll(world, 1, axis=0), 0, axis=1)*2 + np.roll(np.roll(world, 1, axis=0), -1, axis=1)*4 + np.roll(np.roll(world, 0, axis=0), 1, axis=1)*8 + np.roll(np.roll(world, 0, axis=0), -1, axis=1)*32 + np.roll(np.roll(world, -1, axis=0), 1, axis=1)*64 + np.roll(np.roll(world, -1, axis=0), 0, axis=1)*128 + np.roll(np.roll(world, -1, axis=0), -1, axis=1)*256 ) 
	for y in range(range_y):
		for x in range(range_x):
			world[y, x] = int(winner[genotype[y, x]])

	mat.set_data(world)
	return [mat]

anim = animation.FuncAnimation(fig, animate, frames=iterations, interval=1000/fps, blit=True)
#plt.show()
anim.save('Genetic Algorithm - Checkerboard Pattern.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])
##################################################################
##################################################################
##################################################################