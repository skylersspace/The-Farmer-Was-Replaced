from Utility import *

def maze_check():
	if (move(South)):
		move(North)
		return False
	else:
		return True

def spawn_maze():
	reset()
	harvest()
	plant(Entities.Bush)
	if (num_items(Items.Fertilizer) < (get_world_size() * get_world_size())):
			trade(Items.Fertilizer, (get_world_size() * get_world_size()) - num_items(Items.Fertilizer))
	while not maze_check():
		use_item(Items.Water)
		use_item(Items.Fertilizer)

def lh_maze():
	direction = [North, East, South, West]
	index = 0
	spawn_maze()
	
	#Left wall
	while (True):
		if get_entity_type() == Entities.Treasure:
			harvest()
			break
		else:
			#Go Left
			if move (direction[(index+3) % 4]):
				index = (index + 3) % 4
			#Go Forward
			elif move(direction[index]):
				continue
			#Go Right
			elif move(direction[(index + 1) % 4]):
				index = (index + 1) % 4
			#Go Back
			else:
				move(direction[(index + 2) % 4])
				index = (index + 2) % 4
				
def rh_maze():
	direction = [North, East, South, West]
	index = 0
	spawn_maze()
	
	#Right wall
	while (True):
		if get_entity_type() == Entities.Treasure:
			harvest()
			break
		else:
			#Go Right
			if move(direction[(index + 1) % 4]):
				index = (index + 1) % 4
			#Go Forward
			elif move(direction[index]):
				continue
			#Go Left
			elif move (direction[(index+3) % 4]):
				index = (index + 3) % 4
			#Go Back
			else:
				move(direction[(index + 2) % 4])
				index = (index + 2) % 4

#REUSE MAZE
#MAPPING MAZE
#SOLVE MAPPED MAZE