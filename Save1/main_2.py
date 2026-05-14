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

WORLD_SIZE = get_world_size()
FIELD_SIZE = WORLD_SIZE ** 2
quick_print(WORLD_SIZE, FIELD_SIZE)
quick_print("")

def stand_yield(thing):
	return FIELD_SIZE * master_map[thing]["unit"]

def pumpkin_yield(thing):
	multiplier = 0
	if WORLD_SIZE <= 6:
		multiplier = WORLD_SIZE * master_map[thing]["unit"]
	else:
		multiplier = 6 * master_map[thing]["unit"]
	return FIELD_SIZE * multiplier

def power_yield(thing):
	# Actual yield will be less due to power consumed during the run
	return 8 * (FIELD_SIZE - 9) + 9

def cactus_yield(thing):
	return FIELD_SIZE ** 2 * master_map[thing]["unit"]

def gold_yield(thing):
	return None

# ERROR: I'm still having issues with consistent runs with the Dinosaur. FIX!!!
def bone_yield(thing):
	return FIELD_SIZE ** 2 * master_map[thing]["unit"]

#Cactus and Dinosaur have same yield formula

def get_yield(thing):
	reset()
	quick_print("Benchmarking", thing)
	# NOTE: When assesing costs, power can be calculated off time, and not actual yield due to all crops using power.
	master_map[thing]["unit"] = 2 ** (num_unlocked(master_map[thing]["unlock"]) - 1)
	master_map[thing]["yield"] = master_map[thing]["yield_func"](thing)
	# Get cost crops
	if (master_map[thing]["cost"] != None):
		for i in master_map[thing]["cost"]:
			#quick_print(i, master_map[i]["function"], master_map[thing]["cost"][i], master_map[thing]["yield"])
			master_map[i]["function"](ceil( master_map[thing]["cost"][i] * master_map[thing]["unit"] * FIELD_SIZE) )
	start_count = num_items(thing)
	start_time = get_time()
	start_ops = get_tick_count()

	master_map[thing]["function"](start_count + 1)

	op_count = get_tick_count() - start_ops
	time_elapsed = get_time() - start_time
	actual_harvest = num_items(thing) - start_count
	master_map[thing]["time"] = time_elapsed / master_map[thing]["yield"]

	quick_print("Cost - Expected:", master_map[thing]["yield"],
			 "Actual:", actual_harvest,
			 "Poly:", actual_harvest - master_map[thing]["yield"],
			 "Base:", master_map[thing]["unit"],
			 "Average:", actual_harvest / FIELD_SIZE,
			 "Ops:", op_count,
			 "OpC:", actual_harvest / FIELD_SIZE,
			 "Time:", time_elapsed,
			 "TpC", master_map[thing]["time"] * 1000, "ms")
	# quick_print(master_map[thing])
	quick_print("")

def get_all_yield():
	for i in item_unlocks:
		if (num_unlocked(i) > 0):
			testing = item_unlocks[i]
			get_yield(testing)

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
		clear()
		till_all()
		reset()

		# Current, base cost, field harvest, time, operations
		answer = [False, cost_reference[item][1], None, None, None]

		answer[1] = 2 ** (num_unlocked(Unlocks.Grass) - 1)
		answer[2] = answer[0] * FIELD_SIZE
		start_count = num_items(Items.Hay)
		start_time = get_time()
		start_ops = get_tick_count()
		grass(start_count + answer[2])
		answer[4] = get_tick_count() - start_ops
		answer[3] = get_time() - start_time
		field_harvest = num_items(Items.Hay) - start_count
		quick_print("Grass Cost - Expected:", answer[2], "Actual,", field_harvest, "Poly:", field_harvest - answer[2], "Base:", answer[1], "Average:", field_harvest / FIELD_SIZE, "Ops:", answer[4], "OpC:", field_harvest / FIELD_SIZE, "Time:", answer[3], "TpC", answer[3] / FIELD_SIZE)
		quick_print(answer)

		answer[0] = True
		return answer
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
		if curr_unlock.len() < 1:
			continue

		for j in curr_unlock:
			if num_unlocked(j) < 1:
				sum = -1
				break
			
			quick_print(get_cost(i), j, get_cost(i)[j])
			sum += crop_cost(master_map[j]["entity"], get_cost(i)[j])
		
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

