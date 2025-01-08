from Utility import *

def wood(goal, benchmark = False, verbose = False):
	HARVEST_LEVELS = (0, 1, 0, 0, 0,
				   0, 0, 0, 0, 0,
				   1000)
	# Trees are worth 5 bushes when harvested
	GROWTH_RATE_BUSH = (3.2, 4.8)
	GROWTH_RATE_TREE = (5.6, 8.4)
	# CALCULATE WATER LEVELS?
	world_size = get_world_size()
	full_world_size = pow(world_size, 2)

	unit_harvest = HARVEST_LEVELS[num_unlocked(Unlocks.Trees)] / 100
	full_harvest_bush = unit_harvest * full_world_size
	full_harvest_tree = 0
	# Even distribution
	if (world_size % 2 == 0):
		# Half will be trees, half will be bushes
		full_harvest_tree = (full_world_size / 2) * unit_harvest * 6
	# Odd distribution
	else:
		# There will be slightly more trees than bushes
		full_harvest_tree = (((full_world_size // 2) + 1) * unit_harvest * 5) + ((full_world_size // 2) * unit_harvest)


	# Wood has two sources: Bushes, and Trees
	#	Bushes are consistent with no variability or special harvesting conditions
	#	Trees have variability dependant on the planting pattern, but no special harvesting conditions
	# Can plant faster than able to harvest
	# 	Water (and fertilizer on smaller maps?) can speed up growing time

	#--------
	# BUSHES
	#--------

	# Harvest and plant bushes - Continuous
	# Will leave full field behind
	def bushes_normal():
		mark = num_items(Items.Wood) + goal
		while (num_items(Items.Wood) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					plant(Entities.Bush)
					move(North)
				move(East)

	# Same as bushes_normal, but will harvest everything once completed
	def bushes_clean():
		mark = num_items(Items.Wood) + goal
		while ((num_items(Items.Wood)) < mark):
			for i in range (get_world_size()):
				if (num_items(Items.Wood) >= mark):
					break
				for j in range (get_world_size()):
					if (num_items(Items.Wood) >= mark):
						break
					if can_harvest():
						harvest()
					plant(Entities.Bush)
					move(North)
				move(East)
		
		harvest_all_v2()

	# Only plant and harvest what is needed
	def bushes_precise():
		mark = num_items(Items.Wood) + goal

		harvest_map = []

		#Refer to grass_precise_v2 for general logic

		# More than one full harvest required
		if ((num_items(Items.Wood) + full_harvest_bush) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					plant(Entities.Bush)
					move(North)
				move(East)

			# 2+ rounds required
			while ((num_items(Items.Wood) + (full_harvest_bush * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						plant(Entities.Bush)
						move(North)
					move(East)

			# Will always run, final harvest/plant run before final harvest
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if ((num_items(Items.Wood) + full_harvest_bush) <= mark):
						harvest_map.append((get_pos_x(),get_pos_y()))
						plant(Entities.Bush)
					move(North)
				move(East)

		# Plant and map partial field
		else:
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (len(harvest_map) * unit_harvest + num_items(Items.Wood)) < mark:
						plant(Entities.Bush)
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (num_items(Items.Wood) < mark):
					move(East)
				else:
					break

		# Harvest any remaining bushes
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

	# Harvest and plant bushes with water - Continuous
	# Will leave full field behind
	def bushes_water(water_low = 0.8, water_high = 1.0):
		mark = num_items(Items.Wood) + goal
		while ((num_items(Items.Wood)) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					water_check(water_low, water_high)
					plant(Entities.Bush)
					move(North)
				move(East)

	# Same as bushes_water, but will harvest everything once completed
	def bushes_water_clean(water_low = 0.8, water_high = 1.0):
		mark = num_items(Items.Wood) + goal
		while ((num_items(Items.Wood)) < mark):
			for i in range (get_world_size()):
				if (num_items(Items.Wood) >= mark):
					break
				for j in range (get_world_size()):
					if (num_items(Items.Wood) >= mark):
						break
					if can_harvest():
						harvest()
					water_check(water_low, water_high)
					plant(Entities.Bush)
					move(North)
				move(East)
		
		harvest_all_v2()
	
	# Only plant and harvest what is needed
	def bushes_water_precise(water_low = 0.8, water_high = 1.0):
		mark = num_items(Items.Wood) + goal

		harvest_map = []

		# More than one full harvest required
		if ((num_items(Items.Wood) + full_harvest_bush) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					water_check(water_low, water_high)
					plant(Entities.Bush)
					move(North)
				move(East)

			# 2+ rounds required
			while ((num_items(Items.Wood) + (full_harvest_bush * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						water_check(water_low, water_high)
						plant(Entities.Bush)
						move(North)
					move(East)

			# Will always run, final harvest/plant run before final harvest
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if ((num_items(Items.Wood) + full_harvest_bush) <= mark):
						harvest_map.append((get_pos_x(),get_pos_y()))
						water_check(water_low, water_high)
						plant(Entities.Bush)
					move(North)
				move(East)

		# Plant and map partial field
		else:
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (len(harvest_map) * unit_harvest + num_items(Items.Wood)) < mark:
						water_check(water_low, water_high)
						plant(Entities.Bush)
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (num_items(Items.Wood) < mark):
					move(East)
				else:
					break

		# Harvest any remaining bushes
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

	#--------
	# TREES
	#--------

	# This section follows the same logic and naming for the bushes, but adapted for trees.
	#	Biggest modification has to do with planting requirements for trees

	def tree_normal():
		mark = num_items(Items.Wood) + goal
		while (num_items(Items.Wood) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					if on_grid():
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)
					move(North)
				move(East)

	def tree_clean():
		mark = num_items(Items.Wood) + goal
		while (num_items(Items.Wood) < mark):
			for i in range (get_world_size()):
				if (num_items(Items.Wood) >= mark):
					break
				for j in range (get_world_size()):
					if (num_items(Items.Wood) >= mark):
						break
					if can_harvest():
						harvest()
					if on_grid():
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)
					move(North)
				move(East)

		harvest_all_v2()
	
	# Will overproduce if polyculture is unlocked
	def tree_precise():
		mark = num_items(Items.Wood) + goal

		harvest_map = []

		# 1+ full harvest required
		if ((num_items(Items.Wood) + full_harvest_tree) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if on_grid():
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)
					move(North)
				move(East)

			# 2+ rounds required
			while ((num_items(Items.Wood) + (full_harvest_tree * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						if on_grid():
							plant(Entities.Tree)
						else:
							plant(Entities.Bush)
						move(North)
					move(East)

			# Will always run, final harvest/plant run before final harvest
			harvest_tracker = mark - num_items(Items.Wood)
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if (harvest_tracker > 0):
						if on_grid():
							plant(Entities.Tree)
							harvest_tracker -= unit_harvest * 5
						else:
							plant(Entities.Bush)
							harvest_tracker -= unit_harvest
						harvest_map.append((get_pos_x(),get_pos_y()))
					move(North)
				move(East)

		# Plant and map partial field
		# Due to varying values of crops planted, planted crops values will need to be tracked
		# Due to Polyculture, extra wood will likely be harvested
		#	Where this cannot be predicted, it will not be considered
		else:
			harvest_tracker = mark - num_items(Items.Wood)
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (harvest_tracker > 0):
						if on_grid():
							plant(Entities.Tree)
							harvest_tracker -= unit_harvest * 5
						else:
							plant(Entities.Bush)
							harvest_tracker -= unit_harvest
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (harvest_tracker > 0):
					move(East)
				else:
					break

		# Harvest any remaining plants
		quick_print("")
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

	def tree_water(bush_low = 0.8, tree_low = .29, water_high = 1.0):
		mark = num_items(Items.Wood) + goal
		while (num_items(Items.Wood) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					if on_grid():
						water_check(tree_low,water_high)
						plant(Entities.Tree)
					else:
						water_check(bush_low,water_high)
						plant(Entities.Bush)
					move(North)
				move(East)

	def tree_water_clean(bush_low = 0.8, tree_low = .29, water_high = 1.0):
		mark = num_items(Items.Wood) + goal
		while (num_items(Items.Wood) < mark):
			for i in range (get_world_size()):
				if (num_items(Items.Wood) >= mark):
					break
				for j in range (get_world_size()):
					if (num_items(Items.Wood) >= mark):
						break
					if can_harvest():
						harvest()
					if on_grid():
						water_check(tree_low,water_high)
						plant(Entities.Tree)
					else:
						water_check(bush_low,water_high)
						plant(Entities.Bush)
					move(North)
				move(East)

		harvest_all_v2()

	def tree_water_precise(bush_low = 0.8, tree_low = .29, water_high = 1.0):
		mark = num_items(Items.Wood) + goal

		harvest_map = []

		# 1+ full harvest required
		if ((num_items(Items.Wood) + full_harvest_tree) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if on_grid():
						water_check(tree_low,water_high)
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)
					move(North)
				move(East)

			# 2+ rounds required
			while ((num_items(Items.Wood) + (full_harvest_tree * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						if on_grid():
							water_check(tree_low,water_high)
							plant(Entities.Tree)
						else:
							water_check(bush_low,water_high)
							plant(Entities.Bush)
						move(North)
					move(East)

			# Will always run, final harvest/plant run before final harvest
			harvest_tracker = mark - num_items(Items.Wood)
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if (harvest_tracker > 0):
						if on_grid():
							water_check(tree_low,water_high)
							plant(Entities.Tree)
							harvest_tracker -= unit_harvest * 5
						else:
							water_check(bush_low,water_high)
							plant(Entities.Bush)
							harvest_tracker -= unit_harvest
						harvest_map.append((get_pos_x(),get_pos_y()))
					move(North)
				move(East)

		# Plant and map partial field
		else:
			harvest_tracker = mark - num_items(Items.Wood)
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (harvest_tracker > 0):
						if on_grid():
							water_check(tree_low,water_high)
							plant(Entities.Tree)
							harvest_tracker -= unit_harvest * 5
						else:
							water_check(bush_low,water_high)
							plant(Entities.Bush)
							harvest_tracker -= unit_harvest
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (harvest_tracker > 0):
					move(East)
				else:
					break

		# Harvest any remaining plants
		quick_print("")
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)

	def wood_benchmark():
		def run_benchmark(tester):
			clear_tilled()
			reset()
			if verbose:
				quick_print("")
				quick_print(tester[1])
				quick_print("Starting Water:", get_water())
			
			start_num = num_items(Items.Wood)
			start_ops = get_tick_count()
			start_time = get_time()
			
			tester[0]()
			
			ops_used = get_tick_count() - start_ops
			time_elapsed = get_time() - start_time
			items_produced = num_items(Items.Wood) - start_num

			if verbose:
				quick_print("Goal:", goal, "Items Produced:", items_produced)
				quick_print("Time Elapsed:", time_elapsed)
				quick_print("     Items per second:", (items_produced / time_elapsed))
				quick_print("Operations Used:", ops_used)
				quick_print("     Operations per item:", (ops_used / items_produced))
			return (time_elapsed, ops_used, items_produced/time_elapsed, ops_used/items_produced)

		func_list = [
				# [bushes_normal, "Normal Bushes", 0],
				[bushes_clean, "Clean Bushes", 0],
				[bushes_precise, "Precise Bushes", 0],
				# [tree_normal, "Normal Trees", 0],
				[tree_clean, "Clean Trees", 0],
				[tree_precise, "Precise Trees", 0],
				# [bushes_water, "Watered Bushes", 0],
				[bushes_water_clean, "Clean Watered Bushes", 0],
				[bushes_water_precise, "Precise Watered Bushes", 0],
				# [tree_water, "Watered Trees", 0],
				[tree_water_clean, "Clean Watered Trees", 0],
				[tree_water_precise, "Prcise Watered Trees", 0]
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
		wood_benchmark()
	else:
		if (num_unlocked(Unlocks.Trees) > 0):
			if num_unlocked(Unlocks.Watering > 0):
				tree_water_precise()
			else:
				tree_precise()
		else:
			if num_unlocked(Unlocks.Watering > 0):
				bushes_water_precise()
			else:
				bushes_precise()

wood(10000, True, False)