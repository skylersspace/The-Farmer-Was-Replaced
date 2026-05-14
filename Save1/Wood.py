from Utility import *

WORLD_SIZE = get_world_size()
FIELD_SIZE = WORLD_SIZE ** 2

def bush(goal):
	crops = (goal - num_items(Items.Wood))
	
	def full_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Bush)
				move(North)
			move(East)
	
	def full_harvest():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder = 0
				harvest()
				plant(Entities.Bush)
				move(North)
			move(East)
	
	def mixed_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder += 0
				harvest()
				if (remainder > 0):
					plant(Entities.Bush)
					remainder -= 1
				move(North)
			move(East)
	
	def partial_plant(remainder):
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					break
				plant(Entities.Bush)
				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	def partial_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					break
				while not can_harvest():
					remainder += 0
				harvest()
				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	if (crops > FIELD_SIZE):
		reset()
		full_plant()
		crops -= FIELD_SIZE
		while (crops > FIELD_SIZE):
			full_harvest()
			crops -= FIELD_SIZE
		mixed_harvest(crops)
	else:
		reset()
		partial_plant(crops)
		reset()
	partial_harvest(crops)

def bush_simple(goal):
	def bush_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				plant(Entities.Bush)
				move(North)
			move(East)

	def bush_cycle():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				harvest()
				plant(Entities.Bush)
				move(North)
			move(East)

	def bush_harvest():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				harvest()
				move(North)
			move(East)
	
	bush_plant()
	while(num_items(Items.Wood) + FIELD_SIZE < goal):
		bush_cycle()
	bush_harvest()

def tree(goal):
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Trees) - 1)

	def calc_crops():
		return ceil((goal - num_items(Items.Wood)) / (UNIT_HARVEST * 3))
	
	def full_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if on_grid():
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
				move(North)
			move(East)

	def full_harvest():
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder = 0
				poly_check = num_items(Items.Wood)
				harvest()
				if on_grid():
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
				move(North)
			move(East)
	
	def mixed_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					remainder += 0
				harvest()
				if (remainder > 0):
					if on_grid():
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)
					remainder -= 1

				move(North)
			move(East)
	
	def partial_plant(remainder):
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					break
				if on_grid():
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	def partial_harvest(remainder):
		for i in range (WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if (remainder <= 0):
					break
				while not can_harvest():
					remainder += 0

				harvest()

				remainder -= 1
				move(North)
			if (remainder <= 0):
				break
			move(East)
	
	reset()
	crops = calc_crops()
	if (crops > FIELD_SIZE):
		full_plant()
		crops -= FIELD_SIZE
		while (crops > FIELD_SIZE):
			full_harvest()
			crops = calc_crops()
		mixed_harvest(crops)
	else:
		partial_plant(crops)
		reset()
	partial_harvest(crops)

def tree_simple(goal):
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Trees) - 1)
	FULL_HARVEST = FIELD_SIZE * UNIT_HARVEST * 3
	
	def tree_plant():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				if on_grid():
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
				move(North)
			move(East)
	
	def tree_cycle():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					quick_print("Tree awaiting harvest")
				harvest()
				if on_grid():
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
				move(North)
			move(East)

	def tree_harvest():
		for i in range(WORLD_SIZE):
			for j in range (WORLD_SIZE):
				while not can_harvest():
					quick_print("Tree awaiting harvest")
				harvest()
				move(North)
			move(East)

	tree_plant()
	while(num_items(Items.Wood) + FULL_HARVEST < goal):
		tree_cycle()
	tree_harvest()

def wood(goal):
	if (num_items(Items.Wood) < goal):
		if (num_unlocked(Unlocks.Carrots) > 0):
			till_all()
		if num_unlocked(Unlocks.Trees) > 0:
			#tree(goal)
			tree_simple(goal)
		else:
			#bush(goal)
			bush_simple(goal)