def replace_the_farmer():
	for test in range(1):
		next_unlock = cheap_unlock()
		quick_print ("Upgrage Selected:", next_unlock, get_cost(next_unlock))
		#get_unlock(temp)

		if (next_unlock in {Unlocks.Expand, Unlocks.Speed, Unlocks.Sunflowers} or (next_unlock == Unlocks.Sunflowers and num_unlocked(Unlocks.Sunflowers) == 1)):
			quick_print("Global Invalidation")
			for i in master_map:
				master_map[i]["valid"] = False
				# Instead of just marking this false, I should just go ahead and recalculate it
				get_yield(i)
			continue

		if next_unlock in item_unlocks:
			quick_print("Item Invalidation")
			master_map[item_unlocks[next_unlock]]["valid"] = False
			# Instead of just marking this false, I should just go ahead and recalculate it
			get_yield(item_unlocks[next_unlock])

		pet_the_piggy()
		do_a_flip()

# ----ITEM MAP DICTIONARY-----
# This maps the item to the various values and functions needed to collect said item
master_map = {
	Items.Hay : {
		"entity": 	Entities.Grass,
		"unlock": 	Unlocks.Grass,
		"function": grass,
		"unit": 	0,
		"yield_func": stand_yield,
		"yield": 	0,
		"time": 	0,
		"cost":		None
	},
	Items.Wood : {
		"entity":   Entities.Tree,
		"unlock":   Unlocks.Trees,
		"function": wood,
		"unit":     0,
		"yield_func": stand_yield,
		"yield":    0,
		"time":     0,
		"cost":		None
	},
	Items.Carrot : {
		"entity":   Entities.Carrot,
		"unlock":   Unlocks.Carrots,
		"function": carrot,
		"unit":     0,
		"yield_func": stand_yield,
		"yield":    0,
		"time":     0,
		"cost":		{Items.Hay: 1, Items.Wood: 1}
	},
	Items.Pumpkin : {
		"entity":   Entities.Pumpkin,
		"unlock":   Unlocks.Pumpkins,
		"function": pumpkin,
		"unit":     0,
		"yield_func": pumpkin_yield,
		"yield":    0,
		"time":     0,
		"cost":		{Items.Carrot: 1.3} # 1.3 is an arbitrary number to account for dead pumpkins
	},
	Items.Weird_Substance : {
		"entity":   None,
		"unlock":   Unlocks.Fertilizer,
		"function": (weird),
		"unit":     0,
		"yield_func": stand_yield,
		"yield":    0,
		"time":     0,
		"cost":		None
	},
	Items.Power : {
		"entity":   Entities.Sunflower,
		"unlock":   Unlocks.Sunflowers,
		"function": power,
		"unit":     0,
		"yield_func": power_yield,
		"yield":    0,
		"time":     0,
		"cost":		{Items.Carrot: 1}
	},
	Items.Cactus : {
		"entity":   Entities.Cactus,
		"unlock":   Unlocks.Cactus,
		"function": (cactus),
		"unit":     0,
		"yield_func": cactus_yield,
		"yield":    0,
		"time":     0,
		"cost":		None
	},
	Items.Gold : {
		"entity":   Entities.Treasure,
		"unlock":   Unlocks.Mazes,
		"function": (gold),
		"unit":     0,
		"yield_func": gold_yield,
		"yield":    0,
		"time":     0,
		"cost":		None
	},
	Items.Bone : {
		"entity":   Entities.Dinosaur,
		"unlock":   Unlocks.Dinosaurs,
		"function": (bone),
		"unit":     0,
		"yield_func": bone_yield,
		"yield":    0,
		"time":     0,
		"cost":		None
	}
}

item_unlocks = {
	Unlocks.Grass : Items.Hay,
	Unlocks.Trees : Items.Wood,
	Unlocks.Carrots : Items.Carrot,
	Unlocks.Pumpkins : Items.Pumpkin,
	Unlocks.Sunflowers : Items.Power,
	Unlocks.Cactus : Items.Cactus,
	Unlocks.Mazes : Items.Gold,
	Unlocks.Dinosaurs : Items.Bone
}

#replace_the_farmer()

#clear()
#harvest_all()
till_all()
reset()

# get_all_yield()
for i in range(2):
	get_yield(Items.Bone)