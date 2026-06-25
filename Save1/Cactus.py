from Utility import *
from Pumpkin import *

def cactus(goal):
	#quick_print("Starting Cactus:", goal)
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = (num_unlocked(Unlocks.Pumpkins) - 1) ** 2
	FULL_HARVEST = UNIT_HARVEST * FIELD_SIZE

	crops = ceil((goal - num_items(Items.Cactus)) / FULL_HARVEST) * FIELD_SIZE
	#quick_print("Single - Field Harvest:", UNIT_HARVEST, (UNIT_HARVEST * FIELD_SIZE) ** 2)
	#quick_print("Starting Crops:", crops)

	def normal():
		reset()
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				plant(Entities.Cactus)
				move(North)
			move(East)
		
		#Sort X
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE - 1, 0, -1):
				for k in range(0, j):
					move_x(k)
					#quick_print("I, J, K", i, j, k)
					if (measure() > measure(East)):
						#quick_print("Swapping", measure(), measure(East))
						swap(East)
			move(North)

		#Sort Y
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE - 1, 0, -1):
				for k in range(0, j):
					move_y(k)
					if (measure() > measure(North)):
						swap(North)
			move(East)
		
		harvest()

	#get seed crops
	pumpkin(crops * UNIT_HARVEST)
	while (crops > 0):
		normal()
		crops -= FIELD_SIZE

	# TO DO -- TEST OTHER VERSIONS AND METHODS OF SORTING
	# TO DO - TEST PRESORTING AN ARRAY
	# TO DO -- Insertion Sort, Shaker Sort, Gnome Sort

cactus(num_items(Items.Cactus) + 1)