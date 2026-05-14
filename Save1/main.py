from Utility import *
from Grass import *
from Wood import *
from Carrot import *
from Pumpkin import *
from Sunflower import *
from Weird import *
from Cactus import *
from Maze import *
from Dinosaur import *


from temp import *

# ----ITEM MAP DICTIONARY-----
# This maps the item to the function needed to collect said item
item_map = dict()
item_map[Items.Hay] = (grass)
item_map[Items.Wood] = (wood)
item_map[Items.Carrot] = (carrot)
item_map[Items.Pumpkin] = (pumpkin)
item_map[Items.Weird_Substance] = (weird)
item_map[Items.Power] = (power)
item_map[Items.Cactus] = (cactus)
item_map[Items.Gold] = (gold)
item_map[Items.Bone] = (bone)

# -----Entity Map DICTIONARY-----
# Maps the item to the entity
entity_map = dict()
entity_map[Items.Hay] = Entities.Grass
entity_map[Items.Wood] = Entities.Tree
entity_map[Items.Carrot] = Entities.Carrot
entity_map[Items.Pumpkin] = Entities.Pumpkin
entity_map[Items.Power] = Entities.Sunflower
entity_map[Items.Weird_Substance] = None
entity_map[Items.Cactus] = Entities.Cactus
entity_map[Items.Gold] = Entities.Treasure
entity_map[Items.Bone] = Entities.Dinosaur

# -----UNLOCK MAP DICTIONARY-----
# Maps the item to the Unlock
unlock_map = dict()
unlock_map[Items.Hay] = num_unlocked(Unlocks.Grass)
unlock_map[Items.Wood] = num_unlocked(Unlocks.Trees)
unlock_map[Items.Carrot] = num_unlocked(Unlocks.Carrots)
unlock_map[Items.Pumpkin] = num_unlocked(Unlocks.Pumpkins)
unlock_map[Items.Power] = num_unlocked(Unlocks.Sunflowers)
unlock_map[Items.Weird_Substance] = num_unlocked(Unlocks.Fertilizer)
unlock_map[Items.Cactus] = num_unlocked(Unlocks.Cactus)
unlock_map[Items.Gold] = num_unlocked(Unlocks.Mazes)
unlock_map[Items.Bone] = num_unlocked(Unlocks.Dinosaurs)

def get_unlock(thing):
	for i in get_cost(thing):
		starting_power = 0
		
		if (num_unlocked(Unlocks.Sunflowers) > 0):
			power((get_cost(thing)[i]) * .033)
		starting_power = num_items(Items.Power)
		starting_time = get_time()
		starting_tick = get_tick_count()
		item_map[i](get_cost(thing)[i])
		# Power consumption seemsto very closely mirror the time required. E.g. 1774.22 Seconds > 1796.57 Power
		quick_print("Power:", starting_power - num_items(Items.Power), "Time:", get_time() - starting_time, "Ticks:", get_tick_count() - starting_tick)
	unlock(thing)

