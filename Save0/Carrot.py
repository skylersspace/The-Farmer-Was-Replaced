from Utility import *

def carrot(goal, benchmark = False, verbose = False):
	GROWTH_RATE_CARROT = (4.8, 7.2)
	world_size = get_world_size()
	full_world_size = pow(world_size, 2)
	# CALCULATE WATER LEVELS?
	unit_harvest = num_unlocked(Unlocks.Carrots)
	full_harvest = unit_harvest * full_world_size

	# Carrots are very simple like grass or bushes
	# 	The only complication is that 'seeds' are required to plant
	#	Trading was removed from the game - Planting automatically deducts the planting cost

	# The planting cost can be handled in one of two ways:
	#	1: The calling function must understand that a deduction is required, and handle it
	#	2: This function will calculate the cost when it is called, and handle it
	# I like method 2 as all the scope and complexity around this is now handled by this function

	# Harvest amount is determined by upgrades and the world size

	def carrot_cost(amount):
		# The cost of carrots seem to scale with the upgrades unlocked
		# 1 Carrot = 1 Wood, 1 Hay

		# -----INVESTIGATE-----
		# I don't know what will happen if I try to plant, but there isn't enough resources

		# grass(amount * unit_harvest)
		# wood(amount * unit_harvest)
		starting_hay = num_items(Items.Hay)
		starting_wood = num_items(Items.Wood)
		quick_print("Requesting", amount, "hay and wood")
		grass(amount)
		wood(amount)
		quick_print("Received", num_items(Items.Hay) - starting_hay, "hay and", num_items(Items.Wood) - starting_wood, "wood")

	def carrot_normal():
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)
		while (num_items(Items.Carrot) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					plant(Entities.Carrot)
					move(North)
				move(East)

	def carrot_clean():
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)
		while (num_items(Items.Carrot) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					plant(Entities.Carrot)
					move(North)
				move(East)

		harvest_all_v2()

#Fertilizer is not necessary for this crop

	def carrot_benchmark():
		def run_benchmark(tester):
			clear_tilled()
			reset()
			if verbose:
				quick_print("")
				quick_print(tester[1])
				quick_print("Starting Water:", get_water())
			
			start_hay = num_items(Items.Hay)
			start_wood = num_items(Items.Wood)
			start_num = num_items(Items.Carrot)
			start_time = get_time()
			start_ops = get_tick_count()
			
			tester[0]()
			
			ops_used = get_tick_count() - start_ops
			time_elapsed = get_time() - start_time
			items_produced = num_items(Items.Carrot) - start_num

			if verbose:
				quick_print("Goal:", goal, "Items Produced:", items_produced)
				quick_print("Time Elapsed:", time_elapsed)
				quick_print("     Items per second:", (items_produced / time_elapsed))
				quick_print("Operations Used:", ops_used)
				quick_print("     Operations per item:", (ops_used / items_produced))
				quick_print("Excess - Hay:", num_items(Items.Hay) - start_hay, " - Wood:", num_items(Items.Wood) - start_wood)
			return (time_elapsed, ops_used, items_produced/time_elapsed, ops_used/items_produced)

		func_list = [
				[carrot_normal, "Normal Carrots", 0],
				[carrot_clean, "Clean Carrots", 0]
			]
		
		for i in func_list:
			i[2] = run_benchmark(i)

		quick_print("")
		quick_print("-----------------")
		quick_print("Benchmark Results")
		quick_print("-----------------")
		quick_print("Name : Time : Operations: Items/Sec : Ops/Item")
		for i in func_list:
			quick_print(i[1], ":", i[2][0], ":", i[2][1], ":", i[2][2], ":", i[2][3])

	if benchmark:
		carrot_benchmark()
	else:
		carrot_normal()
		# if (num_unlocked(Unlocks.Watering) > 0):
		# 	if num_unlocked(Unlocks.Watering > 0):
		# 		quick_print("")
		# 	else:
		# 		quick_print("")
		# else:
		# 	if num_unlocked(Unlocks.Watering > 0):
		# 		quick_print("")
		# 	else:
		# 		quick_print("")

#VERSION 3 - FASTEST
def carrot_all_water():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			while not can_harvest():
				quick_print(get_water())
				do_a_flip()
			harvest()
			water_check(.22, 1)
			plant(Entities.Carrot)
			move(North)
		move(East)
		
carrot (5000, True, True)