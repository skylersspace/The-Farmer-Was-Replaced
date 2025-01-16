from Utility import *

def carrot(goal, benchmark = False, verbose = False):
	GROWTH_RATE_CARROT = (4.8, 7.2)
	world_size = get_world_size()
	full_world_size = pow(world_size, 2)

	# CALCULATE WATER LEVELS?
	water_low = 0.22
	water_high = 1.0

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
		grass(amount)
		wood(amount)

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

	def carrot_precise():
		#Same logic as grass, but slightly adapted for carrots
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)

		harvest_map = []
		
		# 1+ Rounds required
		if ((num_items(Items.Carrot) + full_harvest) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					plant(Entities.Carrot)
					move(North)
				move(East)

			# 2+ rounds are required loop
			while ((num_items(Items.Carrot) + (full_harvest * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						plant(Entities.Carrot)
						move(North)
					move(East)

			# Will always run if at least one full harvest is required
			# Replace grass as they are havested until the mark will be reached with what is planted
			# If an even harvest is all that's required, nothing will be planted
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if ((num_items(Items.Carrot) + full_harvest) <= mark):
						harvest_map.append((get_pos_x(),get_pos_y()))
						plant(Entities.Carrot)
					move(North)
				move(East)

		# Plant and map partial field
		else:
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (len(harvest_map) * unit_harvest + num_items(Items.Carrot)) < mark:
						plant(Entities.Carrot)
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (num_items(Items.Carrot) < mark):
					move(East)
				else:
					break

		# Harvest any remaining grass
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

	def carrot_water():
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)
		while (num_items(Items.Carrot) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					water_check(water_low, water_high)
					plant(Entities.Carrot)
					move(North)
				move(East)

	def carrot_water_clean():
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)
		while (num_items(Items.Carrot) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					water_check(water_low, water_high)
					plant(Entities.Carrot)
					move(North)
				move(East)

		harvest_all_v2()

	# There seems to be an intermittent bug I can't replicate with logging
	# A few crops are sometimes left unharvested
	def carrot_water_precise():
		#Same logic as before, but water checks have been added
		mark = num_items(Items.Carrot) + goal
		carrot_cost(goal)

		harvest_map = []
		
		if ((num_items(Items.Carrot) + full_harvest) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					water_check(water_low, water_high)
					plant(Entities.Carrot)
					move(North)
				move(East)

			while ((num_items(Items.Carrot) + (full_harvest * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						water_check(water_low, water_high)
						plant(Entities.Carrot)
						move(North)
					move(East)

			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()

					if ((num_items(Items.Carrot) + full_harvest) <= mark):
						harvest_map.append((get_pos_x(),get_pos_y()))
						water_check(water_low, water_high)
						plant(Entities.Carrot)
					move(North)
				move(East)

		else:
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (len(harvest_map) * unit_harvest + num_items(Items.Carrot)) < mark:
						water_check(water_low, water_high)
						plant(Entities.Carrot)
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (num_items(Items.Carrot) < mark):
					move(East)
				else:
					break

		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

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
				quick_print("Goal:", goal, "Items Produced:", items_produced, "Difference:", items_produced - goal)
				quick_print("Time Elapsed:", time_elapsed)
				quick_print("     Items per second:", (items_produced / time_elapsed))
				quick_print("Operations Used:", ops_used)
				quick_print("     Operations per item:", (ops_used / items_produced))
				quick_print("Excess - Hay:", num_items(Items.Hay) - start_hay, " - Wood:", num_items(Items.Wood) - start_wood)
			return (time_elapsed, items_produced, ops_used, items_produced/time_elapsed, ops_used/items_produced)

		func_list = [
				[carrot_normal, "Normal Carrots", 0],
				[carrot_clean, "Clean Carrots", 0],
				[carrot_precise, "Precise Carrots", 0],
				[carrot_water, "Water Carrots", 0],
				[carrot_water_clean, "Precise Water Carrots", 0],
				[carrot_water_precise, "Precise Water Carrots", 0]
			]
		
		for i in func_list:
			i[2] = run_benchmark(i)

		quick_print("")
		quick_print("-----------------")
		quick_print("Benchmark Results")
		quick_print("-----------------")
		quick_print("Name : Time : Items : Operations: Items/Sec : Ops/Item")
		for i in func_list:
			quick_print(i[1], ":", i[2][0], ":", i[2][1], ":", i[2][2], ":", i[2][3], ":", i[2][4])

	if benchmark:
		carrot_benchmark()
	else:
		if (num_unlocked(Unlocks.Watering) > 0):
			carrot_water_precise()
		else:
			carrot_precise()
		
carrot (5000, True, True)