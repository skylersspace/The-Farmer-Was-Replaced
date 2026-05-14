from Utility import *
from Carrot import *

def pumpkin(goal):
	#quick_print("Starting Pumpkins")
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	UNIT_HARVEST = 2 ** (num_unlocked(Unlocks.Pumpkins) - 1)
	
	multiplier = 0
	if WORLD_SIZE <= 6:
		multiplier = WORLD_SIZE * UNIT_HARVEST
	else:
		multiplier = 6 * UNIT_HARVEST

	FULL_HARVEST = FIELD_SIZE * multiplier
	CARROT_COST = ceil(1.3 * UNIT_HARVEST * FIELD_SIZE)

	def normal():
		reset()

		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				plant(Entities.Pumpkin)
				move(North)
			move(East)

		field_map = []

		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				if not can_harvest():
					field_map.append((get_pos_x(), get_pos_y()))
					plant(Entities.Pumpkin)
				move(North)
			move(East)
		
		while(field_map.len() > 0):
			x_pos = field_map[0][0]
			y_pos = field_map[0][1]
			move_to(x_pos, y_pos)
			if not can_harvest():
				if num_unlocked(Unlocks.Carrots) > 0:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				# if (field_map.len() == 1) and (num_unlocked(Unlocks.Fertilizer) > 0):
				# 	use_item(Items.Fertilizer)
				# 	use_item(Items.Weird_Substance)
				field_map.append((x_pos, y_pos))
			field_map.pop(0)
	
		harvest()

	carrot(((goal - num_items(Items.Pumpkin)) / FULL_HARVEST) * CARROT_COST)
	while (num_items(Items.Pumpkin) < goal):
		if num_items(Items.Carrot) < CARROT_COST:
			quick_print("Aquiring extra carrots")
			carrot(ceil(FIELD_SIZE * 1.3 * UNIT_HARVEST))
		normal()