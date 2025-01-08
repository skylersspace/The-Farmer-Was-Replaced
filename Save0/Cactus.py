from Utility import *

def plant_cactus():
	buy_seeds_cactus()

	reset()

	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant(Entities.Cactus)
			move(North)
		move(East)

def cactus_bubble():
	buy_seeds_cactus()

	reset()

	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant(Entities.Cactus)
			move(North)
		move(East)

    #Sort X
	for i in range(get_world_size()):
		for i in range(get_world_size()-1):
			for j in range(0, get_world_size()-i-1):
				move_x(j)
				if (measure() > measure(East)):
					swap(East)
		move(North)

    #Sort Y
	for i in range(get_world_size()):
		for i in range(get_world_size()-1):
			for j in range(0, get_world_size()-i-1):
				move_y(j)
				if (measure() > measure(North)):
					swap(North)
		move(East)

	harvest()

def cactus_bubble_pre():
	#create map
	map = []
	for i in range(get_world_size()):
		map.append([])

	buy_seeds_cactus()

	reset()
	
	map = []
	map_sorted = []
	for i in range(get_world_size()):
		map.append([])
		for j in range(get_world_size()):
			plant(Entities.Cactus)
			plant_value = measure()
			map[i].append([plant_value])
			map_sorted.append(plant_value)
			move(North)
		move(East)
	
	bubble_sort(map_sorted)

	#quick_print(map)
	#quick_print("")
	#quick_print(map_sorted)

	#Now for the moving, but how do I do that?

def cactus_bubble_v2():
	buy_seeds_cactus()

	reset()

	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant(Entities.Cactus)
			move(North)
		move(East)

	#This one should sort in x and y at the same time. But how?
	


#till_all()
#reset()
#cactus_bubble()

cactus_bubble_pre()