def crop_cost(item, goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2
	quick_print("World Size:", WORLD_SIZE, "Field Size:", FIELD_SIZE)

	def grass_cost(goal):
		return ceil(goal/cost_reference[item][1])
	
	def bush_cost(goal):
		return ceil(goal/cost_reference[item][1])

	def tree_cost(goal):
		return ceil(goal/(cost_reference[item][1] * 3))
	
	def carrot_cost(goal):
		crop = ceil(goal/cost_reference[item][1])
		sum = crop
		sum += tree_cost(crop * cost_reference[item][1])
		sum += grass_cost(crop * cost_reference[item][1])
		return sum

	def pumpkin_cost(goal):
		multiplier = 0
		if WORLD_SIZE <= 6:
			multiplier = WORLD_SIZE * cost_reference[item][1]
		else:
			multiplier = 6 * cost_reference[item][1]
		crop = ceil(goal / multiplier / FIELD_SIZE) * FIELD_SIZE
		sum = ceil(crop * 1.3)
		sum += carrot_cost(ceil(crop * 1.3) * cost_reference[item][1])
		return sum

	def sunflower_cost(goal):
		FULL_HARVEST = ((((FIELD_SIZE - 9) * 5) + 9) * cost_reference[item][1])
		crop = ceil(goal / FULL_HARVEST) * FIELD_SIZE
		sum = crop
		sum += carrot_cost(crop * cost_reference[item][1])
		return sum
	
	def weird_cost(goal):
		# With current distribution, appears to cover 80% of crops. Harvested crop provides 50% of yield as strange substance. 40% of total yield is then strange
		return pumpkin_cost(goal * 2.5) 
	
	def cactus_cost(goal):
		UNIT_HARVEST = (num_unlocked(Unlocks.Cactus) - 1) ** 2
		sum = ceil((goal - num_items(Items.Cactus)) / ((UNIT_HARVEST * FIELD_SIZE) ** 2)) * FIELD_SIZE
		sum += pumpkin_cost(sum * UNIT_HARVEST)
		return sum
	
	def gold_cost(goal):
		return -1
	
	def bone_cost(goal):
		return -1
	
	# -----COST REFERENCE DICTIONARY-----
	# Provides the function and number of unlocks associated with the unlock
	cost_reference = dict()
	cost_reference[Entities.Grass] = ((grass_cost), 2 ** (num_unlocked(Unlocks.Grass) - 1))
	cost_reference[Entities.Bush] = ((bush_cost), 2 ** (num_unlocked(Unlocks.Plant) - 1))
	cost_reference[Entities.Tree] = ((tree_cost), 2 ** (num_unlocked(Unlocks.Trees) - 1))
	cost_reference[Entities.Carrot] = ((carrot_cost), 2 ** (num_unlocked(Unlocks.Carrots) - 1))
	cost_reference[Entities.Pumpkin] = ((pumpkin_cost), 2 ** (num_unlocked(Unlocks.Pumpkins) - 1))
	cost_reference[Entities.Sunflower] = ((sunflower_cost), 2 ** (num_unlocked(Unlocks.Sunflowers) - 1))
	cost_reference[Items.Weird_Substance] = ((weird_cost), 2 ** (num_unlocked(Unlocks.Sunflowers) - 1))
	cost_reference[Entities.Cactus] = ((cactus_cost), 2 ** (num_unlocked(Unlocks.Cactus) - 1))
	#Treasure
	#Dinosaurs
	cost_reference[Entities.Treasure] = ((gold_cost), 2 ** (num_unlocked(Unlocks.Mazes) - 1))
	cost_reference[Entities.Dinosaur] = ((bone_cost), 2 ** (num_unlocked(Unlocks.Dinosaurs) - 1))
	
	return cost_reference[item][0](goal)

def cheap_unlock():
	answer = None
	current = -1
	
	# Cycle through all unlocks, comparing the predicted cost and select the cheapest
	for i in Unlocks:
		sum = 0
		curr_unlock = get_cost(i)

		# No unlock cost (completed), continue
		#if get_cost(i).len() > 0:
		if curr_unlock.len() < 1:
			continue

		for j in curr_unlock:
			if num_unlocked(j) < 1:
				sum = -1
				break
			checking = crop_cost(entity_map[j], get_cost(i)[j])
			# IS THIS IF STATEMENT NEEDED?
			# if (checking > 0):
			# 	sum += checking
			sum += checking
		
		# Invalid unlock option, continue
		if (sum == -1):
			continue
		
		# I don't remember the logic of this check
		if ((sum < current) and (current > -1)):
			answer = i
			current = sum
	
	if (num_unlocked(Unlocks.Sunflowers) >  1):
		answer += crop_cost(Entities.Sunflower, current * .033)
	return answer

for test in range(1):
	temp = cheap_unlock()
	quick_print ("Upgrage Selected:", temp, get_cost(temp))
	#get_unlock(temp)

#weird(100)