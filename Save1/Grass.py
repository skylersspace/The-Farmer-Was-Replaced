from Utility import *

def grass_old(goal):
	#quick_print("Starting Grass")
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Grass) - 1)
	
	crops = ceil((goal - num_items(Items.Hay)) / UNIT_HARVEST)

	FULL_HARVEST = FIELD_SIZE * UNIT_HARVEST
	#quick_print("Crops:", crops, "Full Harvest:", FULL_HARVEST)
	
	def full_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Grass)
				move(North)
			move(East)
	
	def full_harvest():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder += 0
				harvest()
				plant(Entities.Grass)
				move(North)
			move(East)
	
	def mixed_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder += 0
				harvest()
				if (remainder > 0):
					plant(Entities.Grass)
					remainder -= 1
					#quick_print("Mixed Harvest - crops:", remainder)
				move(North)
			move(East)
	
	def partial_plant(remainder):
		#quick_print("Planting:", remainder)
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					#quick_print("Done Planting!")
					break
				plant(Entities.Grass)
				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	def partial_harvest(remainder):
		#quick_print("Harvesting:", remainder)
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					#quick_print("Done Harvesting!")
					break
				while not can_harvest():
					remainder += 0
				harvest()
				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	if (num_unlocked(Unlocks.Carrots) > 0):
			till_all()

	reset()
	if (crops > FIELD_SIZE):
		full_plant()
		crops -= FIELD_SIZE
		while (crops > FIELD_SIZE):
			full_harvest()
			crops -= FIELD_SIZE
		mixed_harvest(crops)
	else:
		partial_plant(crops)
		reset()
	partial_harvest(crops)

def grass(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Grass) - 1)
	FULL_HARVEST = FIELD_SIZE * UNIT_HARVEST

	def grass_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Grass)
				move(North)
			move(East)

	def grass_cycle():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				harvest()
				plant(Entities.Grass)
				move(North)
			move(East)

	def grass_harvest():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				harvest()
				move(North)
			move(East)

	if (num_unlocked(Unlocks.Carrots) > 0):
		till_all()

	if (num_items(Items.Hay) < goal):
		grass_plant()
		while(num_items(Items.Hay) + FULL_HARVEST < goal):
			grass_cycle()
		grass_harvest()