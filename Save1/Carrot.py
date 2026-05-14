from Utility import *
from Grass import *
from Wood import *

def carrot_old(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Carrots) - 1)
	
	crops = ceil((goal - num_items(Items.Carrot)) / UNIT_HARVEST)

	#FULL_HARVEST = FIELD_SIZE * UNIT_HARVEST
	#quick_print("Crops:", crops, "Full Harvest:", FULL_HARVEST)

	wood(crops * UNIT_HARVEST)
	grass(crops * UNIT_HARVEST)
	
	def full_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Carrot)
				move(North)
			move(East)

	def full_harvest():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder = 0
				harvest()
				plant(Entities.Carrot)
				move(North)
			move(East)
	
	def mixed_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder += 0
				harvest()
				if (remainder > 0):
					plant(Entities.Carrot)
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
				plant(Entities.Carrot)
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

	till_all()
	reset()
	if (crops > FIELD_SIZE):
		#quick_print("Beginning Full Carrot")
		full_plant()
		crops -= FIELD_SIZE
		#quick_print("Full Plant - crops:", crops)
		while (crops > FIELD_SIZE):
			full_harvest()
			crops -= FIELD_SIZE
			#quick_print("Full Harvest - crops:", crops)
		mixed_harvest(crops)
	else:
		#quick_print("Beginning Partial Carrot")
		partial_plant(crops)
		reset()
	partial_harvest(crops)

def carrot(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Carrots) - 1)
	FULL_HARVEST = UNIT_HARVEST * FIELD_SIZE
	
	def full_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Carrot)
				move(North)
			move(East)

	def full_harvest():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					quick_print("Carrot awaiting harvest")
				harvest()
				move(North)
			move(East)
	
	def carrot_cycle():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					quick_print("Carrot awaiting harvest")
				harvest()
				plant(Entities.Carrot)
				move(North)
			move(East)

	till_all()
	wood(goal - num_items(Items.Wood))
	grass(goal - num_items(Items.Hay))
	if (num_items(Items.Carrot) < goal):
		full_plant()
		while(num_items(Items.Wood) + FULL_HARVEST < goal):
			carrot_cycle()
		full_harvest()