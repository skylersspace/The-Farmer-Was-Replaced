from Utility import *
from Carrot import *

def weird(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	PUMPKIN_HARVEST = 2 ** (num_unlocked(Unlocks.Pumpkins) - 1)

	def plus_center():
		center_list = []
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				if ((i % 2) == 0):
					if ((j - ((i / 2) % 3)) % 3) == 0:
						center_list.append((i, j))
		return center_list
	
	center_list = plus_center()
	while (num_items(Items.Weird_Substance) < len(center_list)):
		plant(Entities.Grass)
		use_item(Items.Fertilizer)
		harvest()

	def normal():
		# This uses pumpkins due to harvest simplicity
		carrot(ceil(FIELD_SIZE * 1.3) * PUMPKIN_HARVEST)

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
				field_map.append((x_pos, y_pos))
			field_map.pop(0)

		for i in center_list:
			move_to(i[0], i[1])
			use_item(Items.Weird_Substance)

		harvest()
	
	while (num_items(Items.Weird_Substance) < goal):
		normal()