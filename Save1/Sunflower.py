from Utility import *
from Carrot import *

def power(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	# No UNIT_HARVEST for this one. It only has one unlock
	# FULL_HARVEST = 8 * (FIELD_SIZE - 9) + 9

	def normal():
		reset()
		
		# Create a key for each petal count which is assigned an empty array
		# This array will store the xy location of the flower
		# Petal count ranges from 7 - 15
		sun_petal_loc = dict()
		for i in range(7,15+1):
			sun_petal_loc[i] = []
		
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Sunflower)
				sun_petal_loc[measure()].append((get_pos_x(), get_pos_y()))
				if (measure() > 12):
					water_to(0.2)
				move(North)
			move(East)

		#Harvest all the flowers
		for i in range(15, 7-1, -1):
			skip = []
			for j in sun_petal_loc[i]:
				move_to(j[0], j[1])
				if can_harvest():
					# temp = num_items(Items.Power)
					harvest()
				else:
					use_item(Items.Water)
					skip.append((j[0], j[1]))
			while skip.len() > 0:
				move_to(skip[0][0], skip[0][1])
				if can_harvest():
					# temp = num_items(Items.Power)
					harvest()
				else:
					use_item(Items.Water)
					skip.append(skip[0])
				skip.pop(0)
			
	carrot(FIELD_SIZE)
	while (num_items(Items.Power) < goal):
		normal()

power(num_items(Items.Power) + 1)